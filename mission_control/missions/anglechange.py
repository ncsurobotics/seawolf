
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

ANGLE_CHANGE = 2 #amount to turn before beginning Love Lane

class AngleChangeMission(MissionBase):

    def __init__(self):
        pass

    def init(self):
        self.entity_searcher.start_search([ ])
        sw3.nav.do( sw3.RelativeYaw(ANGLE_CHANGE) )
        self.set_entity_timeout(1)

    def step(self, entity_found):
        print "Finished Turning"
        return True

