
from __future__ import division
from time import time

import entities
from missions.base import MissionBase
import sw3
import seawolf

INITIAL_FORWARD_SPEED = 3.5
BUMPING_SPEED = 3.0
BUMPING_TIME = 3 #how many seconds we give seawolf to bump the buoy
BACKING_SPEED = -2.5 #how fast to back up
BACKUP_TIME = 2  #how many seconds to back up for
RELATIVE_DEPTH = -1.5 #how much to surface to clear the buoy
BYPASS_SPEED = 3.5 #how fast to pass over the buoy
BYPASS_TIME = 3 #how long to spend passing over the buoy

class BuoyBumpMission(MissionBase):

    def init(self):
        self.entity_searcher.start_search([
            entities.BuoyBoxEntity(),
        ])
        sw3.nav.do(
            sw3.Forward(INITIAL_FORWARD_SPEED), 
        )

        self.state = "Searching"

    def step(self, entity_found):
        if (self.state == "Searching"):
            self.state = "Bumping" 
            sw3.nav.do(
                sw3.Forward(BUMPING_SPEED),
            )
            self.entity_searcher.start_search([])
            self.set_entity_timeout(BUMPING_TIME)

        elif self.state == "Bumping":
            self.state = "BackingUp"
            sw3.nav.do(
                sw3.Forward(BACKING_SPEED),
            )
            self.set_entity_timeout(BACKUP_TIME)

        elif self.state == "BackingUp":
            self.state = "Rising"

            forward_routine = sw3.Forward(BYPASS_SPEED,BYPASS_TIME)
            relative_depth_up = sw3.RelativeDepth(RELATIVE_DEPTH)
            relative_depth_down = sw3.RelativeDepth(-1*RELATIVE_DEPTH)
            
            relative_depth_up.on_done(lambda x : sw3.nav.do(forward_routine))
            forward_routine.on_done(lambda x : sw3.nav.do(relative_depth_down)) 
            relative_depth_down.on_done(self.finish_mission)

            sw3.nav.do(relative_depth_up)

        return False
            


