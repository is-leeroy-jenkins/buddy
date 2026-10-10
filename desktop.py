"""
    ******************************************************************************************
      Assembly:                Buddy
      Filename:                desktop.py
      Purpose:                 Launch Buddy in a local Windows desktop webview.
    ******************************************************************************************
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen


def application_root( ) -> Path:
    """Return the installed application assets directory.

    Returns:
        Path: Bundled resource directory for frozen or source execution.
    """
    return Path( getattr( sys, '_MEIPASS', Path( __file__ ).resolve( ).parent ) )


def user_data_root( ) -> Path:
    """Resolve the writable per-user Buddy directory.

    Returns:
        Path: Directory outside the protected installation location.
    """
    base = os.environ.get( 'LOCALAPPDATA' )
    if base is None:
        base = str( Path.home( ) / 'AppData' / 'Local' )
    location = Path( base ) / 'Buddy'
    location.mkdir( parents=True, exist_ok=True )
    return location


def prepare_user_data( ) -> Path:
    """Provision writable resources and storage without overwriting user data.

    Returns:
        Path: Writable working directory for the Streamlit server.
    """
    destination = user_data_root( )
    source = application_root( )
    for name in ( 'resources', '.streamlit' ):
        directory = source / name
        if directory.exists( ):
            shutil.copytree( directory, destination / name, dirs_exist_ok=True,
                copy_function=copy_if_missing )
    (destination / 'stores' / 'sqlite').mkdir( parents=True, exist_ok=True )
    os.environ[ 'LOG_DIR' ] = str( destination / 'logging' )
    return destination


def copy_if_missing( source: str, destination: str ) -> str:
    """Copy bundled defaults only when the destination does not already exist.

    Args:
        source (str): Original bundled file.
        destination (str): Writable target.

    Returns:
        str: Destination filename.
    """
    if not Path( destination ).exists( ):
        shutil.copy2( source, destination )
    return destination


def free_port( ) -> int:
    """Find a currently unused TCP port on loopback.

    Returns:
        int: Port reserved during inspection; released before server startup.
    """
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as sock:
        sock.bind( ('127.0.0.1', 0) )
        return int( sock.getsockname( )[ 1 ] )


def serve( port: int, directory: Path ) -> None:
    """Run Buddy's Streamlit app inside the child process.

    Args:
        port (int): Loopback TCP port.
        directory (Path): Writable application data location.

    Returns:
        None: Blocks until Streamlit exits.
    """
    os.chdir( directory )
    from streamlit.web import bootstrap
    app = application_root( ) / 'app.py'
    bootstrap.run( str( app ), False, [ ], {
        'server.address': '127.0.0.1',
        'server.port': port,
        'server.headless': True,
        'browser.gatherUsageStats': False,
        'server.fileWatcherType': 'none',
        'server.enableCORS': True,
        'server.enableXsrfProtection': True,
    } )


def wait_for_server( process: subprocess.Popen, port: int ) -> None:
    """Wait for the child server health endpoint or fail on early exit.

    Args:
        process (subprocess.Popen): Streamlit child process.
        port (int): Child TCP port.

    Returns:
        None: Server was reachable before timeout.

    Raises:
        RuntimeError: Server exited or failed to become healthy.
    """
    endpoint = f'http://127.0.0.1:{port}/_stcore/health'
    for attempt in range( 240 ):
        if process.poll( ) is not None:
            raise RuntimeError( 'Buddy Streamlit server exited before startup.' )
        try:
            with urlopen( endpoint, timeout=1 ) as response:
                if response.status == 200:
                    return
        except (OSError, URLError):
            time.sleep( 0.5 )
    raise RuntimeError( 'Buddy Streamlit server did not become ready within 120 seconds.' )


def main( ) -> None:
    """Launch the dedicated webview, terminating its server on window close.

    Returns:
        None: The process exits after the webview is closed.
    """
    if len( sys.argv ) == 4 and sys.argv[ 1 ] == '--buddy-server':
        serve( int( sys.argv[ 2 ] ), Path( sys.argv[ 3 ] ) )
        return

    import webview
    working_directory = prepare_user_data( )
    port = free_port( )
    command = [ sys.executable, '--buddy-server', str( port ), str( working_directory ) ]
    if not getattr( sys, 'frozen', False ):
        command.insert( 1, str( Path( __file__ ).resolve( ) ) )
    log_path = working_directory / 'desktop.log'
    log = log_path.open( 'a', encoding='utf-8' )
    server = subprocess.Popen( command, cwd=working_directory, stdout=log, stderr=log,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0 )
    try:
        wait_for_server( server, port )
        webview.create_window( 'Buddy', f'http://127.0.0.1:{port}',
            width=1400, height=900, min_size=(900, 600) )
        webview.start( gui='edgechromium', debug=False )
    except Exception as error:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.MessageBoxW( 0,
                f'{error}\n\nStartup log: {log_path}', 'Buddy startup error', 16 )
        raise
    finally:
        if server.poll( ) is None:
            server.terminate( )
            try:
                server.wait( timeout=10 )
            except subprocess.TimeoutExpired:
                server.kill( )
                server.wait( )
        log.close( )


if __name__ == '__main__':
    main( )
