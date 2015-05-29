#!/usr/bin/env python

from __future__ import division, print_function

import time
import sys
import seawolf

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Thruster Test")

# Names of all the thrusters to be tested
THRUSTERS = ["Bow", "Stern", "Port", "Star", "StrafeB", "StrafeT"]


def test_thruster_constant(name, val=.3):
    """ Test a named thruster at a given value ::val between -1 and 1
    """

    assert(-1 <= val <= 1)

    print("Testing {}".format(name))
    print("----------------")
    print("Setting {} to {} ".format(name, val), end="")
    sys.stdout.flush()

    seawolf.var.set(name, val)

    # a simple time.sleep(3.5) here would suffice, but this is prettier
    for i in range(0, 6):
        print(".", end="")
        sys.stdout.flush()
        time.sleep(.5)

    seawolf.var.set(name, 0.0)

    print(" 0.0")


def test_thruster_over_range(name, begin=-.3, end=.3, inc=.1):
    """ Test a named thruster over a range of values from ::begin to ::end with increment ::incr
    """

    assert(-1 <= begin <= 1)
    assert(-1 <= end <= 1)

    begin = int(begin * 10)
    end = int(end * 10 + (1 if end > 0 else -1))
    inc = int(inc * 10)

    # Produce a range of values from begin to end with increments of inc
    VALUE_RANGE = [x / 10 for x in range(begin, end, inc)]

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
    # test_thruster_over_range(thruster, .3, -.3, -.1)
    test_thruster_constant(thruster, .3)
    print()

seawolf.close()
