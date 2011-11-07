
import sys
import os
import random

import seawolf

from simulator import Simulator
from interface import Interface
from vision import entities
import model

# Add mission_control/ to sys.path
parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../.."
))
mission_control_directory = os.path.join(parent_directory, "mission_control/")
sys.path.append(mission_control_directory)

PARAMETER_SETS = {
    "gate": {
        "cam_pos": [13, 0, 25],
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": [0, 0, 0],
        "robot_yaw": 0,
    },
    "gate-random": {
        "cam_pos": [13, 0, 25],
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": [0, 0, 0],
        "robot_yaw": random.uniform(-20, 20),
    },
    "path1": {
        "cam_pos": [30, 0, 25],
        "cam_yaw": 90,
        "cam_pitch": -90,
        "robot_pos": [22, 0, -2],
        "robot_yaw": 0,
    },
    "buoys": {
        "cam_pos": [35, 0, 4],
        "cam_yaw": 45,
        "cam_pitch": -20,
        "robot_pos": [35, 0, -2],
        "robot_yaw": -45,
    },
}

# libseawolf Init
seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Simulator")

# Parse argument for initial parameters
if len(sys.argv) < 2:
    parameters = PARAMETER_SETS['gate']
elif sys.argv[1] in PARAMETER_SETS:
    parameters = PARAMETER_SETS[sys.argv[1]]
else:
    print 'Parameter set "%s" not found!  Valid parameter sets:\n%s' % \
            (sys.argv[1], PARAMETER_SETS.keys())
    sys.exit(1)

cam_pos = parameters["cam_pos"]
cam_yaw = parameters["cam_yaw"]
cam_pitch = parameters["cam_pitch"]
robot_pos = parameters["robot_pos"]
robot_yaw = parameters["robot_yaw"]

# Initialize everything!
interface = Interface(
    cam_pos = cam_pos,
    cam_yaw = cam_yaw,
    cam_pitch = cam_pitch,
    parameter_sets = PARAMETER_SETS,
)
robot = entities.RobotEntity(
    pos = robot_pos,
    yaw = robot_yaw,
)
simulator = Simulator(interface, robot, entities=[

    entities.AxisEntity(),

    entities.GateEntity((25, 0, 0)),
    entities.PathEntity((35, 0, -12), yaw=-45),
    entities.BuoysEntity((55, 20, -4), yaw=-45,
                         pos_red=(0, 0, 1.5),
                         pos_yellow=(0, 4, 0),
                         pos_green=(0, -4, -1.5))
])

simulator.run()
