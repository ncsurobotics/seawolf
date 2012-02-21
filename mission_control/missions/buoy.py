
from __future__ import division

from vision import entities
from missions.base import MissionBase
from vision import process_manager
import sw3
import math
from math import pi
from sw3 import util

MISSION_TIMEOUT = 5
FORWARD_SPEED = 0.5

CENTER_TIME = 5

BUOY_FIRST = 1 #first buoy to bump(1 is left, 2 is center, 3 is right)
BUOY_SECOND = 3 #second buoy to bump
BUMP_TIME = 5 #time to move forward in bump routine
OVER_DEPTH = 3 #depth to pass over the center buoy
RUNOVER_TIME = 8 #
DIST_THRESHOLD = 5
CENTER_THRESHOLD = 2

class BuoyMission(MissionBase):

    def __init__(self):
        print "__init__"
        self.bump_count = 0
        self.pointing_to = False
    def init(self):
        print "BuoyMission: initializing "
        '''runs at start of mission '''
        self.process_manager.start_process(entities.BuoyEntity, "buoy", "forward", debug=True)
        sw3.nav.do(sw3.Forward(FORWARD_SPEED,5))

        self.reference_angle = sw3.data.imu.yaw()*(pi/180) % (2*pi)

        self.tracking_id = None
        self.state = "centering"
    def step(self, vision_data):

        if vision_data == None:
            return

        buoy_data = vision_data['buoy'].buoys
        print buoy_data


        if self.state == "centering":
            self.state_centering(buoy_data)
        if self.state == "bump_buoy":
            self.state_bump_buoy(buoy_data)
        if self.state == "stepto":
            self.state_stepto(buoy_data)
        if self.state == "findpath":
            self.state_findpath()

    def state_centering(self,buoy_data):
        if self.tracking_id == None:
            if len(buoy) == 3:
                bouy.sort(lambda x: x.theta)
                self.tracking_id = buoy[1].id
        if self.tracking_id != None:
            track_buoy = None
            for buoy in buoys:
                if buoy.id == self.tracking_id:
                    track_buoy = buoy

        if not track_buoy:
            return

        print "State: Centering  dist: ",track_buoy.r," x angle from current: ",track_buoy.theta, " y angle from current: ",track_buoy.phi

        sw3.nav.do(sw3.Forward(0))
        yaw_routine = sw3.RelativeYaw(track_buoy.theta)
        sw3.nav.do(yaw_routine)

        forward_routine = sw3.Forward(FORWARD_SPEED, CENTER_TIME)
        #yaw_routine.on_done(forward_routine)

        if track_buoy.theta <= CENTER_THRESHOLD:
            self.state = "bump_buoy"

    def state_bump_buoy(self,buoy_data):
        print "State: BuoyBump bumpcount: ",self.bump_count
        if len(buoy_data)==3:
            buoy_data.sort(lambda x: x.theta)
            if self.bump_count == 0:
                self.tracking_id = buoy_data[FIRST_BUOY].id
            if self.bump_count == 1:
                self.tracking_id = buoy_data[SECOND_BUOY].id

        track_buoy = None
        for buoy in buoy_data:
            if buoy.id ==self.tracking_id:
                track_buoy = buoy

        if not track_buoy:
            return

        print "State: BuoyBump  dist: ",track_buoy.r, " x angle from current: ",track_buoy.theta, " y angle from current: ", track_buoy.phi
        yaw_routine = sw3.RelativeYaw(track_buoy.theta)
        forward_routine = sw3.Forward(FORWARD_SPEED,CENTER_TIME)
        bump_routine = sw3.Forward(FORWARD_SPEED,BUMP_TIME)
        stop_routine = sw3.Forward(0,0)
        backup_routine = sw3.Forward(BACKWARD_SPEED,BUMP_TIME)
        reset_routine = sw3.SetYaw(self.reference_angle)


        if abs(track_buoy.theta) <= CENTER_THRESHOLD:
            self.pointing_to = True

        if self.pointing_to:
            sw3.nav.do(SequentialRoutine(
                    forward_routine,
                    stop_routine
                    ))
           
        else:
           sw3.nav.do(CompoundRoutine(
                stop_routine,
                yaw_routine
                ))
       
        if abs(track_buoy.r) <= DIST_THRESHOLD:
            sw3.nav.do(SequentialRoutine(
                bump_routine,
                backup_routine,
                stop_routine,
                reset_routine,
                stop_routine
                ))
            self.state = "stepto"



    #after bumping buoys go over center buoy and end mission, the next mission is to find path with bottom camera
    def state_findpath(self):
        riseup_routine = sw3.SetDepth(OVER_DEPTH)
        runover_routine = sw3.Forward(FORWARD_SPEED)
        stop_routine = sw3.Forward(0)

        sw3.nav.do(SequentialRoutine(
            riseup_routine,
            runover_routine
            ))
    #use to increment the buoy bump counter 1
    def state_stepto(self):
        self.bump_count += 1

        if self.bump_count == 1:
            self.state = "centering"

        elif self.bump_count == 2:
            self.state = "findpath"

