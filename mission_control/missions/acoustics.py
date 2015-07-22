from __future__ import division

from vision import entities
from acoustics import acoustics
from missions.base import MissionBase
import sw3
import math
from math import pi
from sw3 import util

import seawolf as sw

PORT_NAME = 'port'
YAW_TOLERANCE = 10
EPOCH_STALE = 5

class AcousticsMission(MissionBase):

    def init(self):
        '''runs at start of mission '''
        self.process_manager.start_process(entities.PathEntity, "path", "forward", debug=True)
        self.acoustics = acoustics.Acoustics()
        self.acoustics.connect(PORT_NAME)

    def step(self, vision_data):
        if not vision_data:
            return

        ac_data = self.acoustics.get_data()

        if ac_data['error'] == 0:
            epoch = ac_data['data']['epoch']
            rel_yaw = ac_data['data']['heading']['ab']
            if epoch > 5:
               # data is stale
               return
            if abs(rel_yaw) > YAW_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine(sw3.RelativeYaw(rel_yaw), sw3.Forward(.3))
        
