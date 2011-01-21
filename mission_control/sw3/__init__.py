
import sys

if sys.version_info < (2, 5):
    raise RuntimeError("Python version 2.6 or greater required!")

from data import data
import pid
import nav
