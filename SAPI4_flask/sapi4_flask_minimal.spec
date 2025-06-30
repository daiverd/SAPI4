# -*- mode: python ; coding: utf-8 -*-
# Ultra-minimal PyInstaller spec for maximum Windows XP compatibility
# Excludes everything that might cause XP issues

import os
import sys

block_cipher = None

# Get the directory containing this spec file
spec_dir = os.path.dirname(os.path.abspath(SPEC))

# Define data files to include
datas = [
    (os.path.join(spec_dir, 'templates'), 'templates'),
    (os.path.join(spec_dir, 'static'), 'static'),
    # Include SAPI4 files as data files (since binaries didn't work)
    ('sapi4out.exe', '.'),
    ('sapi4limits.exe', '.'),
    ('sapi4.dll', '.'),
]

# Define binaries to include (empty - using datas instead)
binaries = []

# Verify files exist
for src, dst in binaries:
    if not os.path.exists(src):
        print("ERROR: {} not found in current directory".format(src))

# Absolutely minimal hidden imports - only core essentials
hiddenimports = [
    'flask',
    'werkzeug.serving',
    'werkzeug.urls', 
    'werkzeug.http',
    'jinja2',
    'markupsafe',
    'tempfile',
    'subprocess',
    'json',
    'os',
    'sys',
]

a = Analysis(
    ['run.py'],
    pathex=[spec_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        # Exclude only the most problematic modules for XP
        'tkinter', 'Tkinter', '_tkinter',
        'ssl', '_ssl',  # Keep hashlib, exclude only SSL
        'asyncio', 'concurrent.futures',
        'multiprocessing',
        'sqlite3',
        'doctest', 'pdb', 'unittest',
        'distutils', 'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sapi4_flask_minimal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # No compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon=os.path.join(spec_dir, 'static', 'favicon.ico') if os.path.exists(os.path.join(spec_dir, 'static', 'favicon.ico')) else None
)