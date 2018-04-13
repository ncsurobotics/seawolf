
from __future__ import division
import sys
sys.path.append("/home/seawolf/seawolf/mission_control/sw3")
from data import data
from vision import entities
from missions.base import MissionBase

import sw3, time

MISSION_TIMEOUT = 400
TIMEOUT_ENABLED = True
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = .9
SLOW_FORWARD_SPEED = 0.4

RECKON_TIME = 10
GATE_LOST_THRESHOLD = 30
DEPTH = 4
DELAY = 2

LEFT = 0
CENTER = 1
RIGHT = 2
FORWARD = 3
#in secconds
TIME_FORWARD = 3

class GateMission325(MissionBase):

    def __init__(self):
        self.gate_seen = 0
        self.gate_lost = 0
        self.mission_timeout = MISSION_TIMEOUT
       
		# new variables start - 3/25/17
        # states
        self.currentState = LEFT
        self.prevState = LEFT
        # scan degree
        self.degree = 15; # change me to modify scan range
        
        # keeps track of whether left/right/center routines were running
        self.wasLeftRunning = 0
        self.wasRightRunning = 0
        self.wasCenterRunning = 0
        self.wasForwardRunning = 0
		# new variables end - 3/25/17
        
    def init(self):
        # dive, but keep heading at same time
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.HoldYaw(),
            sw3.SetDepth(DEPTH)
        ))

        # give some time for the dive to complete
        time.sleep(DELAY)

        # start vision
        self.process_manager.start_process(entities.GateEntity, "gate", "forward", debug=True)

        # go forward
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.HoldYaw(),
            sw3.Forward(FORWARD_SPEED),
        ))
        
		# new variables start - 3/25/17
        # get our initial yaw
        self.initialYaw = data.imu.yaw()
        # is left pos or neg? assuming left is neg...
        self.targetYaw = self.initialYaw - self.degree
        self.startingYaw = self.initialYaw
        self.leftRelYaw = sw3.RelativeYaw(-self.degree)
        self.centerYaw = sw3.SetYaw(self.initialYaw)
        self.rightRelYaw = sw3.RelativeYaw(self.degree)
        self.goingForward = sw3.Forward(SLOW_FORWARD_SPEED, TIME_FORWARD)
		# new variables end - 3/25/17

    def step(self, vision_data):
        #print "timeout = {}".format(self.mission_timeout)
        print self.currentState
        if TIMEOUT_ENABLED:
            self.mission_timeout -= 1            
            
        if not vision_data:
            return
        gate_data = vision_data['gate']
        if not gate_data:
            return
        print gate_data
        
        if gate_data and gate_data.left_pole and gate_data.right_pole:
            gate_center = DEGREE_PER_PIXEL * (gate_data.left_pole + gate_data.right_pole) / 2  # degrees

            # If both poles are seen, point toward it then go forward.
            self.gate_seen += 1
            self.gate_lost = 0

            if abs(gate_center) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.Forward(FORWARD_SPEED),
                    sw3.HoldYaw()
                ]))
            else:
                print "Correcting Yaw", gate_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(gate_center),
                    sw3.Forward(SLOW_FORWARD_SPEED)
                ]))
        elif (self.gate_seen >= 15):
            self.gate_lost += 1
        elif self.currentState == LEFT :		#START MODIFIED CODE 3/25/17
            #assures seawolf not going forward.
            sw3.nav.do(sw3.Forward(0))
            if ((not self.leftRelYaw.is_running()) and self.wasLeftRunning == 0):
                sw3.nav.do(self.leftRelYaw)
                self.wasLeftRunning = 1
            elif ((not self.leftRelYaw.is_running()) and self.wasLeftRunning == 1):
                self.currentState = CENTER
                self.prevState = LEFT
                self.wasLeftRunning = 0
                self.leftRelYaw.reset()
        elif (self.currentState == CENTER):
            if ((not self.centerYaw.is_running()) and self.wasCenterRunning == 0):
                sw3.nav.do(self.centerYaw)
                self.wasCenterRunning = 1
            elif ((not self.centerYaw.is_running()) and self.wasCenterRunning == 1):
                if (self.prevState == LEFT):
                    self.currentState = RIGHT
                else:
                    self.currentState = FORWARD
                self.prevState = CENTER
                self.wasCenterRunning = 0
                self.centerYaw.reset()
        elif (self.currentState == RIGHT):
            if ((not self.rightRelYaw.is_running()) and self.wasRightRunning == 0):
                sw3.nav.do(self.rightRelYaw)
                self.wasRightRunning = 1
            elif ((not self.rightRelYaw.is_running()) and self.wasRightRunning == 1):
                self.currentState = CENTER
                self.prevState = RIGHT
                self.wasRightRunning = 0		# END MODIFIED CODE
                self.rightRelYaw.reset()
        elif (self.currentState == FORWARD):
            if ((not self.goingForward.is_running()) and self.wasForwardRunning == 0):
                sw3.nav.do(self.goingForward)
                self.wasForwardRunning = 1
            elif ((not self.goingForward.is_running()) and self.wasForwardRunning == 1):
                self.currentState = LEFT
                self.prevState = FORWARD
                self.wasForwardRunning = 0		# END MODIFIED CODE
                self.goingForward.reset()
              
        #print self.currentState
        if self.gate_lost > GATE_LOST_THRESHOLD or self.mission_timeout <= 0:
            print("Gate lost: %s , timeout: %s" % (self.gate_lost>5, self.mission_timeout <= 0))
            if self.mission_timeout <= 0:
                print "Gate Mission Timeout!"

            # we're done with gate. move forward for a bit, and move on
            print "going forward (dead reckoning)"
            sw3.nav.do(sw3.Forward(FORWARD_SPEED, RECKON_TIME))
            time.sleep(RECKON_TIME)

            print "Heading Locked"
            self.finish_mission()
            return
