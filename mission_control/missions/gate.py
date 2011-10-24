

from __future__ import division

from vision import entities
from missions.base import MissionBase
from vision import process_manager
import sw3

MISSION_TIMEOUT = 3
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.4

class GateMission(MissionBase):

    def __init__(self):
        self.gate_seen = 0

    def init(self):
        self.process_manager.start_process(entities.GateEntity,"gate", "forward", debug = True)
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(FORWARD_SPEED),
            sw3.SetDepth(2),
            sw3.HoldYaw(),
        ]))

    def step(self, vision_data):
        print vision_data
        gate_data = vision_data['gate']
        if isinstance(gate_data, process_manager.KillSignal):
            raise gate_data

        if gate_data and gate_data.left_pole and gate_data.right_pole:
            gate_center = DEGREE_PER_PIXEL*(gate_data.left_pole + gate_data.right_pole)/2  # degrees

            # If both poles are seen, point toward it then go forward.
            self.set_entity_timeout(MISSION_TIMEOUT)
            self.gate_seen += 1

            if abs(gate_center) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.Forward(FORWARD_SPEED),
                    sw3.HoldYaw()
                ]))
                if self.gate_seen > 10:
                    print "Heading Locked"
                    self.finish_mission()
                    return
            else:
                print "Correcting Yaw", gate_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(gate_center),
                    sw3.Forward(0.4)
                ]))
