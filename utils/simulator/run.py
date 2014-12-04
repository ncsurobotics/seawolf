#!/usr/bin/env python

import sys
import os
import random
from optparse import OptionParser

import seawolf

from simulator import Simulator
from interface import Interface
from vision import entities
import model

# Add mission_control/ to sys.path
parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../../.."
))
mission_control_directory = os.path.join(parent_directory, "mission_control/")
sys.path.append(mission_control_directory)

PARAMETER_SETS = {
    "gate": {
        "cam_pos": (13, 0, 25),
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": (0, 0, 0),
        "robot_yaw": 0,
    },
    "gate-random": {
        "cam_pos": (13, 0, 25),
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": (0, 0, 0),
        "robot_yaw": random.uniform(-20, 20),
    },
    "path1": {
        "cam_pos": (30, 0, 25),
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": (22, 0, -2),
        "robot_yaw": 0,
    },
    "buoys": {
        "cam_pos": (35, 0, 4),
        "cam_yaw": 45,
        "cam_pitch": -20,
        "robot_pos": (35, 0, -2),
        "robot_yaw": -45,
    },
    "path2": {
        "cam_pos": (30, 0, 25),
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": (56, 20, -2),
        "robot_yaw": -45,
    },
    "hedge": {
        "cam_pos": (35, 0, 4),
        "cam_yaw": 45,
        "cam_pitch": -20,
        "robot_pos": (60, 25, -3),
        "robot_yaw": -90,
    },
    "bins": {
        "robot_pos": (60, 43, -5),
        "robot_yaw": -115,
    },
}

opt_parser = OptionParser(
    usage="%prog [options] [initial-parameter-set]",
    description="Acts like the serialapp, but simulates the environment.",
)
opt_parser.add_option("-s", "--svr-source", action="store_true",
                      dest="svr_source", default=False,
                      help="Create an SVR source for each camera and stream what the robot is "
                      "seeing."
                      )
options, args = opt_parser.parse_args()
if len(args) < 2:
    parameters = PARAMETER_SETS['gate']
    parameter_set_name = 'gate'
elif args[1] in PARAMETER_SETS:
    parameters = PARAMETER_SETS[args[1]]
    parameter_set_name = args[1]
else:
    print 'Parameter set "%s" not found!  Valid parameter sets:\n%s' % \
        (args[1], PARAMETER_SETS.keys())
    sys.exit(1)

cam_pos = parameters["cam_pos"]
cam_yaw = parameters["cam_yaw"]
cam_pitch = parameters["cam_pitch"]
robot_pos = parameters["robot_pos"]
robot_yaw = parameters["robot_yaw"]

# libseawolf Init
seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Simulator")

# Initialize everything!
interface = Interface(
    cam_pos=cam_pos,
    cam_yaw=cam_yaw,
    cam_pitch=cam_pitch,
    parameter_sets=PARAMETER_SETS,
    svr_source=options.svr_source,
)
robot = entities.RobotEntity(
    pos=robot_pos,
    yaw=robot_yaw,
)
simulator = Simulator(interface, robot, entities=[

    entities.AxisEntity(),

    entities.GateEntity((25, 0, 0)),
    #entities.PathEntity((35, 0, -12), yaw=-45),
    entities.BuoyEntity((35, 2, -4), yaw=-15,
                        pos_red=(0, 0, 1.5),
                        pos_yellow=(0, 4, 0),
                        pos_green=(0, -4, -1.5)),
    entities.PathEntity((45, 4, -12), yaw=-20),
    entities.HedgeEntity((58, 8, -5), yaw=-45),
    entities.PathEntity((60, 10, -12), yaw=-20),
    entities.PathEntity((58, 58, -12), yaw=65),
    entities.BinsEntity((55, 70, -12), yaw=0),
])

print """
This simulator replaces the physical environment with a simulation.  The
simultor replaces the vision and serialapp applications.  Run mission control
with the -s flag to tell it to connect to the simulator instead of starting
vision processes.  All other applications should be run as normal.

Camera Movement:
    Forward/Backward    Mouse Wheel or up and down keys
          Look          Drag left mouse
          Pan           Drag middle mouse

Actions:
    Most of these actions can be accessed in the right click menu and a
    keyboard shortcut.

      Action        Key   Notes
     ---------      ---   -----------

       Reset         r    Reset the robot and camera to an initial state.
                          Right click menu gives more reset options.

    Camera Mode      m    Cycle between freecam and robot views.

   Zero Thrusters    z

       Quit               Only available through right click menu.  Closing the
                          window also exits.
"""

interface.last_parameter_set = parameter_set_name
simulator.run()
