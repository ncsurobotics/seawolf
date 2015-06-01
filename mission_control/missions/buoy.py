
from __future__ import division

from vision import entities
from missions.base import MissionBase
from vision import process_manager
import sw3
import math
from sw3 import util

MISSION_TIMEOUT = 10
FORWARD_SPEED = 0.3
BACKWARD_SPEED = -0.3
CENTER_TIME = 5

DEPTH_THRESHOLD = .05
DEPTH_UNIT = 0.2

CAM_FRAME_X_MIN = 0
CAM_FRAME_X_MAX = 0

CAM_FRAME_Y_MIN = 0
CAM_FRAME_Y_MAX = 0


BUOY_FIRST = 0  # first buoy to bump(0 is left, 1 is center, 2 is right)
BUOY_SECOND = 2  # second buoy to bump

BUMP_TIME = 5  # time to move forward in bump routine
OVER_DEPTH = -4  # depth to pass over the center buoy
RUNOVER_TIME = 8
DIST_THRESHOLD = 7
CENTER_THRESHOLD = 2
APPROACH_TIMEOUT = 6
BUMP_TIMEOUT = 7
BACKUP_TIME = 6

# TODO: depth control, check findpath, check if second buoy is center, testing for different buoy arrangements


class BuoyMission(MissionBase):

    def __init__(self):
        self.bump_count = 0

    def init(self):
        '''runs at start of mission '''
        self.set_timer("mission_timeout", MISSION_TIMEOUT, self.mission_timeout)
        self.process_manager.start_process(entities.BuoyTestEntity, "buoy", "forward", debug=True)
        sw3.nav.do(sw3.Forward(FORWARD_SPEED, 5))

        #self.reference_angle = sw3.data.imu.yaw()*(pi/180) % (2*pi)
        self.reference_angle = sw3.data.imu.yaw()

        self.tracking_id = None

        self.depth_seen = None

        self.states = [
            "first_approach",
            "bump",
            "second_approach",
            "bump",
            "center_approach",
            "findpath"
        ]
        self.state_num = 0
        self.state = self.states[self.state_num]
        self.set_timer("buoy_timeout", 120, self.fail_mission)

    def next_state(self):
        self.state_num += 1
        if self.state_num >= len(self.states):
            self.finish_mission()
        self.state = self.states[self.state_num]
        print "State:", self.state

    def sweep_routine(self, approach_angle):
        return sw3.LoopRoutine(
            sw3.Forward(BACKWARD_SPEED, BACKUP_TIME),
            sw3.Forward(0, 2),
            sw3.SetYaw(self.reference_angle),
            sw3.SetYaw(approach_angle),
        )

    def mission_timeout(self):
        ''' mission has timed out, progress to next task'''
        # TODO fill this in with delicious cream
        print "BUOY TIMEOUT REACHED"

    def step(self, vision_data):

        if vision_data is None:
            buoys = []
        else:
            buoys = vision_data['buoy'].buoys

        if self.state == "first_approach":
            self.state_approach(BUOY_FIRST, buoys)
        if self.state == "second_approach":
            self.state_approach(BUOY_SECOND, buoys)
        if self.state == "center_approach":
            self.state_approach(1, buoys)
        if self.state == "bump":
            self.state_bump(buoys)
        if self.state == "findpath":
            self.state_findpath()

    def state_approach(self, buoy_to_bump, buoys):
        # TODO: include depth routine
        if len(buoys) == 3:
            buoys.sort(key=lambda x: x.theta)
            self.tracking_id = buoys[buoy_to_bump].id

            if self.depth_seen is None:
                self.depth_seen = sw3.data.depth()

        track_buoy = None
        for buoy in buoys:
            if buoy.id == self.tracking_id:
                track_buoy = buoy

        if not track_buoy:
            return
        #self.set_timer("Approach_Timeout", APPROACH_TIMEOUT, self.approach_timeout, sw3.data.imu.yaw())
        # print "State: BuoyBump  dist: ",track_buoy.r, " x angle from current: ",track_buoy.theta, " y angle from current: ", track_buoy.phi
        yaw_routine = sw3.RelativeYaw(track_buoy.theta)
        forward_routine = sw3.Forward(FORWARD_SPEED)
        stop_routine = sw3.Forward(0, 0)
        backup_routine = sw3.Forward(BACKWARD_SPEED)
        reset_routine = sw3.SetYaw(self.reference_angle)

        track_depth_angle = (track_buoy.phi)
        if abs(track_depth_angle) > DEPTH_THRESHOLD:
            if (track_depth_angle > 0):
                depth_routine = sw3.RelativeDepth(-DEPTH_UNIT)
            if (track_depth_angle < 0):
                depth_routine = sw3.RelativeDepth(DEPTH_UNIT)

        else:
            depth_routine = sw3.NullRoutine()

        centered = False
        if abs(track_buoy.theta) <= CENTER_THRESHOLD:
            centered = True

        if centered:
            sw3.nav.do(sw3.CompoundRoutine(
                forward_routine,
                yaw_routine,
                depth_routine
            ))
            '''
            if abs(track_buoy.r) <= DIST_THRESHOLD:
                self.delete_timer("Approach_Timeout")
                self.next_state()
            '''
            self.next_state()
        else:
            sw3.nav.do(sw3.CompoundRoutine(
                stop_routine,
                yaw_routine
            ))

    def approach_timeout(self, approach_angle):
        self.next_state()
        '''
        sw3.nav.do(sw3.SequentialRoutine(
            sw3.Forward(BACKWARD_SPEED, 5),
            self.sweep_routine(approach_angle)
            ))
        '''

    def state_bump(self, buoys):
        track_buoy = None
        for buoy in buoys:
            if buoy.id == self.tracking_id:
                track_buoy = buoy

        if not track_buoy:
            return

        # TODO add smarter timeout
        self.set_timer("Bump_Timeout", BUMP_TIMEOUT, self.bump_timeout, sw3.data.imu.yaw())

    def bump_timeout(self, approach_angle):
        sw3.nav.do(sw3.SequentialRoutine(
            sw3.Forward(BACKWARD_SPEED, 5),
            self.sweep_routine(approach_angle)
        ))
        self.next_state()

    # after bumping buoys go over center buoy and end mission, the next mission is to find path with bottom camera
    def state_findpath(self):
        # TODO: check if the second buoy was center, if so, dont do another approach
        riseup_routine = sw3.RelativeDepth(OVER_DEPTH)
        runover_routine = sw3.Forward(FORWARD_SPEED)
        stop_routine = sw3.Forward(0)
        depth_goto = sw3.SetDepth(self.depth_seen)
        print "findpath"
        sw3.nav.do(sw3.SequentialRoutine(
            depth_goto,
            riseup_routine,
            runover_routine
        ))

        self.finish_mission()
