
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

INITIAL_TIMEOUT = 25  # Timeout if we never see the love lane
MISSION_TIMEOUT = 8  # Timeout after we've seen the love lane

DEGREE_PER_PIXEL = 0.19
APPROACH_SPEED = 0.4
TRACKING_SPEED = 0.4
DEPTH = 4

class LoveLaneMission(MissionBase):

    def __init__(self):
        pass

    def init(self):
        self.set_entity_timeout(INITIAL_TIMEOUT)
        self.entity_searcher.start_search([
            entities.LoveLaneEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(APPROACH_SPEED), sw3.SetDepth(DEPTH)
        ]))

    def step(self, entity_found):

        # Finish when timeout reached
        if not entity_found:
            return True

        # Set a smaller timeout once we see the lane
        self.set_entity_timeout(MISSION_TIMEOUT)

        target_yaw = entity_found.center[0] * DEGREE_PER_PIXEL

        print "Correcting Yaw", target_yaw
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.RelativeYaw(target_yaw),
            sw3.Forward(TRACKING_SPEED)
        ]))

