# Windows XP Native Build Instructions

## Prerequisites for Windows XP

1. **Python 2.7.11** (last version to support Windows XP)
   - Download: https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi
   - Install to default location (C:\Python27)

2. **PyInstaller 3.6** (last version to support Windows XP)
   ```cmd
   pip install pyinstaller==3.6
   ```

3. **Flask Dependencies**
   ```cmd
   pip install Flask==1.1.4 Werkzeug==1.0.1 MarkupSafe==1.1.1 Jinja2==2.11.3 itsdangerous==1.1.0 click==7.1.2
   ```

## Build Process on Windows XP

1. **Copy all files to Windows XP machine**:
   - All Python files (`app.py`, `run.py`)
   - SAPI4 files (`sapi4out.exe`, `sapi4limits.exe`, `sapi4.dll`)
   - Templates and static folders
   - `sapi4_flask_minimal.spec`

2. **Build executable**:
   ```cmd
   cd C:\path\to\sapi4_flask
   pyinstaller --onefile sapi4_flask_minimal.spec
   ```

3. **Output**: `dist\sapi4_flask_minimal.exe`

## Troubleshooting

### If PyInstaller 3.6 fails:
Try PyInstaller 3.2.1 (compiled with VS2008 for better XP compatibility):
```cmd
pip uninstall pyinstaller
pip install pyinstaller==3.2.1
pyinstaller --onefile sapi4_flask_minimal.spec
```

### If dependencies fail to install:
- Ensure you're using Python 2.7.11 (not newer versions)
- Try installing without SSL verification:
  ```cmd
  pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==1.1.4
  ```

### Required Visual C++ Runtime:
Windows XP may need Visual C++ 2008 Redistributable Package (x86)

## Expected Result

- Single executable: `sapi4_flask_minimal.exe` (~3-4MB)
- Should run directly on Windows XP SP3
- Access via: http://localhost:23451