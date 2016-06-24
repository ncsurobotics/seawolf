from __future__ import division
import sys
sys.path.append("/home/seawolf/software/acoustics/host_communication/seawolf/")
import time

from vision import entities
import acoustics_client
from missions.base import MissionBase
import sw3
import math
from math import pi
from sw3 import util

import seawolf as sw

PORT_NAME = '/dev/ttyUSB3'
YAW_TOLERANCE = 10
EPOCH_STALE = 5

class AcousticsMission(MissionBase):

    def init(self):
        '''runs at start of mission '''
        #self.process_manager.start_process(entities.PathEntity, "path", "forward", debug=True)
        self.acoustics = acoustics_client.Acoustics()
        self.acoustics.connect(PORT_NAME)

    def step(self, vision_data):
        #if not vision_data:
        #    return

        ac_data = self.acoustics.get_data()

        if ac_data['error'] == 0:
            # grab data
            epoch = ac_data['data']['epoch']
            rel_yaw = ac_data['data']['heading']['ab']

            if epoch > 5:
                print "data is stale. will try again later"
                return # data is stale

            print rel_yaw

            if abs(rel_yaw) > YAW_TOLERANCE:
                sw3.nav.do(
                    sw3.CompoundRoutine(
                        sw3.RelativeYaw(rel_yaw), sw3.Forward(.3)
                        )
                    )

            time.sleep(6)