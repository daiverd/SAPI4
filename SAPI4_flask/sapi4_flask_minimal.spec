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
]

# Define binaries to include (SAPI4 executables and DLL)
binaries = []
sapi4_files = ['sapi4out.exe', 'sapi4limits.exe', 'sapi4.dll']
for filename in sapi4_files:
    filepath = os.path.join(spec_dir, filename)
    if os.path.exists(filepath):
        binaries.append((filepath, '.'))
    else:
        print("Warning: {} not found in {}".format(filename, spec_dir))

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
        # Exclude EVERYTHING that might be problematic on XP
        'tkinter', 'Tkinter', '_tkinter',
        'ssl', 'hashlib', '_hashlib', '_ssl',
        'asyncio', 'concurrent', 'threading',
        '_socket', 'socket', 'select',
        'xml', 'xml.etree', 'xml.parsers', 'xml.sax',
        'email', 'smtplib', 'urllib', 'urllib2', 'urlparse',
        'doctest', 'pdb', 'unittest', 'difflib', 'inspect',
        'pydoc', 'pickle', 'cPickle', 'shelve',
        'bz2', 'gzip', 'tarfile', 'zipfile',
        'sqlite3', 'dbm', 'anydbm',
        'ctypes.wintypes', 'msvcrt',
        'multiprocessing', 'subprocess32',
        'locale', 'codecs', 'encodings.idna',
        'distutils', 'setuptools', 'pkg_resources',
        'importlib', 'imp',
        'optparse', 'argparse', 'getopt',
        'logging', 'logging.handlers',
        'platform', 'getpass', 'pwd', 'grp',
        'stat', 'posix', 'posixpath',
        'decimal', 'fractions', 'numbers',
        'calendar', 'datetime', 'time',
        'random', 'uuid',
        'collections', 'heapq', 'bisect',
        'array', 'struct', 'binascii',
        'base64', 'uu', 'binhex',
        'mimetypes', 'quopri',
        'StringIO', 'cStringIO',
        'weakref', 'copy', 'copy_reg',
        'repr', 'pprint',
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