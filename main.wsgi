#!/usr/bin/python3

import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f'{dir_path}')

from main import app as application
