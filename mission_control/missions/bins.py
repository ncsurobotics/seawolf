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

BIN_DEPTH = 8
CENTER_THRESH = 6
FORWARD_SPEED = .5
CENTER_TIME = 5
BIN_TIMEOUT = 8
ORIENT_THRESH = 15
TURNING_TIME = 4
TURNAROUND_TIMER = 3

class BinsMission(MissionBase):

    def __init__(self):
        pass
    def init(self):
        #pooltest
        #self.process_manager.start_process(entities.BinsCornerEntity, "bins", "down", debug=True)
        #simulator
        self.process_manager.start_process(entities.BinsEntity, "bins", "down", debug=True)
        self.reference_angle = sw3.data.imu.yaw()
        self.highest_id = None

        self.turn_count = 1
        self.drop_count = 0
        self.dropped = "E"
        self.orientdata = None
        self.states = [
            "seek",
            "orient",
            "sweep",
            "drop",
            "findpath"
        ]
        self.state_num = 0
        self.state = self.states[self.state_num]
        self.x = 0
        self.y = 0
        self.set_timer("bins_timeout", 45, self.fail_mission)
        #sw3.nav.do(sw3.Forward(0,0))
    def step(self, vision_data):
        if vision_data is None:
            bins = None
            self.orientdata = None
        else:
            bins = vision_data['bins'].bins
            self.orientdata = vision_data['bins'].orientation
        
        if self.drop_count == 2:
            self.state_num = 4
            self.findpath()
        if self.state == "seek":
            self.seek(bins)
        if self.state == "orient":
            self.orient(bins)
        if self.state == "sweep":
            self.sweep(bins)
        if self.state == "drop":
            self.drop(bins)
        if self.state == "findpath":
            self.findpath()

    def seek(self, bins):
        #print "seek"
        #print bins
        if bins and self.orientdata:
            sw3.nav.do(sw3.Forward(0,1))
            #print bins
            pos_x = math.atan2(bins[0].theta,bins[0].phi)*(180/pi)
            print pos_x
            pos_rho = math.sqrt(bins[0].theta**2 + bins[0].phi**2)
           # sw3.nav.do(sw3.Forward(0,0))
            print "center"
            center = sw3.CompoundRoutine(sw3.RelativeYaw(pos_x), sw3.Forward(.2),sw3.SetDepth(BIN_DEPTH), timeout = 3)
            sw3.nav.do(center)
            #print pos_x
           # sw3.nav.do(sw3.Forward(FORWARD_SPEED, CENTER_TIME))
            #print "centering"
            #self.orientdata *= 180/math.pi
            if pos_x <= CENTER_THRESH:
                
                #print "centered"
                #orient_angle = self.orientdata
                sw3.nav.do(sw3.Forward(0,1))
                #sw3.nav.do(sw3.RelativeYaw(20))
                #sw3.nav.do(sw3.RelativeYaw(self.orientdata))
                #sw3.nav.do(sw3.RelativeDepth(BIN_DEPTH))
                self.nextState()
    #see 1? orient, move forward -- timeout if no 2nd buoy set yaw 180
    #see 2? center x, depth
    def orient(self, bins):
        if bins and self.orientdata:
            orient_angle = self.orientdata*(180/pi)
            #print "forward"
            #center = sw3.Forward(0.5,2)
            #centering =  sw3.nav.do(center)
            #sw3.nav.do(center)
            #sw3.nav.do(sw3.Forward(FORWARD_SPEED,1))
            #sw3.nav.do(sw3.Forward(0,0))
            print "orient"
            orient = sw3.CompoundRoutine(sw3.Forward(0,5),sw3.RelativeYaw(orient_angle))
            #sw3.nav.do(sw3.CompoundRoutine(sw3.Forward(0,0),(sw3.RelativeYaw(self.orientdata),timeout =5)))
            sw3.nav.do(orient)
            #orient.on_done(lambda z: sw3.nav.do(sw3.Forward(FORWARD_SPEED, 1)))
            #center.on_done(lambda b: sw3.nav.do(orient))
            #sw3.nav.do(sw3.RelativeDepth(BIN_DEPTH))
            #print sw3.data.imu.yaw() 
           # print self.orientdata
            if (abs(abs(sw3.data.imu.yaw()) - orient_angle) <= ORIENT_THRESH):
                print "done orienting"
                orient.on_done(lambda z: sw3.nav.do(sw3.Forward(FORWARD_SPEED, 1)))
                self.turn_count += 1
                self.nextState()
    def sweep(self, bins):
        #print "sweep"
        #print self.orientdata
        sweep = sw3.Forward(FORWARD_SPEED,1)
        turning = sw3.CompoundRoutine(sw3.Forward(0,TURNING_TIME), sw3.RelativeYaw(180))
        turnaround = lambda: sw3.nav.do(turning)
        #self.id_holder = self.highest_id
        #iif self.x == 0:
            #print "nav.sweep"
            #sw3.nav.do(sweep)
            #self.x = 1
        if bins:    
            for bincount in bins:
                if bincount.id > self.highest_id:
                    self.highest_id = bincount.id
        current_bin = None
        if self.orientdata is not None:
        #if self.highest_id > self.id_holder:
        #this means weve seen a new bini
            #print self.highest_id
            #print self.id_holder
            #self.id_holder = self.highest_id
            #sw3.nav.do(sw3.Forward(0,0))
            #sw3.nav.do(turning)
            print "turning"
            self.set_timer("bin_timeout",TURNAROUND_TIMER, turnaround )
            turning.on_done(lambda y: sw3.nav.do(sweep))
            #print "I turned!"
            #sw3.nav.do(sw3.Forward(FORWARD_SPEED))
           # print "turning"
            self.turn_count += 1
            #print self.turn_countF none
          
            for bina in bins:
                if bina.id == self.highest_id:
                    current_bin = bina
                    print current_bin.shape
                    #self.highest_id = bina.id
        if current_bin:
            if current_bin.shape is "A" or current_bin.shape is "C":
                if self.dropped is "A" and current_bin.shape is "C":
                    self.nextState()
                if self.dropped is "C" and current_bin.shape is "A":
                    self.nextState()
                if self.dropped is "E":
                    self.nextState()
                self.dropped = current_bin.shape
      # sw3.SequentialRoutine(sweep_routine, turnaround,sweep_routine)
        
    #move forward, order bins as we find, found/ordered 4 bins?
    def drop(self, bins):
        #print "Marker Dropped"
        if bins and self.orientdata:
            orient_angle = self.orientdata*(180/pi)
            print "orient"
            orient = sw3.CompoundRoutine(sw3.Forward(0),sw3.RelativeYaw(orient_angle), timeout = 5)
            sw3.nav.do(orient)


            self.drop_count += 1
            print "State:", self.state
            self.state = self.states[0]
            self.state_num = 0
        
   #move forward, bin below a target?, stop, drop.
    #repeat if markers dropped is not 2
    #find path if else
    def findpath(self):
        if self.turn_count % 2:
            sw3.nav.do(sw3.RelativeYaw(-90))
        else:
            sw3.nav.do(sw3.RelativeYaw(90))
        sw3.nav.do(sw3.Forward(.1, 2))
        self.finish_mission()
    def nextState(self):
        self.state_num += 1
        #if self.state_num >= len(self.states):
            #self.finish_mission()
        self.state = self.states[self.state_num]
        print "State:", self.state
       
