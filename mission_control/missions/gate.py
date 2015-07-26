
from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3, time

MISSION_TIMEOUT = 400
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.3
DEPTH = 2
DELAY = 2

class GateMission(MissionBase):

    def __init__(self):
        self.gate_seen = 0
        self.gate_lost = 0
        self.mission_timeout = MISSION_TIMEOUT

    def init(self):
        sw3.nav.do(
            sw3.SetDepth(DEPTH),
        )
        time.sleep(DELAY)
        self.process_manager.start_process(entities.GateEntity, "gate", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.HoldYaw(),
            sw3.Forward(FORWARD_SPEED),
        ))

    def step(self, vision_data):
        self.mission_timeout -= 1
        if not vision_data:
            return
        gate_data = vision_data['gate']
        if not gate_data:
            return
        print gate_data

        if gate_data and gate_data.left_pole and gate_data.right_pole:
            gate_center = DEGREE_PER_PIXEL * (gate_data.left_pole + gate_data.right_pole) / 2  # degrees

            # If both poles are seen, point toward it then go forward.
            self.gate_seen += 1
            self.gate_lost = 0

            if abs(gate_center) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.Forward(FORWARD_SPEED),
                    sw3.HoldYaw()
                ]))
            else:
                print "Correcting Yaw", gate_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(gate_center),
                    sw3.Forward(0.4)
                ]))
        elif self.gate_seen >= 15:
            self.gate_lost += 1

        if self.gate_lost > 1 or self.mission_timeout <= 0:
            print "Heading Locked"
            self.finish_mission()
            return
