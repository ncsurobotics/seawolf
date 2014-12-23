#!/usr/bin/env python

from __future__ import division, print_function

import time
import sys
import seawolf

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Thruster Test")

# Names of all the thrusters to be tested
THRUSTERS = ["Bow", "Stern", "Port", "Star", "StrafeB", "StrafeT"]

# Produce a range of values from -.3 to .3 in increments of .1
VALUE_RANGE = [x / 10 for x in range(-3, 4, 1)]


def test_thruster(name):

    print("Testing {}".format(name))
    print("----------------")
    print("Setting {} to ".format(name), end="")

    for val in VALUE_RANGE:
        assert(-1 <= val <= 1)
        seawolf.var.set(name, val)

        print("{}".format(val), end="  ")
        sys.stdout.flush()

        time.sleep(.7)

    seawolf.var.set(name, 0.0)
    print("0.0")


for thruster in THRUSTERS:
    test_thruster(thruster)
    print()

seawolf.close()
