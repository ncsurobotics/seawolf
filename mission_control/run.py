#!/usr/bin/env python

'''
The main Seawolf mission control script.
'''

import sys
import os
from optparse import OptionParser

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
    missions.TestMission(),
]

if __name__ == "__main__":

    # Parse Arguments
    opt_parser = OptionParser()
    opt_parser.add_option("-i", "--initial-mission", action="store", default=0,
        dest="initial_mission", type="int",
        help="Specifies a mission index to start at.  Default 0.")
    opt_parser.add_option("-w", "--wait-for-go", action="store_true",
        default=True, dest="wait_for_go",
        help="Wait for mission go signal. (default)")
    opt_parser.add_option("-W", "--no-wait-for-go", action="store_false",
        dest="wait_for_go",
        help="Do not wait fo the go signal.")
    opt_parser.add_option("-d", "--delay", type="int",
        dest="delay", default=0.1,
        help="Delay between steps, in seconds.")
    opt_parser.add_option("-c", "--camera", nargs=2, action="append",
        type="string", metavar="<camera> <index/filename>",
        dest="cameras", default=[],
        help="Specifies that the camera given should use the given index or "
            "file to capture its frames.  Camera names should be one of: %s" %
            get_all_used_cameras())
    options, args = opt_parser.parse_args(sys.argv)

    # Put camera option into dictionary format
    camera_dict = {}
    for camera_name, camera_index in options.cameras:
        camera_dict[camera_name] = camera_index

    mission_index = options.initial_mission

    entity_searcher = vision.EntitySearcher(
        camera_indexes=camera_dict,
        #is_graphical=options.graphical, #TODO
        #record=options.record, #TODO
    )

    mission_controller = MissionController(entity_searcher)

    # Add missions
    for mission in MISSION_ORDER:
        mission_controller.append_mission(mission)

    mission_controller.execute_all()
