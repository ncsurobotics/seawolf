from __future__ import division
import math
from math import pi

import seawolf
from time import time
from missions.base import MissionBase
from vision import process_manager
from vision import entities
import sw3
from sw3 import util

BOX_DEPTH = 8
FORWARD_SPEED = .3
ORIENT_THRESH = 15

class AcousticsMission(MissionBase):

    def __init__(self):
        pass
    def init(self):
        self.pinger_data = var_watch('Acoustics.Channels')
        self.process_manager.start_process(entities.AcousticsEntity, "acoustics", "down", debug=True)
        self.reference_angle = sw3.data.imu.yaw()

        self.orientdata = None
        self.states = [
            "followpinger",
            "findbox",
            "grab",
            "drop",
            "findpath"
        ]
        self.state_num = 0
        self.state = self.states[self.state_num]

    def step(self, vision_data):
        if pinger_data is not None:
            self.orientdata = pinger_data.orientation
        if vision_data is not None:
            box = vision_data.box

        if self.state == "followpinger":
            pinger_data = var_watch('Acoustics.Channels')
            self.followpinger(pinger_data)
        if self.state == "findbox":
            self.findbox(vision_data)
        if self.state == "grab":
            self.grab(box)
        if self.state == "drop":
            self.drop()
        if self.state == "findpath":
            self.findpath()

    def followpinger(self, pinger_data):
        if pinger_data:
                
                self.nextState()

    def findbox(self, vision_data):
        self.nextState()

    def grab(self, box):
        self.nextState()

    def drop(self):
        self.nextState()

    def findpath(self):
        sw3.nav.do(sw3.Forward(.1, 2))
        self.finish_mission()

    def nextState(self):
        self.state_num += 1
        #if self.state_num >= len(self.states):
            #self.finish_mission()
        self.state = self.states[self.state_num]
        print "State:", self.state
       
