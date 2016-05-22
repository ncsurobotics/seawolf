from __future__ import division
from math import pi

import seawolf
from missions.base import MissionBase
from vision import entities
import sw3

BIN_DEPTH = 8
CENTER_THRESH = 6
FORWARD_SPEED = .3
CENTER_TIME = 5
BIN_TIMEOUT = 8
ORIENT_THRESH = 15
TURNING_TIME = 4
TURNAROUND_TIMER = 3


class NewBinsMission(MissionBase):

    def __init__(self):
        pass

    def init(self):
        import pdb; pdb.set_trace()
        self.process_manager.start_process(entities.BinsCornerEntity, "bins", "down", debug=True)
        self.reference_angle = sw3.data.imu.yaw()
        self.highest_id = None
        self.drop_count = 0
        self.dropped = "E"
        self.orientdata = None
        self.states = [
            "see4",
            "zoomin",
            "drop",
            "findpath"
        ]
        self.state_num = 0
        self.state = self.states[self.state_num]
        self.x = 0
        self.y = 0
        self.set_timer("new_bins_timeout", 45, self.fail_mission)
        # sw3.nav.do(sw3.Forward(0,0))

    def step(self, vision_data):
        if vision_data is None:
            bins = None
            self.orientdata = None
        else:
            bins = vision_data['bins'].bins
            self.orientdata = vision_data['bins'].orientation
        if self.state == "see4":
            self.see4(bins)
        if self.state == "zoomin":
            self.zoomin(bins)
        if self.state == "drop":
            self.drop(bins)
        if self.state == "findpath":
            self.findpath()

    def see4(self, bins):
        # make sure lined up with bin
        # complicated:
        #    raise depth until see two
        #    move so centered between
        #    raise depth?
        #    move perpendicular to first motion to see four
        # simple:
        #    raise depth
        #    if length of bins is 4, next state.
        if bins and self.orientdata:
            orient_angle = self.orientdata * (180 / pi)
            print "orienting"
            orient = sw3.CompoundRoutine(sw3.Forward(0, 5), sw3.RelativeYaw(orient_angle))
            sw3.nav.do(orient)
            if (abs(abs(sw3.data.imu.yaw()) - orient_angle) <= ORIENT_THRESH):
                print "done orienting"
                sw3.nav.do(sw3.Forward(1, 1))
                x = 1
                while(x < BIN_DEPTH):
                    sw3.nav.do(sw3.SetDepth(BIN_DEPTH - (x / 2)))
                    if len(bins) == 4:
                        sw3.nav.do(sw3.Forward(0, 0))
                        self.nextState()
                    x += 1
                print "too far up without seeing four bins. Help!"

    def zoomin(self, bins):
        # if can see letters from here, much easier
        # else choose one, go down (center?)
        #     check if right bin
        #     if not go back to see4
        #     else drop
        if bins:
            for bina in bins:
                if bina.id == "A" and self.dropped == "E":
                    self.dropped = "A"
                    break
                elif bina.id == "C" and self.dropped == "A":
                    self.dropped = "C"
                    break
            sw3.nav.do(sw3.setDepth(BIN_DEPTH))
            self.nextState()

    def drop(self, bins):
        seawolf.var.set("Servo1", 160)
        print "Marker Dropped"
        self.drop_count += 1
        if self.drop_count == 1:
            self.state_num = 0
        else:
            self.state_num = 3
        seawolf.var.set("Servo1", 20)
        self.state = self.states[self.state_num]
   # move forward, bin below a target?, stop, drop.
    # repeat if markers dropped is not 2
    # find path if else

    def findpath(self):
        sw3.nav.do(sw3.Forward(.1, 2))
        self.nextState()

    def nextState(self):
        self.state_num += 1
        if self.state_num > 3:
            self.finish_mission()
        self.state = self.states[self.state_num]
        print "State:" + self.state
