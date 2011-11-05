
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

# libseawolf Init
seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Simulator")

# Parse argument for mission
if len(sys.argv) < 2:
    parameter_set = "gate"
else:
    parameter_set = sys.argv[1]

# Determine initial parameters
if parameter_set == "gate" or parameter_set == "gate-straight":
    cam_pos = [13, 0, 25]
    cam_yaw = 90
    cam_pitch = -90
    robot_pos = [0, 0, 0]
    robot_yaw = 0
elif parameter_set == "gate-random":
    cam_pos = [13, 0, 25]
    cam_yaw = 90
    cam_pitch = -90
    robot_pos = [0, 0, 0]
    robot_yaw = random.uniform(-20, 20)
    print "Starting at yaw =", robot_yaw
elif parameter_set == "path1":
    cam_pos = [30, 0, 25]
    cam_yaw = 90
    cam_pitch = -90
    robot_pos = [22, 0, -2]
    robot_yaw = 0
else:
    raise ValueError("Unknown starting parameter set: %s" % parameter_set)

# Initialize everything!
interface = Interface(
    cam_pos = cam_pos,
    cam_yaw = cam_yaw,
    cam_pitch = cam_pitch,
)
robot = entities.RobotEntity(
    pos = robot_pos,
    yaw = robot_yaw,
)
simulator = Simulator(interface, robot, entities=[

    entities.AxisEntity(),

    entities.GateEntity((25, 0, 0)),
    entities.PathEntity((35, 0, -12), yaw=-45),
    entities.BuoysEntity((45, 10, -4), yaw=-45,
                         pos_red=(0, 0, 1.5),
                         pos_yellow=(0, 4, 0),
                         pos_green=(0, -4, -1.5))
])

simulator.run()
