#!/usr/bin/env python2

from __future__ import division, print_function

import time
import sys
import seawolf

# Names of all the thrusters to be tested
THRUSTERS = ["Bow", "Stern", "Port", "Star", "StrafeB", "StrafeT"]


def main(args):
    # Connect to hub
    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Thruster Test")

    # Default test function
    default = test_thruster_constant

    # Arguments
    opts = {
        "const": test_thruster_constant,
        "range": test_thruster_over_range
    }

    # If the name of a test function was provided by the user as an argument, use it
    func = opts.get(args[0], default) if args else default

    print("Running test", func.__name__, "\n")

    # Run the chosen test function against all the thrusters
    try:
        for thruster in THRUSTERS:
            # test_thruster_over_range(thruster, .3, -.3, -.1)
            func(thruster, duration=4)
            print()

    # Safely exit if CTRL+C
    except (KeyboardInterrupt, AssertionError) as e:
        print()
        print(e)
        print("Setting all thrusters to 0")
        for thruster in THRUSTERS:
            seawolf.var.set(thruster, 0.0)

    seawolf.close()


def test_thruster_constant(name, duration=4, val=.3):
    """ Test a named thruster at a given value ::val between -1 and 1
    """

    assert(-1 <= val <= 1)

    print("Testing {}".format(name))
    print("--------------------")
    print("Setting {} to {} ".format(name, val), end="")
    sys.stdout.flush()

    seawolf.var.set(name, val)

    # a simple time.sleep(length) here would suffice, but this is prettier
    wait_time = duration / 8

    for i in range(0, 8):
        print(".", end="")
        sys.stdout.flush()
        time.sleep(wait_time)

    seawolf.var.set(name, 0.0)

    print(" END")


def test_thruster_over_range(name, duration=.45, begin=-.3, end=.3, inc=.1):
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
    print("END")


if __name__ == '__main__':
    main(sys.argv[1:])
