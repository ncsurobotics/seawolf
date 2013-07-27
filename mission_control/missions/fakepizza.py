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

class FakePizzaMission(MissionBase):

    def __init__(self):
        pass
    def init(self):
        sw3.nav.do(sw3.SetDepth(6))
        self.process_manager.start_process(entities.PizzaCornerEntity, "pizzabox", "down", debug=True)
        self.reference_angle = sw3.data.imu.yaw()
        self.highest_id = None

        self.states = [
            "findpizza",
            "pickup",
        ]
        self.state_num = 0
        self.state = self.states[self.state_num]

    def step(self, vision_data):
        if vision_data.pizza is None:
            pizzabox = None
        else:
            pizzabox = vision_data.pizza
        if self.state == "findpizza":
            self.findpizza(pizzabox)
        if self.state == "pickup":
            self.pickup()

    def findpizza(self, pizzabox):
        #go forward until pizza box, then slightly more.
        if not pizzabox:
            sw3.nav.do(sw3.Forward(.3,1))
        else: 
            sw3.nav.do(sw3.Forward(0,0))
            self.nextState()

    def pickup(self):
        sw3.nav.do(sw3.CompoundRoutine(
                    sw3.SetDepth(9),
                    sw3.Forward(0,0),
                    sw3.SetDepth(0)
        ))
        self.nextState()

    def nextState(self):
        self.state_num += 1
        #if self.state_num >= len(self.states):
            #self.finish_mission()
        self.state = self.states[self.state_num]
        print "State:", self.state
       
