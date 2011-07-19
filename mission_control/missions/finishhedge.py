
from __future__ import division
from time import time

import entities
from missions.base import MissionBase
import sw3
import seawolf

ANGULAR_CORRECTION = 4 #degrees to turn after finishing hedge

INITIAL_FORWARD_SPEED = .30
INITIAL_TIMEOUT = 15

FINISHED_DEPTH = 2
RISE_TIME = 3
TURNING_TIME = 2 #time to turn 

class FinishHedgeMission(MissionBase):

    def init(self):
        self.entity_searcher.start_search([
            entities.BuoyBoxEntity(),
        ])
        sw3.nav.do(
            sw3.Forward(INITIAL_FORWARD_SPEED),
        )

        self.state = "Searching"
        self.set_entity_timeout(INITIAL_TIMEOUT) # XXX 

    def step(self, entity_found):
        if self.state == "Searching":
            self.state = "Rising"
            sw3.nav.do(
                sw3.SetDepth(FINISHED_DEPTH),
            )
            self.entity_searcher.start_search([])
            self.set_entity_timeout(RISE_TIME)
            print "Rising"

        elif self.state == "Rising":
            self.state = "Turning"
            sw3.nav.do(
                sw3.RelativeYaw(ANGULAR_CORRECTION),
            )
            self.set_entity_timeout(TURNING_TIME)
            print "Turning"

        elif self.state == "Turning":
            print "finished finishing hedge"
            return True

        return False

