from __future__ import division

from acoustics import acoustics
from missions.base import MissionBase
import sw3
import math
from math import pi
from sw3 import util

import seawolf as sw

PORT_NAME = 'port'
MISSION_TIMEOUT = 5
# for which_path, 0 = right, 1 = left


class AcousticsMission(MissionBase):

    #### OVERRIDING VISION-BASED MISSION ####
    def register_mission_controller(self, mission_controller):
        ''' Called by the mission controller when the mission is added.'''
        self.mission_controller = mission_controller
        self.process_manager = acoustics

    def execute(self):
        '''Runs the mission.

        This is a blocking call that returns when the mission completes.
        '''

        if not hasattr(self, "timers"):
            self.timers = {}

        self._entity_timeout = getattr(self, "_entity_timeout", None)
        self._mission_done = getattr(self, "_mission_done", False)
        self._mission_fail = getattr(self, "_mission_fail", False)
        last_entity_timestamp = time()

        while not self._mission_done:

            if seawolf.var.get("MissionReset"):
                print "MISSION RESET"
                raise MissionControlReset()

            acoustics_data = self.process_manager.get_data(delay=0.05)

            self.step(vision_data)

            # Timer callbacks
            current_time = time()
            for name, (t, delay, callback, args) in self.timers.items():
                if t + delay <= current_time:
                    self.delete_timer(name)
                    callback(*args)

            if self._mission_fail:
                return False
        return True


    def init(self):
        '''runs at start of mission '''
        

    def step(self, vision_data):
        
