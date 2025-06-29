# -*- coding: utf-8 -*-
"""
py2exe setup script for SAPI4 Flask application
For native Windows XP building (better XP compatibility than PyInstaller)
"""
from distutils.core import setup
import py2exe
import sys
import os

# Ensure we're building with py2exe
if len(sys.argv) == 1:
    sys.argv.append("py2exe")

# Get current directory for data files
current_dir = os.path.dirname(os.path.abspath(__file__))

# Data files to include
data_files = [
    # Flask templates
    ('templates', [
        os.path.join(current_dir, 'templates', 'base.html'),
        os.path.join(current_dir, 'templates', 'index.html'),
    ]),
    # Static files
    ('static', [
        os.path.join(current_dir, 'static', 'style.css'),
        os.path.join(current_dir, 'static', 'favicon.ico'),
    ]),
    ('static/scripts', [
        os.path.join(current_dir, 'static', 'scripts', 'tts.js'),
    ]),
    # SAPI4 executables and DLL
    ('.', [
        os.path.join(current_dir, 'sapi4out.exe'),
        os.path.join(current_dir, 'sapi4limits.exe'),
        os.path.join(current_dir, 'sapi4.dll'),
    ]),
]

# py2exe options optimized for Windows XP
py2exe_options = {
    'packages': ['flask', 'werkzeug', 'jinja2', 'markupsafe', 'itsdangerous', 'click'],
    'includes': ['os', 'sys', 'time', 'json', 'tempfile', 'subprocess', 'unicodedata'],
    'excludes': ['_tkinter', 'Tkinter', 'ssl', 'hashlib', '_hashlib', 'doctest', 'pdb', 'unittest'],
    'compressed': True,
    'optimize': 2,
    'bundle_files': 1,  # Single exe file
    'dist_dir': 'dist',
}

setup(
    name='SAPI4_Flask_XP',
    version='1.0',
    description='SAPI4 Flask TTS Server - Windows XP Native',
    
    console=[{
        'script': 'run.py',
        'dest_base': 'sapi4_flask_py2exe',
        'icon_resources': [(1, os.path.join(current_dir, 'static', 'favicon.ico'))],
    }],
    
    data_files=data_files,
    options={'py2exe': py2exe_options},
    zipfile=None,  # Include everything in exe
)