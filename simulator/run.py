
import seawolf

from simulator import Simulator
import entities
import model

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Simulator")

s = Simulator(
    robot_pos = [2, 2, 0],
)
s.add_entities( [
    entities.CubeEntity(1, (1, -2, 0), (1, 1, 1)),
    entities.CubeEntity(1, (2, -2, 0)),
    entities.CubeEntity(1, (3, -2, 0)),
    entities.CubeEntity(1, (4, -2, 0)),
    entities.CubeEntity(1, (5, -2, 0)),
    entities.CubeEntity(1, (6, -2, 0), (1, 1, 1)),
])
s.run()
