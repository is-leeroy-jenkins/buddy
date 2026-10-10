# -*- mode: python ; coding: utf-8 -*-
"""Package Buddy and its dynamically loaded application dependencies."""
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules, copy_metadata

root = Path( SPECPATH )
datas = [(str( root / 'app.py' ), '.'),
         (str( root / 'resources' ), 'resources'),
         (str( root / '.streamlit' / 'config.toml' ), '.streamlit')]
# Runtime databases are created in user storage; development data and secrets are excluded.
hiddenimports = ['config', 'gpt', 'gemini', 'grok', 'models']
binaries = []
for package in ('streamlit', 'streamlit_extras', 'streamlit_pdf', 'webview',
                'plotly', 'sqlite_vec', 'sentence_transformers', 'transformers',
                'torch', 'torchvision', 'tiktoken', 'xai_sdk', 'openai',
                'google.genai', 'google.cloud.storage', 'boogr'):
    package_datas, package_bins, package_hidden = collect_all( package )
    datas += package_datas
    binaries += package_bins
    hiddenimports += package_hidden
for distribution in ('streamlit', 'sentence-transformers', 'transformers'):
    datas += copy_metadata( distribution, recursive=True )

a = Analysis( [str( root / 'desktop.py' )], pathex=[str( root )],
    binaries=binaries, datas=datas, hiddenimports=hiddenimports,
    hookspath=[], runtime_hooks=[], excludes=[], noarchive=False )
pyz = PYZ( a.pure )
exe = EXE( pyz, a.scripts, [], exclude_binaries=True, name='Buddy',
    console=False, disable_windowed_traceback=False )
coll = COLLECT( exe, a.binaries, a.datas, strip=False, upx=False, name='Buddy' )
