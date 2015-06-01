
import sys

if sys.version_info < (2, 6):
    raise RuntimeError("Python version 2.6 or greater required!")

from data import data
from routines import *
from navqueue import NavQueue

import pid
import util

# Initialize the primary navigation stack
nav = NavQueue()

# Emergency breech function


def emergency_breech():
    nav.do(EmergencyBreech())
