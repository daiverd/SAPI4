# -*- coding: utf-8 -*-
"""
SAPI4 Flask Web Interface
Python 2.7 + Flask port of the D language SAPI4 web server
"""
import os
import sys
import json
import tempfile
import subprocess
import time
from flask import Flask, render_template, request, jsonify, send_file, abort

app = Flask(__name__)

# Global dictionary to store voice information
VOICES = {}

def get_executable_path(exe_name):
    """Get the correct path to bundled executables"""
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundle
        return os.path.join(sys._MEIPASS, exe_name)
    else:
        # Running as regular Python script
        return exe_name

class Voice(object):
    """Voice configuration class"""
    def __init__(self, name):
        self.name = name
        self.def_pitch = 0
        self.min_pitch = 0
        self.max_pitch = 0
        self.def_speed = 0
        self.min_speed = 0
        self.max_speed = 0
        
        # Get voice limits from sapi4limits.exe
        try:
            sapi4limits_path = get_executable_path('sapi4limits.exe')
            proc = subprocess.Popen([sapi4limits_path, name], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            
            if proc.returncode != 0:
                print("sapi4limits failed for voice: %s" % name)
                return
                
            # Clean output and parse
            output = stdout.replace("err:xrandr:xrandr12_init_modes Failed to get primary CRTC info.", "").strip()
            lines = output.split('\r\n')
            
            if len(lines) >= 3:
                self.name = lines[0]
                
                # Parse pitch values
                pitch_parts = lines[1].split(' ')
                if len(pitch_parts) >= 3:
                    self.def_pitch = int(pitch_parts[0])
                    self.min_pitch = int(pitch_parts[1])
                    self.max_pitch = int(pitch_parts[2])
                
                # Parse speed values  
                speed_parts = lines[2].split(' ')
                if len(speed_parts) >= 3:
                    self.def_speed = int(speed_parts[0])
                    self.min_speed = int(speed_parts[1])
                    self.max_speed = int(speed_parts[2])
                    
        except Exception as e:
            print("Error getting voice limits for %s: %s" % (name, str(e)))

def initialize_voices():
    """Initialize available voices by calling sapi4limits.exe"""
    global VOICES
    try:
        sapi4limits_path = get_executable_path('sapi4limits.exe')
        proc = subprocess.Popen([sapi4limits_path], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        
        if proc.returncode != 0:
            print("sapi4limits failed")
            sys.exit(1)
            
        # Clean output and get voice list
        output = stdout.replace("err:xrandr:xrandr12_init_modes Failed to get primary CRTC info.", "").strip()
        voice_names = output.split('\r\n')
        
        # Initialize each voice
        for voice_name in voice_names:
            if voice_name.strip():
                VOICES[voice_name] = Voice(voice_name)
                
    except Exception as e:
        print("Error initializing voices: %s" % str(e))
        sys.exit(1)

@app.route('/')
def index():
    """Main TTS interface"""
    voice_list = sorted(VOICES.keys())
    return render_template('index.html', voices=voice_list)

@app.route('/VoiceLimitations')
def voice_limitations():
    """Get voice parameter limits as JSON"""
    voice_name = request.args.get('voice', '')
    
    if not voice_name or voice_name not in VOICES:
        abort(400, "Invalid voice")
    
    voice = VOICES[voice_name]
    return jsonify({
        'defPitch': voice.def_pitch,
        'minPitch': voice.min_pitch,
        'maxPitch': voice.max_pitch,
        'defSpeed': voice.def_speed,
        'minSpeed': voice.min_speed,
        'maxSpeed': voice.max_speed
    })

@app.route('/Voices')
def get_voices():
    """Get all available voices with their parameter limits as JSON"""
    voices_data = {}
    
    for voice_name, voice in VOICES.items():
        voices_data[voice_name] = {
            'defPitch': voice.def_pitch,
            'minPitch': voice.min_pitch,
            'maxPitch': voice.max_pitch,
            'defSpeed': voice.def_speed,
            'minSpeed': voice.min_speed,
            'maxSpeed': voice.max_speed
        }
    
    return jsonify(voices_data)

@app.route('/SAPI4')
def generate_tts():
    """Generate TTS audio using sapi4out.exe"""
    try:
        # Get parameters
        text_raw = request.args.get('text', '')
        voice_name = request.args.get('voice', 'INVALID')
        
        # Validate text
        if not text_raw or len(text_raw) > 4095:
            abort(400, "Invalid text")
        
        # Convert text to ASCII/Latin-1 for SAPI4 compatibility
        try:
            text = text_raw.encode('ascii', 'ignore')
        except UnicodeError:
            try:
                text = text_raw.encode('latin-1', 'ignore')
            except UnicodeError:
                abort(400, "Text encoding error")
        
        # Validate voice
        if voice_name not in VOICES:
            abort(400, "Invalid voice")
        
        voice = VOICES[voice_name]
        
        # Parse pitch and speed
        try:
            pitch = int(request.args.get('pitch', -1))
            speed = int(request.args.get('speed', -1))
        except (ValueError, TypeError):
            abort(400, "Invalid pitch/speed")
        
        # Use defaults if not specified
        if pitch == -1:
            pitch = voice.def_pitch
        if speed == -1:
            speed = voice.def_speed
        
        # Validate ranges
        if pitch < voice.min_pitch or pitch > voice.max_pitch:
            abort(400, "Available pitch: [%d; %d], got %d" % (voice.min_pitch, voice.max_pitch, pitch))
        
        if speed < voice.min_speed or speed > voice.max_speed:
            abort(400, "Available speed: [%d; %d], got %d" % (voice.min_speed, voice.max_speed, speed))
        
        # Execute sapi4out.exe with timeout
        try:
            sapi4out_path = get_executable_path('sapi4out.exe')
            proc = subprocess.Popen([sapi4out_path, voice_name, str(pitch), str(speed), text],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            
            # Wait with timeout (10 seconds)
            start_time = time.time()
            while proc.poll() is None and (time.time() - start_time) < 10:
                time.sleep(0.1)
            
            if proc.poll() is None:
                proc.terminate()
                abort(400, "Please reformat your text")
            
            stdout, stderr = proc.communicate()
            
            if proc.returncode != 0:
                abort(400, "Please reformat your text")
                
            # Get output file path
            output_file = stdout.replace("err:xrandr:xrandr12_init_modes Failed to get primary CRTC info.", "").strip()
            
            if not output_file or not os.path.exists(output_file):
                abort(500, "Audio generation failed")
            
            # Send file and clean up
            try:
                return send_file(output_file, mimetype='audio/wav', as_attachment=False)
            finally:
                # Clean up temp file after sending
                try:
                    os.remove(output_file)
                except:
                    pass
                    
        except Exception as e:
            print("TTS generation error: %s" % str(e))
            abort(500, "Audio generation failed")
            
    except Exception as e:
        print("Request error: %s" % str(e))
        abort(500, "Internal server error")

# Use run.py for starting the server