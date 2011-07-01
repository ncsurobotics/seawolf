
from __future__ import division
import math
from math import pi
#from collections import de

from missions.base import MissionBase
import entities
import sw3
from sw3 import util

#bins we are supposed to mark.
# 1=X  2=O  3=x  4=o 
BIN1 = 1
BIN2 = 2
# If the bin's position is off by more than this much, turn towards it
DISTANCE_CAP = 100   #determines where to cap the linear scaling of velocity
INITIAL_CENTERING_TIMEOUT_THRESHOLD = 300 #Timeout length when centering on our first bin
INITIAL_DIVING_TIMEOUT_THRESHOLD = 300 #Timeout length when diving to exam height
ANGULAR_CENTERING_THRESHOLD = 10 #anglular tolerance for alligning with target angles
RADIAL_CENTERING_THRESHOLD = 50  #radial displacement tolerance for alligning with targets
MISSION_TIMEOUT = 800 #blindly restart the mission if we see nothing for this long
CENTERED_COUNTER_THRESHOLD = 5 #how long we must stay centered before acknowledging it 
APPROACH_DEPTH = 2 #how deep when approaching obstacle
EXAM_DEPTH = 4     #how deep when walkign along row of bins
DROP_DEPTH = 5     #how deep when dropping a marker 

class BinsMission(MissionBase):

    def __init__(self):
        self.orienting = False
        self.centered_count = 0

    def init(self):
        self.entity_searcher.start_search([
            entities.LettersEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(0.3), sw3.SetDepth(2),sw3.RelativeYaw(0)
        ]))

        self.reference_angle = sw3.data.imu.yaw*(pi/180) % (2*pi)
        self.phase = 1
        self.state = 0
        self.centering_timeout = 0
        self.centered_counter = 0
        self.centering = False
        self.obstacle_angle = 0
        #be sure step always gets called
        self.set_entity_timeout(0)

    def step(self, entity_found):
        print "running vission code"
        if(not entity_found):
            #we don't see an entity this frame
            #but might still be tracking one
            if(self.centering):
                center_on_point(self.target.center)
                self.centering_timeout += 1
                if(self.centering_timeout < MISSION_TIMEOUT):
                    self.reset_mission()

        if(self.phase == 1):
        # --- PHASE ONE ---- 
        # the first time we see a bin, get on top of it 
        # if it is a target drop. 
        # afterwards, orient with the row of bins, and begin
        # walking down the row looking for the other target(s) 
            if(self.state == 0):
                #this is our first time seeing a bin
                print "Saw Our First Bin"

                #choose the closest bin 
                for i, a_bin in enumerate(entity_found.known_bins):
                    distance = math.sqrt(a_bin.center[0]**2+a_bin.center[1]**2)
                    if(not i or distance < min_distance):
                        min_distance = distance
                        self.target_id = a_bin.id 
                        self.target = a_bin

                #start centering on target bin
                center_on_point(self.target.center)
                self.centering = True

                #initialization finished
                self.state += 1

            elif(self.state == 1):
                #we are attempting to center on a target bin

                #determine if we see our target bin
                found_target = False
                for a_bin in enumerate(entity_found.known_bins):
                    if(a_bin.id == self.target_id):
                        print "Centering on a bin\n"
                        #we see our target bin, update centering algorithm
                        found_target = True
                        self.target = a_bin
                        centered = center_on_point(self.target.center)
                        #make a note if we are centered
                        if(centered < RADIAL_CENTERING_THRESHOLD):
                            self.centered_counter += 1
                        else:
                            self.centerd_counter = 0
                
                #handle timeout for this centering algorithm
                if(not found_target):
                    self.state_timeout += 1
                else:
                    self.state_timeout = 0
                if(self.state_timeout > INITIAL_CENTERING_TIMEOUT_THRESHOLD):
                    #reset the entire mission 
                    self.reset_mission()
                    print "RESTARTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

                if(self.centered_counter > CENTERED_COUNTER_THRESHOLD):
                    #we have successfully centered on our first bin
                    #record direction the bin is pointing
                    self.obstacle_angle = self.target.angle+sw3.data.imu.yaw*(pi/180) % (2*pi)

                    #descend to desired depth
                    sw3.nav.do(sw3.SetDepth(EXAM_HEIGHT))
                    
                    #proceed to the next state
                    self.state += 1    
                    
            elif(self.state == 2):
                #currently descending to EXAM_HEIGHT
                #continue to track target bin as reference
                found_target = False
                for a_bin in enumerate(entity_found.known_bins):
                    if(a_bin.id == self.target_id):
                        #we see our target bin, update centering algorithm
                        found_target = True
                        self.target = a_bin
                        centered = center_on_point(self.target.center)
                        #make a note if we are centered
                        if(centered < RADIAL_CENTERING_THRESHOLD):
                            self.centered_counter += 1
                        else:
                            self.centerd_counter = 0
                            
                #handle timeout                
                if(not found_target):
                    self.state_timeout += 1
                else:
                    self.state_timeout = 0
                if(self.state_timeout > INITIAL_DIVING_TIMEOUT_THRESHOLD):
                    #rise to previous depth, and revert a state 
                    sw3.nav.do(sw3.SetDepth(APPROACH_DEPTH))
                    self.state -= 1
                
                #test our depth
                depth_error = abs(sw3.data.depth - EXAM_DEPTH)  
                if(depth_error < DEPTH_ERROR_THRESHOLD):
                    depth_reached = True
                else:
                    depth_reached = False

                #if we are centered at depth, increment state
                if(depth_reached and self.centered_counter > CENTERED_COUNTER_THRESHOLD):
                    self.state += 1

            elif(self.state ==3):

                #check to see what kind of bin this is 
                if (self.target.type == BIN1 or self.target.type == BIN2 ):
                    #FIRE ZE MISSILES!!!
                    print "we should be dropping now"
                
                self.state += 1

            elif(self.state == 4):

                #compute and allign with our new target angle
                sw3.nav.do(sw3.SetYaw(self.obstacle_angle))
                
                
                self.phase = 2
                self.state = 0

        elif(self.phase == 2):
        # --- PHASE TWO ---- 
        # walk down the row of bins, looking for new bins
        # if we see a new bin, get on top of it
        # if we don't see a bin, reverse the robot
            
            if(self.state == 0):
                #we are moving forward, looking for a new bin

                #if it's been too long since we last saw a new bin,
                #start moving the robot the other direction

                #if we see a bin
                self.state = 1

            if(self.state == 1):
                #we are alligning with a bin

                #if it's too far away, get on top of it

                #if we are on top of it
                #drop the ball if this is a target
                #if we are out of balls
                    #self.phase = 3
                    #self.state = 0
                self.state = 2
            
            if(self.state == 2):
                #we are on top of a bin, 
                #allign ourselves to continue walkign down

                #if alligned
                self.state == 0

        elif(self.phase == 3):
            # --- PHASE THREE ---- 
            # we have dropped both markers 
            # celebrate with champagne 
            self.state == party 
    
    #reset the mission
    def reset_mission(self):
        #reset states
        self.phase = 0
        self.state = 0

        #resume navigating
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Yaw(self.reference_angle),sw3.Forward(0.4)
        ]))


def center_on_point(point):
    #calculate neccessary rotation of robot
    x = point[0]
    y = point[1]
    theta = math.atan2(x,y)*180/pi - 90
    distance = math.sqrt(x**2 + y**2)
    distance /= DISTANCE_CAP

    if(abs(theta) <= 90):
        direction = 1
    else:
        direction = -1
        theta += 180
        if(theta >= 180):
            theta -= 360

    #handle navigation
    if(distance > RADIAL_CENTERING_THRESHOLD):
        #we are far enough away for angular data to be sensible
        sw3.nav.do(sw3.RelativeYaw(theta))
    
    if(abs(theta) < ANGULAR_CENTERING_THRESHOLD):
        #we are pointed towards our target
        sw3.nav.do(sw3.Forward(0.4*direction*distance))

    return distance

