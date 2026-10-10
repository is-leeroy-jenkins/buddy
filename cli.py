"""Installed application entry points.

Purpose:
    Launches the packaged Streamlit application with writable per-user storage.
"""
from pathlib import Path
import os
import sys
from . import desktop as launcher


def prepare_runtime( ) -> Path:
    """Provision application data and expose the existing script imports.

    Returns:
        Path: Writable application working directory.
    """
    root = Path( __file__ ).resolve( ).parent
    sys.path.insert( 0, str( root ) )
    directory = launcher.prepare_user_data( )
    os.chdir( directory )
    return directory


def main( ) -> None:
    """Run Buddy through the Streamlit command-line interface.

    Returns:
        None: Runs until the application server exits.
    """
    prepare_runtime( )
    from streamlit.web.cli import main as streamlit_main
    arguments = sys.argv[ 1: ]
    sys.argv = ['streamlit', 'run', str( Path( __file__ ).with_name( 'app.py' ) ),
                *arguments]
    streamlit_main( )


def desktop( ) -> None:
    """Run the Windows WebView2 launcher from an installed distribution.

    Returns:
        None: Runs until the desktop window closes.
    """
    if os.name != 'nt':
        raise RuntimeError( 'The Buddy desktop window requires Windows and WebView2.' )
    prepare_runtime( )
    launcher.main( )
