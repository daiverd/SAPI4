# SAPI4 Flask Web Interface

Python 2.7 + Flask port of the SAPI4 web server for Microsoft Speech API 4.0 voices.

## Requirements

- Python 2.7
- Flask 1.1.4
- Windows environment (or Wine on Linux)
- Microsoft Speech API 4.0 with voices installed
- `sapi4out.exe` and `sapi4limits.exe` executables

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure `sapi4out.exe` and `sapi4limits.exe` are in the system PATH or current directory

3. Run the server:
   ```bash
   python run.py
   ```

## Usage

- Open http://127.0.0.1:23451 in your browser
- Select a voice from the dropdown
- Adjust pitch and speed parameters
- Enter text and click "Say it" to generate audio
- Right-click on the audio player to save the generated WAV file

## API Endpoints

- `/` - Main web interface
- `/VoiceLimitations?voice=(voice)` - Get voice parameter limits (JSON)
- `/SAPI4?text=(text)[&voice=(voice)][&pitch=(pitch)][&speed=(speed)]` - Generate TTS audio (returns WAV)

## Deployment

For production deployment with Wine on Linux:

```bash
# Install Wine and dependencies
# Install Microsoft Speech SDK and voices via winetricks
# Then run:
xvfb-run -a wine python run.py
```

## Compatibility

This version maintains API compatibility with the original D language server, using the same endpoints and parameters. It can be used as a drop-in replacement.