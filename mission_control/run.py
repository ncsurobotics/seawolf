#!/usr/bin/env python

'''
The main Seawolf mission control script.
'''

import sys
import os
from optparse import OptionParser
from time import sleep
import subprocess
import sw3

parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../.."
))
vision_directory = os.path.join(parent_directory, "vision/")
sys.path.append(parent_directory)
sys.path.append(vision_directory)

import vision
import missions
from mission_controller import MissionController

#This is the list of missions, it may contain either missions
# or NavRoutines
MISSION_ORDER = [
    #missions.GateMission,
    sw3.RelativeYaw(-90),
    sw3.Forward(.5,5),
    sw3.Forward(0,1),
    sw3.RelativeYaw(-90),
    sw3.Forward(.5,5),
    #missions.TestMission,
]

def unbreak_firewire():
    try:
        ret = subprocess.call(["dc1394_reset_bus"])
    except OSError:
        print "Warning: You don't have the dc1394_reset_bus command. " \
            "Cannot reset firewire bus."
        return
    if ret != 0:
        print "Warning: Could not reset firewire bus."

if __name__ == "__main__":

    # Parse Arguments
    opt_parser = OptionParser()
    opt_parser.add_option("-i", "--initial-mission", action="store", default=0,
        dest="initial_mission", type="int",
        help="Specifies a mission index to start at.  Default 0.")
    opt_parser.add_option("-w", "--wait-for-go", action="store_true",
        default=False, dest="wait_for_go",
        help="Wait for mission go signal. (default)")
    opt_parser.add_option("-W", "--no-wait-for-go", action="store_false",
        dest="wait_for_go",
        help="Do not wait fo the go signal.")
    opt_parser.add_option("-d", "--delay", type="int",
        dest="delay", default=10,
        help="Delay between frames, in milliseconds, or -1 to wait for "
            "keypress")
    opt_parser.add_option("-r", "--record", action="store_true",
        default="true", dest="record",
        help="All images captured from cameras will be recorded.")
    opt_parser.add_option("-R", "--not-record", action="store_false",
        dest="record",
        help="Images captured from cameras will not be recorded.")
    opt_parser.add_option("-g", "--graphical", action="store_true",
        dest="graphical",
        help="Indicates that graphical windows can be displayed.")
    opt_parser.add_option("-G", "--non-graphical", action="store_false",
        default="true", dest="graphical",
        help="Indicates that no graphical windows will be displayed.")
    options, args = opt_parser.parse_args(sys.argv)

    unbreak_firewire()
    sleep(1)

    process_manager = vision.ProcessManager()

    while True:

        mission_controller = MissionController(
            process_manager,
            options.wait_for_go,
        )

        # Add missions
        for mission_cls in MISSION_ORDER[options.initial_mission:]:
            if isinstance(mission_cls, sw3.NavRoutine):
                mission_controller.append_mission(mission_cls)
            else:
                mission_controller.append_mission(mission_cls())

        try:
            mission_controller.execute_all()
        except missions.MissionControlReset:
            mission_controller.kill()
            sleep(2)
            continue
        else:
            break

    process_manager.kill()
    mission_controller.kill()

