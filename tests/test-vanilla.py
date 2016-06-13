#!/usr/bin/env python

# [test-vanilla.py]: a template for creating new test files.
# This folder contains the bare minimum for open a file under
# hub's supervision just like all the other scripts written for
# seawolf. This is meant to be generic and copy&paste-able for
# quickly creating new test scripts

from __future__ import division, print_function

import seawolf
# other imports here...

seawolf.loadConfig("../conf/seawolf.conf") # <--Contains IP for connecting to hub
seawolf.init("Sensor Test") #<--Gives program a name under hub

"""
Do stuff here
"""

seawolf.close() #<--Gracefully disconnects program from hub
