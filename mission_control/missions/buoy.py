

from __future__ import division

import entities
from missions.base import MissionBase
from vision import process_manager
import sw3
import math
from math import pi
from sw3 import util
from math import fabs
from time import time


MISSION_TIMEOUT = 5
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.2
CENTER_THRESHOLD = 2
FIELD_OF_VIEW=20
CENTER_TIME = 5
MIN_ANGLE_THRESHOLD = 5
MAX_ANGLE_THRESHOLD = 175
BUMP_COUNTER = 0
BACKWARD_SPEED = -0.2


PREV_BUOY = 0# the buoy we just bumped, 0 is none, 1 left, 2 center, 3 right

FIRST_BUOY = 1 #First buoy to hit, 1 is left, 2 is center, 3 is right
SECOND_BUOY = 3 #Second buoy to hit, 1 is left, 2 is center, 3 is right

class BuoyMission(MissionBase):

    def __init__(self):
        self.path_seen = 0

    def init(self):
        '''runs at start of mission '''
        self.process_manager.start_process(entities.BuoyEntity,"buoy", "forward", debug = True)
       

        sw3.nav.do(sw3.SetDepth(4))
        sw3.nav.do(sw3.Forward(FORWARD_SPEED,5))

        self.reference_angle = sw3.data.imu.yaw*(pi/180) % (2*pi)
        self.state = "centering"
           
        self.buoytimer = None

    def step(self, vision_data):
        #include code to condsider if we never see three bouys, and operate with what we have
        if not (vision_data['buoy'].buoys[0].found and vision_data['buoy'].buoys[1].found and vision_data['buoy'].buoys[2].found):
            return 0
        buoy0_x = vision_data['buoy'].buoys[0].x
        buoy1_x = vision_data['buoy'].buoys[1].x
        buoy2_x = vision_data['buoy'].buoys[2].x
        
        if buoy0_x < buoy1_x and buoy0_x < buoy2_x:
            self.left_id = vision_data['buoy'].buoys[0].id
        if buoy1_x < buoy0_x and buoy1_x < buoy2_x:
            self.left_id = vision_data['buoy'].buoys[1].id
        if buoy2_x < buoy0_x and buoy2_x < buoy1_x:
            self.left_id = vision_data['buoy'].buoys[2].id

        if buoy0_x > buoy1_x and buoy0_x > buoy2_x:
            self.right_id = vision_data['buoy'].buoys[0].id
        if buoy1_x > buoy0_x and buoy1_x > buoy2_x:
            self.right_id = vision_data['buoy'].buoys[1].id
        if buoy2_x > buoy0_x and buoy2_x > buoy1_x:
            self.right_id = vision_data['buoy'].buoys[2].id

        if buoy0_x < fabs(buoy1_x) and buoy0_x < fabs(buoy2_x):
            self.center_id = vision_data['buoy'].buoys[0].id
        if buoy1_x < fabs(buoy0_x) and buoy1_x < fabs(buoy2_x):
            self.center_id = vision_data['buoy'].buoys[1].id
        if buoy2_x < fabs(buoy0_x) and buoy2_x < fabs(buoy1_x):
            self.center_id = vision_data['buoy'].buoys[2].id
        
        


       # vision_data['buoy'].bouys[0].
        
        if self.state == "centering" and vision_data['bouy'].buoys[0].found and vision_data['buoy'].buoys[1].found and vision_data['buoy'].buoys[2].found:
            self.state_center(vision_data)
        if self.state == "buoy":
            self.state_buoy(vision_data)
        if self.state =="reset":
            self.state_buoy(vision_data)
        if self.state == "findpath":
            self.state_findpath(vision_data)


    def state_center(self,vision_data):
        sw3.nav.do(sw3.Forward(0))
        
        #figure out which x coordinate is closest to origin
        x = [0,1,2]
        for i in x:
            if self.center_id == vision_data['buoy'].buoys[i].id:
                center_x = vision_data['buoy'].buoys[i].x
        if center_x > 5:
            sw3.nav.do(sw3.RelativeYaw(5))
        elif center_x < -5:
            sw3.nav.do(sw3.RelativeYaw(-5))
        else:
            self.state = "buoy"
            
    

    def state_buoy(self,vision_data):
        if BUMP_COUNTER == 0:
            if FIRST_BUOY == 1: # LEFT BUOY

                x = [0,1,2]
                for i in x:
                    if self.left_id == vision_data['buoy'].buoys[i].id:
                        left_x = vision_data['buoy'].buoys[i].x

                if left_x > -5:
                    sw3.nav.do(sw3.RelativeYaw(-10))
                else:
                    if not self.buoytimer:
                        self.buoytimer = time() + 7
                    sw3.nav.do(sw3.Forward(FORWARD_SPEED, 7))
          
                if time() > self.buoytimer:
                    self.buoytimer = None
                    self.state = "reset"
                    PREV_BUOY = 1
                    BUMP_COUNTER+=1

            if FIRST_BUOY == 2: #Center buoy
                
                x = [0,1,2]
                for i in x:
                    if self.center_id == vision_data['buoy'].buoys[i].id:
                        center_x = vision_data['buoy'].buoys[i].x
                #figure out which x coordinate is closest to origin
                                                                  
                                                                  
                                                                  
                if center_x > 5:
                    center_angle = current_yaw + 5
                    sw3.nav.do(sw3.RelativeYaw(5))
                elif center_x < -5:
                    center_angle = current_yaw - 5
                    sw3.nav.do(sw3.RelativeYaw(-5))

                else:
                    if not self.buoytimer:
                        self.buoytimer = time() + 7
                    sw3.nav.do(sw3.Forward(FORWARD_SPEED, 7))
          
                if time() > self.buoytimer:
                    self.buoytimer = None
                    self.state = "reset"
                    PREV_BUOY = 2
                    BUMP_COUNTER+=1

            if FIRST_BUOY == 3: #Right buoy

                x = [0,1,2]
                for i in x:
                    if self.right_id == vision_data['buoy'].buoys[i].id:
                        right_x = vision_data['buoy'].buoys[i].x

                if right_x < 5:
                    sw3.nav.do(sw3.RelativeYaw(10))
                else:
                    if not self.buoytimer:
                        self.buoytimer = time() + 7
                    sw3.nav.do(sw3.Forward(FORWARD_SPEED, 7))
          
                if time() > self.buoytimer:
                    self.buoytimer = None
                    self.state = "reset"
                    PREV_BUOY = 3
                    BUMP_COUNTER+=1

        if BUMP_COUNTER == 1:
            if SECOND_BUOY == 1:  #left buoy

                x = [0,1,2]
                for i in x:
                    if self.left_id == vision_data['buoy'].buoys[i].id:
                        left_x = vision_data['buoy'].buoys[i].x

                if left_x > -5:
                    sw3.nav.do(sw3.RelativeYaw(-10))
                else:
                    if not self.buoytimer:
                        self.buoytimer = time() + 7
                    sw3.nav.do(sw3.Forward(FORWARD_SPEED, 7))
          
                if time() > self.buoytimer:
                    self.buoytimer = None
                    self.state = "reset"
                    PREV_BUOY = 1
                    BUMP_COUNTER+=1

            if SECOND_BUOY == 2: #center buoy
                                                                  
                x = [0,1,2]
                for i in x:
                    if self.center_id == vision_data['buoy'].buoys[i].id:
                        center_x = vision_data['buoy'].buoys[i].x

                if center_x > 5:
                    sw3.nav.do(sw3.RelativeYaw(-5))
                elif center_x < 5:
                    sw3.nav.do(sw3.RelativeYaw(5))
                else:
                    if not self.buoytimer:
                        self.buoytimer = time() + 7
                    sw3.nav.do(sw3.Forward(FORWARD_SPEED, 7))
          
                if time() > self.buoytimer:
                    self.buoytimer = None
                    self.state = "reset"
                    PREV_BUOY = 2
                    BUMP_COUNTER+=1

            if SECOND_BUOY == 3: #right buoy

                x = [0,1,2]
                for i in x:
                    if self.right_id == vision_data['buoy'].buoys[i].id:
                        right_x = vision_data['buoy'].buoys[i].x

                if right_x < 5:
                    sw3.nav.do(sw3.RelativeYaw(10)
                else:
                    if not self.buoytimer:
                        self.buoytimer = time() + 7
                    sw3.nav.do(sw3.Forward(FORWARD_SPEED, 7))
          
                if time() > self.buoytimer:
                    self.buoytimer = None
                    self.state = "reset"
                    PREV_BUOY = 3
                    BUMP_COUNTER+=1

    def state_reset(self,buoy_data):
        self.prev_angle = sw3.data.imu.yaw
            sw3.nav.do(sw3.Forward(0))
            if not self.buoytimer:
                self.buoytimer = time() + 4
            sw3.nav.do(sw3.SetYaw(self.prev_angle))    
            sw3.nav.do(sw3.Forward(BACKWARD_SPEED,4))

            if time() > self.buoytimer:
                self.buoytimer = None
                sw3.nav.do(sw3.SetYaw(self.reference_angle))
                if vision_data['buoy'].buoys[0].found and vision_data['buoy'].buoys[1].found and vision_data['buoy'].buoys[2].found:
                    self.state = "centering"

    def state_findpath(self)
        
