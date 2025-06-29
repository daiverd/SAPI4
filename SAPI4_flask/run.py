#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
SAPI4 Flask Server Runner
For Windows with Wine compatibility
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, initialize_voices

if __name__ == '__main__':
    print("SAPI4 Flask Server - Python 2.7")
    print("Initializing voices...")
    
    try:
        initialize_voices()
        print("Server starting on http://0.0.0.0:23451")
        app.run(host='0.0.0.0', port=23451, debug=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print("Error: %s" % str(e))
        sys.exit(1)