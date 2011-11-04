
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
elif parameter_set == "path1":
    cam_pos = [30, 0, 25]
    cam_yaw = 90
    cam_pitch = -90
    robot_pos = [22, 0, 0]
    robot_yaw = 0
else:
    raise ValueError("Unknown starting parameters: %s" % parameter_set)

# Initialize everything!
interface = Interface(
    cam_pos = cam_pos,
    cam_yaw = cam_yaw,
    cam_pitch = cam_pitch,
)
robot = entities.RobotEntity(
    model.ObjModel(file("models/seawolf5.obj")),
    pos = robot_pos,
    yaw = robot_yaw,
    yaw_offset = -90,
)
simulator = Simulator(interface, robot, entities=[
    entities.AxisEntity(),
    entities.GateEntity((25, 0, 0)),
    entities.PathEntity((30, 0, -8), yaw=-45),
])

simulator.run()
