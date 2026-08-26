#!/usr/bin/python3
"""
WSGI Entry Point for 360IT Learning & Consulting Application.
Compatible with Apache mod_wsgi, Gunicorn, uWSGI, and cPanel/Passenger.
"""

import os
import sys

# Determine project root directory
if '__file__' in globals():
    dir_path = os.path.dirname(os.path.abspath(__file__))
else:
    dir_path = os.getcwd()

if dir_path not in sys.path:
    sys.path.insert(0, dir_path)


# Activate virtual environment if available
venv_activate = os.path.join(dir_path, '.venv', 'bin', 'activate_this.py')
if os.path.exists(venv_activate):
    with open(venv_activate) as f:
        exec(f.read(), {'__file__': venv_activate})

# Ensure environment variables are loaded from .env
from dotenv import load_dotenv
load_dotenv(os.path.join(dir_path, '.env'))

# Import Flask WSGI application instance
from app import app as application

# Export application callable for WSGI servers
__all__ = ['application']

