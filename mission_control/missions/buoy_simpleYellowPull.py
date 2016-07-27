
"""
Note:"""

from __future__ import division

from vision import entities
from missions.base import MissionBase
import time

import sw3

INITIAL_RECON_SPEED = -0.7
INIT_BACKUP_TIME = 10


MISSION_TIMEOUT = 120
FORWARD_SPEED = 0.8
BACKWARD_SPEED = -0.3
CENTER_TIME = 5



DEPTH_THRESHOLD = .05*5
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
BUMP_TIMEOUT = 2
BACKUP_TIME = 6

# TODO: depth control, check findpath, check if second buoy is center, testing for different buoy arrangements


class SimpleYellowPullBuoyMission(MissionBase):

    def __init__(self):
        # state machine variables
        self.state_num = -1
        self.state = None
        self.states = []
        
        self.bump_count = 0
        self.tracking_id = None
        self.depth_seen = None

    def init(self):
        '''runs at start of mission '''
        self.set_timer("mission_timeout", MISSION_TIMEOUT, self.mission_timeout)
        
        # start vision process
        self.process_manager.start_process(entities.BuoyHoughEntity, "buoy", "forward", debug=True)
        
        # ease backwards in order get a better view
        #sw3.nav.do(sw3.Forward(INITIAL_RECON_SPEED, INIT_BACKUP_TIME))
        #time.sleep(INIT_BACKUP_TIME)
        
        # capture orientation at this point
        self.reference_angle = sw3.data.imu.yaw()

        self.tracking_id = None
        self.depth_seen = None
        self.states = [
            "first_approach",
            "bump",
            #"second_approach", #ommited. we only want to bump the first buoy we see.
            #"bump",
            #"center_approach",
            "setup_pull_down",
            "wait",
            "pull_down",
            "wait",
            #"find_path",
            "disconnect",
            "wait",
            "find_path",
            "wait",

        ]
        
        self.state_num = 0
        self.state = self.states[self.state_num]
        self.set_timer("buoy_timeout", 120, self.fail_mission)

        # debug parameters
        self.i = 0

        # waiting variables
        self.substate = ''
        self.wait_stop_mark = -1
        self.hidden = False
        

    #TODO: code a class for buoy entities inside the mission itself
 
    def step(self, vision_data):
        """
        Buoy vision data will contain a list of buoy objects. Each buoy will have the
        following attributes:
          * color: determined color of the buoy.
          * id: numerical ID uniqely assigned to every discovered buoy
          * found: ???
          * phi: ???
          * theta: ???
        """
        if vision_data is None:
            buoys = []
        else:
            buoys = vision_data['buoy'].buoys
            #print buoys

        #print self.state
        # TODO: What if only 2 buoys are visible? how do we proceed?
        if self.state == "first_approach":
            self.state_approach(BUOY_FIRST, buoys)
        #if self.state == "second_approach":
        #    self.state_approach(BUOY_SECOND, buoys)
        if self.state == "bump":
            self.state_bump(buoys)
        #if self.state == "center_approach":
        #    self.state_approach(1, buoys)
        if self.state == "setup_pull_down":
            self.state_setup_pulldown()
        if self.state == "pull_down":
            #self.hidden = True
            self.state_pulldown()

        if self.state == "disconnect":
            self.state_disconnect()
        if self.state == "fly_over":
            self.state_fly_over()
        if self.state == "find_path":
            self.state_findpath()
        if self.state == "wait":
            self.state_wait_for_finish()
        if not (self.state in self.states):
            raise ValueError("State \"{}\" does not exist.".format(self.state))


    #TODO: add an exit state, and update everything.
    def next_state(self):
        """method for incrementing through the buoy mission sequence"""

        # increment state counter
        self.state_num += 1

        # if we're about to do the last state, end the mission!
        if self.state_num >= len(self.states):
            self.finish_mission()
            return

        # set new state
        self.state = self.states[self.state_num]
        print "State:", self.state

    def sweep_routine(self, approach_angle):
        return sw3.LoopRoutine(
            #sw3.Forward(BACKWARD_SPEED, BACKUP_TIME),
            sw3.Forward(0, 1),
            #sw3.SetYaw(self.reference_angle),
            sw3.SetRotate(0.3, 1),
            sw3.SetRotate(-0.3,2),
            sw3.SetYaw(approach_angle),
        )

    def mission_timeout(self):
        ''' mission has timed out, progress to next task'''
        # TODO fill this in with delicious cream
        print "BUOY TIMEOUT REACHED"

    def state_approach(self, buoy_to_bump, buoys):
        # self.tracking_id
        # if vision doesn't return any buoy objects, there's nothing to process.
        if not buoys:
            return
        # 
        print "buoy to bump: {}".format(buoy_to_bump)
        
        # TODO: include depth routine
        if len(buoys) >= 1:
            # Note: this is meant to create a pocket of code that only runs at 
            # the begginning of the approach phase. The assumption is that every
            # approach begins with 3 buoys in view. Once the sub moves forward, the
            # assumption is that this setup code ran enough times such that the
            # correct buoy is being tracked, and the optimal depth for seeing all
            # buoys simultaneously has been captured.
            
            # sort buoys from left to right
            buoys.sort(key=lambda x: x.theta)

            # store buoy-to-bump's ID under self.tracking_id for later recall
            self.tracking_id = buoys[buoy_to_bump].id

            # update depth parameter
            if self.depth_seen is None:
                self.depth_seen = sw3.data.depth()


        # assert that the tracked/target buoy is still in our field of view
        track_buoy = None
        for buoy in buoys:
            if buoy.id == self.tracking_id:
                track_buoy = buoy

        # if target buoy is not in our FOV, terminate processing and try again.
        # mission will time out if this happens too much.
        if not track_buoy:
            return
            
        # start/reset the approach timer
        self.set_timer("Approach_Timeout", APPROACH_TIMEOUT, self.approach_timeout, sw3.data.imu.yaw())
        
        # print debug text
        print("approach state: {} buoys detected".format(len(buoys)))
        # print "State: BuoyBump  dist: ",track_buoy.r, " x angle from current: ",track_buoy.theta, " y angle from current: ", track_buoy.phi
        
        # various buoy related routines
        yaw_routine = sw3.RelativeYaw(track_buoy.theta)
        forward_routine = sw3.Forward(FORWARD_SPEED)
        stop_routine = sw3.Forward(0,0)
        backup_routine = sw3.Forward(BACKWARD_SPEED)
        reset_routine = sw3.SetYaw(self.reference_angle)

        # generate Depth changing parameters
        track_depth_angle = (track_buoy.phi)
        centered = False
        #print (track_depth_angle)

        # dynamically assign depth_routine to trim depth by DEPTH_UNITs
        if abs(track_depth_angle) > DEPTH_THRESHOLD:
            if (track_depth_angle > 0):
                depth_routine = sw3.RelativeDepth(-DEPTH_UNIT)
                
            if (track_depth_angle < 0):
                depth_routine = sw3.RelativeDepth(DEPTH_UNIT)
        else:
            depth_routine = sw3.NullRoutine()
            centered = True


        
        # check if yaw is centered
        #print (track_buoy.theta)
        if abs(track_buoy.theta) <= CENTER_THRESHOLD:
            centered = True*centered

            
        # if yaw and depth are not centered, stop and adjust yaw/depth
        if not centered:
            sw3.nav.do(sw3.CompoundRoutine(
                stop_routine,
                yaw_routine,
                depth_routine
            ))
            
        # else yaw and depth are centered, advance to the next state!
        else:
            sw3.nav.do(sw3.CompoundRoutine(
                forward_routine,
                yaw_routine,
                depth_routine
            ))
            self.delete_timer("Approach_Timeout")
            self.next_state()

    def approach_timeout(self, approach_angle):
        self.next_state()
        '''state
        sw3.nav.do(sw3.SequentialRoutine(
            sw3.Forward(BACKWARD_SPEED, 5),
            self.sweep_routine(approach_angle)
            ))
        '''

    def state_bump(self, buoys):
        """assumes forward movement from the previous state."""

        track_buoy = self.get_live_target_buoy(self.tracking_id, buoys)

        # if tracked buoy was not found, terminate processing and try again
        if not track_buoy:
            return

        # TODO add smarter timeout
        # if tracked buoy was found, reset the Bump_Timeout routine.
        # timeout routine is meant to ensure that vehicle reverses while bumping the buoy,
        # but keeps yaw orientation constant the entire time.
        self.set_timer("Bump_Timeout", BUMP_TIMEOUT, self.bump_timeout, sw3.data.imu.yaw())

    def get_live_target_buoy(self, target_id, buoys):
        tracked_buoy = None

        # search live buoys for the target one
        for buoy in buoys:
            if buoy.id == target_id:
                tracked_buoy = buoy

        # return (live) tracked buoy if found, or return None
        if tracked_buoy:
            return tracked_buoy
        else: 
            return None
    
    def bump_timeout(self, approach_angle):
        ##sw3.nav.do(sw3.SequentialRoutine(
            #sw3.Forward(BACKWARD_SPEED, 10),
            #self.sweep_routine(approach_angle)
          ##  ))
        self.next_state()

    # after bumping buoys go over center buoy and end mission, the next mission is to find path with bottom camera
    def state_findpath(self):
        sw3.nav.do(sw3.Forward(0))

        # TODO: check if the second buoy was center, if so, dont do another approach
        riseup_routine = sw3.RelativeDepth(OVER_DEPTH)
        runover_routine = sw3.Forward(FORWARD_SPEED)
        stop_routine = sw3.Forward(0)
        depth_goto = sw3.SetDepth(self.depth_seen)
        print "findpath"
        sw3.nav.do(sw3.SequentialRoutine(
            sw3.Forward(-0.6,0.1),
            riseup_routine,
            sw3.SetYaw(self.reference_angle),
            runover_routine
        ))
        self.wait_stop_mark = 3
        

        self.next_state()

    def change_substate(self, new_state):
        self.substate = new_state
    
    def state_setup_pulldown(self):
        # start: buoy has dissappeard b/c we're so close to it
        # ###
        sw3.nav.do(sw3.SequentialRoutine(
            sw3.Forward(-0.7, 1),
            sw3.Forward(0,0.1),
            sw3.RelativeDepth(-2),
            sw3.Forward(0.7,1*1.5),
            sw3.Forward(0,0.1)
        ))
        self.wait_stop_mark = 4
        self.next_state()

    def state_pulldown(self):
        sw3.nav.do(sw3.SequentialRoutine( 
            sw3.Forward(0.7, 0.2),
            sw3.DepthRate(1,1),
            sw3.RelativeDepth(2),
            sw3.Forward(0, 0.01)
        ))
        self.wait_stop_mark = 3
        self.next_state()

    def state_disconnect(self):
        sw3.nav.do(sw3.SequentialRoutine(
            sw3.Forward(-0.5,3),
            sw3.NullRoutine(),
        ))
        self.wait_stop_mark = 1
        self.next_state()
    
    def state_wait_for_finish(self):
        """eat vision messages while waiting for buoy mission to
        finish up"""

        current_routine = sw3.nav.current_routine.routine_counter
        #print "hey I'm{}. Looking for{}".format(current_routine, self.wait_stop_mark)
        #print 'waiting'
        
        if current_routine >= self.wait_stop_mark:
            self.next_state()

        