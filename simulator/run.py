
import sys
import os

import seawolf

parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../.."
))
mission_control_directory = os.path.join(parent_directory, "mission_control/")
sys.path.append(mission_control_directory)

from simulator import Simulator
from vision import entities
import model

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Simulator")

s = Simulator(
    robot_pos = [0, 0, 0],
    cam_pos = [13, 0, 25],
    cam_yaw = 90,
    cam_pitch = -90,
)
s.add_entities( [
    #entities.CubeEntity(1, (1, -2, 0), (1, 1, 1)),
    #entities.CubeEntity(1, (2, -2, 0)),
    #entities.CubeEntity(1, (3, -2, 0)),
    #entities.CubeEntity(1, (4, -2, 0)),
    #entities.CubeEntity(1, (5, -2, 0)),
    #entities.CubeEntity(1, (6, -2, 0), (1, 1, 1)),
    entities.GateEntity((25, 0, 0)),
    entities.AxisEntity(),
])
s.run()
