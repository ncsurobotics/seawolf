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

simulator = False

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
    opt_parser.add_option("-c", "--camera", nargs=2, action="append",
        type="string", metavar="<camera> <index/filename>",
        dest="cameras", default=[],
        help="Specifies that the camera given should use the given index or "
            "file to capture its frames.  If this option is not given for a "
            "camera, SVR is used.")
    opt_parser.add_option("-d", "--delay", type="int",
        dest="delay", default=0,
        help="Delay between frames, in milliseconds, or -1 to wait for "
            "keypress.  Default is 0.")
    opt_parser.add_option("-G", "--non-graphical", action="store_false",
        dest="graphical", default=True,
        help="Takes vision out of debug mode, disallowing windows to be displayed.")
    opt_parser.add_option("-s", "--simulator", action="store_true",
        default=False, dest="simulator",
        help="Connect to the simulator instead of starting vision processes.")
    options, args = opt_parser.parse_args(sys.argv)

    if len(args) > 1:
        opt_parser.error("%prog accepts no positional arguments!")
    # It seems silly to assign this to another variable, but options will not
    # be defined if __name__ != "__main__".
    simulator = options.simulator

parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../.."
))
vision_directory = os.path.join(parent_directory, "vision/")
sys.path.append(vision_directory)
if simulator:
    print "Using Simulator..."
    simulator_directory = os.path.join(parent_directory, "simulator/")
    sys.path.append(simulator_directory)
else:
    sys.path.append(parent_directory)

import vision
import missions
from mission_controller import MissionController

# Ordered list of tasks.  Can be one of the following types:
#  * Mission Class - Found in ``missions.<name>Mission``.  Instantiated with no
#                    arguments.
#  * Nav routine - Found in ``sw3.nav.<name>``.
#  * Tuple - First item must be a mission class.  The rest of the tuple is
#            passed in as arguments to the ``mission.__init__``.
MISSION_ORDER = [
    missions.GateMission,
   (missions.PathMission, False, 0),
    #sw3.SetDepth(6.0, timeout=5),
    missions.BuoyMission,
  # missions.SimpleBuoyMission,
    missions.PathMission,
    sw3.SetDepth(8.0, timeout=5),
    missions.HedgeMission,
    (missions.PathMission, True, 1),
    sw3.Forward(.5, 1),
    missions.NewBinsMission,
    #(missions.PathMission, None, 15, True, 0, 50),
    #(missions.PathMission, 0, 30),
    #missions.HedgeMission
    missions.AcousticsMission
]

if __name__ == "__main__":

    # Put camera option into dictionary format
    cameras_dict = {}
    for name, index in options.cameras:
        cameras_dict[name] = index

    if options.graphical and options.delay == 0:
        options.delay = 10

    process_manager = vision.ProcessManager(extra_kwargs={
        "delay": options.delay,
        "cameras": cameras_dict,
        "debug": options.graphical,
    })

    try:
        while True:

            mission_controller = MissionController(
                process_manager,
                options.wait_for_go,
            )

            # Add missions
            for mission in MISSION_ORDER[options.initial_mission:]:
                if isinstance(mission, sw3.NavRoutine):
                    mission.reset()
                    mission_controller.append_mission(mission)
                else:
                    if type(mission) is tuple:
                        mission_cls = mission[0]
                        args = mission[1:]
                    else:
                        mission_cls = mission
                        args = ()
                    mission_controller.append_mission(mission_cls(*args))

            try:
                mission_controller.execute_all()
            except missions.MissionControlReset:
                mission_controller.kill()
                sleep(2)
                continue
            else:
                break

    finally:
        process_manager.kill()
        mission_controller.kill()

