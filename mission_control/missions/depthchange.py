
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

DEPTH_CHANGE = 2 #amount to turn before beginning Love Lane

class DepthChangeMission(MissionBase):

    def __init__(self):
        pass

    def init(self):
        self.entity_searcher.start_search([ ])
        sw3.nav.do(
            sw3.SetDepth(DEPTH_CHANGE),
        )
        self.set_entity_timeout(5)

    def step(self, entity_found):
        print "Finished Setting Depth"
        return True

