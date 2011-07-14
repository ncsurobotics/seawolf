#!/usr/bin/env python

'''
The main Seawolf mission control script.
'''

import sys
import os
from optparse import OptionParser
from time import sleep
import subprocess

parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../.."
))
vision_directory = os.path.join(parent_directory, "vision/")
sys.path.append(parent_directory)
sys.path.append(vision_directory)

import vision
from entities import get_all_used_cameras
import missions
from mission_controller import MissionController

MISSION_ORDER = [
    missions.GateMission(),
    missions.PathMission(),
    missions.BuoysMission(),
    missions.BuoyBumpMission(),
    missions.PathMission(),
    missions.LoveLaneMission(),
    missions.DoublePathMission(),
    missions.BinsMission(),
    missions.PathMission(),
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
    opt_parser.add_option("-c", "--camera", nargs=2, action="append",
        type="string", metavar="<camera> <index/filename>",
        dest="cameras", default=[],
        help="Specifies that the camera given should use the given index or "
            "file to capture its frames.  Camera names should be one of: %s" %
            vision.entities.get_all_used_cameras())
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

    # Put camera option into dictionary format
    camera_dict = {}
    for camera_name, camera_index in options.cameras:
        camera_dict[camera_name] = camera_index

    unbreak_firewire()
    sleep(1)

    entity_searcher = vision.EntitySearcher(
        camera_indexes=camera_dict,
        is_graphical=options.graphical,
        record=options.record,
        delay=options.delay,
    )

    while True:

        mission_controller = MissionController(
            entity_searcher,
            options.wait_for_go,
        )

        # Add missions
        for mission in MISSION_ORDER[options.initial_mission:]:
            mission_controller.append_mission(mission)

        try:
            mission_controller.execute_all()
        except missions.MissionControlReset:
            mission_controller.kill()
            sleep(2)
            continue
        else:
            break

    entity_searcher.kill()
    mission_controller.kill()

