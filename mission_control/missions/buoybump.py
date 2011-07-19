
from __future__ import division
from time import time

import entities
from missions.base import MissionBase
import sw3
import seawolf

ANGULAR_CORRECTION = 5 #degrees to turn when above buoys
TURNING_TIME = 0.5 #time to turn while above buoys

INITIAL_FORWARD_SPEED = .35
INITIAL_TIMEOUT = 27
BUMPING_SPEED = .3
BUMPING_TIME = 5 #how many seconds we give seawolf to bump the buoy
BACKING_SPEED = -.4 #how fast to back up
BACKUP_TIME = 3  #how many seconds to back up for
#RELATIVE_DEPTH = -2.5 #how much to surface to clear the buoy
BYPASS_DEPTH = 2.0 #where to surface to clear the buoy
BYPASS_SPEED = .60 #how fast to pass over the buoy
BYPASS_TIME = 5 #how long to spend passing over the buoy
RISE_TIME = 5
BYPASS_TIME = 8
DESCENT_TIME = 3

class BuoyBumpMission(MissionBase):

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
        if (self.state == "Searching"):
            self.state = "Bumping"
            sw3.nav.do(
                sw3.Forward(BUMPING_SPEED),
            )
            self.entity_searcher.start_search([])
            self.set_entity_timeout(BUMPING_TIME)
            print "Bumping"

        elif self.state == "Bumping":
            self.state = "BackingUp"
            sw3.nav.do(
                sw3.Forward(BACKING_SPEED),
            )
            self.set_entity_timeout(BACKUP_TIME)
            print "BackingUp"

        elif self.state == "BackingUp":
            self.state = "Rising"

            sw3.nav.do(sw3.CompoundRoutine([
                sw3.SetDepth(BYPASS_DEPTH),
                sw3.Forward(0),
            ]))
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
            self.state = "Bypassing"

            sw3.nav.do(sw3.CompoundRoutine([
                sw3.Forward(BYPASS_SPEED),
            ]))
            self.set_entity_timeout(BYPASS_TIME)
            print "Bypassing"

        elif self.state == "Bypassing":
            #finish the mission
            return True

        return False

