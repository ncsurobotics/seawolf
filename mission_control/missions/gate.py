
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

MISSION_TIMEOUT = 3
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.4

class GateMission(MissionBase):

    def __init__(self, gate_type=entities.GATE_WHITE):
        self.gate_type = gate_type
        self.gate_seen = 0
        self.heading_locked = False

    def init(self):
        self.entity_searcher.start_search([
            entities.GateEntity(self.gate_type),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(FORWARD_SPEED), sw3.SetDepth(2)
        ]))

    def step(self, entity_found):
        print entity_found

        if not entity_found:  # timeout has been triggered
            if self.gate_seen:
                return True
            else:
                return False

        if self.heading_locked:
            return  # Do nothing while heading is locked

        if entity_found.left_pole and entity_found.right_pole:
            gate_center = DEGREE_PER_PIXEL*(entity_found.left_pole + entity_found.right_pole)/2  # degrees

            # If both poles are seen, point toward it then go forward.
            self.set_entity_timeout(MISSION_TIMEOUT)
            self.gate_seen += 1

            if abs(gate_center) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.Forward(FORWARD_SPEED),
                    sw3.HoldYaw()
                ]))
                if self.gate_seen > 30:
                    self.heading_locked = True
                    print "Heading Locked"
            else:
                print "Correcting Yaw", gate_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(gate_center),
                    sw3.Forward(0.4)
                ]))
