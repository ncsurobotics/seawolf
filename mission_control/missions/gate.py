
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

MISSION_TIMEOUT = 3
DEGREE_PER_PIXEL = 0.19
STRAIGHT_TOLERANCE = 5  # In degrees

class GateMission(MissionBase):

    def __init__(self, gate_type=entities.GATE_WHITE):
        self.gate_type = gate_type
        self.gate_seen = 0

    def init(self):
        self.entity_searcher.start_search([
            entities.GateEntity(self.gate_type),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(0.1), sw3.SetDepth(2)
        ]))

    def step(self, entity_found):

        if not entity_found:  # timeout has been triggered
            if self.gate_seen:
                return True
            else:
                return False

        # If both poles are seen, point toward it then go forward.
        if entity_found.left_pole and entity_found.right_pole:
            self.set_entity_timeout(MISSION_TIMEOUT)
            self.gate_seen += 1

            angle = (entity_found.left_pole + entity_found.right_pole)/2  # degrees
            if abs(angle) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.Forward(0.1))
            else: 
                sw3.nav.do(sw3.RelativeYaw(angle))
                sw3.nav.append(sw3.Forward(0.1))
