
from __future__ import division

from vision import entities
from missions.base import MissionBase
import time

import sw3

LEGACY = False

INITIAL_RECON_SPEED = -0.7
INIT_BACKUP_TIME = 10


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
BUMP_TIMEOUT = 2
BACKUP_TIME = 6


# TODO: depth control, check findpath, check if second buoy is center, testing for different buoy arrangements
class BuoyManager():
    def __init__(self):
        self.buoys = []

    def new_buoy(self,buoy):
        self.buoys.append(buoy)

    def get_buoy_list_l2r(self):
        if len(buoys) == 3:
            buoys.sort(key=lambda x: x.theta)
            

        

class BuoyMission(MissionBase):

    def __init__(self):
        # state machine variables
        self.state_num = -1
        self.current_state = 'collect_targets'
        self.prev_state = None
        self.next_state = None
        self.state_queue = []
        self.states = {}
        
        # orientation variables
        self.reference_angle = None

        # tracking variables
        self.bump_count = 0
        self.tracking_id = None
        self.depth_seen = None

        # buoy detection variables
        self.bm = BuoyManager()

    def init(self):
        '''runs at start of mission '''
        self.set_timer("mission_timeout", MISSION_TIMEOUT, self.mission_timeout)
        
        # start vision process
        self.process_manager.start_process(entities.BuoyHoughEntity, "buoy", "forward", debug=True)
        
        # ease backwards in order get a better view
        #sw3.nav.do(sw3.Forward(INITIAL_RECON_SPEED, INIT_BACKUP_TIME))
        #time.sleep(INIT_BACKUP_TIME)
        #sw3.nav.do(sw3.Forward(0, 5))
        
        # capture orientation at this point
        self.reference_angle = sw3.data.imu.yaw()

        #  Configure and run
        self.config_state_machine([
                                'approach',
                                'searching',
                                'bump_target',
                                'select_reference_buoy',
                                'select_target',
                                'restart',
                                'collect_targets',
                                'exit'])
        #self.run_buoys1()

        
        #self.current_state = self.state_queue[self.state_num]
        self.set_timer("buoy_timeout", 120, self.fail_mission)

    def run_buoys1(self):
        scan_rate = 0.1
        scan_time = 5
        

        self.next_state = self.states['searching']


        # run the buoy mission
        exit = False
        while exit==False:

            

            
                pass #do nothing

    def config_state_machine(self,state_list):
        self.state_num = 0

        if LEGACY:
            self.state_queue = [
                "first_approach",
                "bump",
                "second_approach",
                "bump",
                "center_approach",
                "findpath"
            ]
        else:
            # self.states['<state>'] = '<state>'
            self.states = {}
            for item in state_list:
                self.states[item] = item

    #TODO: add an exit state, and update everything.
    def next_state(self):
        self.state_num += 1
        if self.state_num >= len(self.state_queue):
            self.finish_mission()
        self.current_state = self.state_queue[self.state_num]
        print "State:", self.state

    def sweep_routine(self, approach_angle):
        return sw3.LoopRoutine(
            sw3.Forward(BACKWARD_SPEED, BACKUP_TIME),
            sw3.Forward(0, 2),
            sw3.SetYaw(self.reference_angle),
            #sw3.SetYaw(approach_angle),
        )

    def sweep_routine2(self):
        sw3.SequentialRoutine(
            sw3.Forward(BACKWARD_SPEED, BACKUP_TIME),
            sw3.Forward(0, 2),
            sw3.SetYaw(self.reference_angle))


    

    def mission_timeout(self):
        ''' mission has timed out, progress to next task'''
        # TODO fill this in with delicious cream
        print "BUOY TIMEOUT REACHED"

    def set_next_state(self,state):
        self.next_state = state
    
    def update_state(self):
        if self.next_state != None:
            self.prev_state = self.current_state
            self.current_state = self.next_state
        else:
            self.prev_state = self.current_state
            pass #don't change current state
    
    def step(self, vision_data):
        # Update vision data
        if vision_data is None:
            buoys = []
        else:
            buoys = vision_data['buoy'].buoys
            #print buoys

        
        
        # ###################
        # Collection
        # ############
        if self.current_state == self.states['collect_targets']:
      
            if self.prev_state != self.states['collect_targets']:
                self.set_timer("collection_timeout", 2, self.set_next_state, 'select_reference_buoy')

            if len(buoys)==3:
                self.delete_timer("collection_timeout")
                self.set_next_state('select_reference_buoy')

        # ###############
        # situation analysis and buoy pattern selection
        # #########
        elif self.current_state == self.states['select_reference_buoy']:
            # if full house
            if buoys is not None:
                buoys = self.bm.sort_by_confidence(buoys)
                confidence = buoys.confidence()
                colors = buoys.colors()

        elif self.current_state == self.states['searching']:
            pass

        elif self.current_state == self.states['select_target']:
            pass

        elif self.current_state == self.states['approach']:
            pass

        elif self.current_state == self.states['bump_target']:
            pass

        elif self.current_state == self.states['restart']:
            pass

        elif self.current_state == self.states['exit']:
            pass

        # update state
        self.update_state()
        """
        # TODO: What if only 2 buoys are visible? how do we proceed?

        if self.current_state == "first_approach":
            self.state_approach(BUOY_FIRST, buoys)
        if self.current_state == "second_approach":
            self.state_approach(BUOY_SECOND, buoys)
        if self.current_state == "center_approach":
            self.state_approach(1, buoys)
        if self.current_state == "bump":
            self.state_bump(buoys)
        if self.current_state == "findpath":
            self.state_findpath()"""

    def state_approach(self, buoy_to_bump, buoys):
        print("approach state: {} buoys detected".format(len(buoys)))
        # TODO: include depth routine
        if len(buoys) == 3:
            
            buoys.sort(key=lambda x: x.theta)
            self.tracking_id = buoys[buoy_to_bump].id

            if self.depth_seen is None:
                self.depth_seen = sw3.data.depth()


        # any available buoys represent the one we want to hit, track it 
        track_buoy = None
        for buoy in buoys:
            if buoy.id == self.tracking_id:
                track_buoy = buoy

        # if no hits on finding the target buoy, go back and try again.
        # mission will time out if this happens too much.
        if not track_buoy:
            return
            
        
        # print "State: BuoyBump  dist: ",track_buoy.r, " x angle from current: ",track_buoy.theta, " y angle from current: ", track_buoy.phi
        
        # various buoy related routines
        yaw_routine = sw3.RelativeYaw(track_buoy.theta)
        forward_routine = sw3.Forward(FORWARD_SPEED)
        stop_routine = sw3.Forward(0,0)
        backup_routine = sw3.Forward(BACKWARD_SPEED)
        reset_routine = sw3.SetYaw(self.reference_angle)

        #change Depth
        track_depth_angle = (track_buoy.phi)
        centered = False
        if abs(track_depth_angle) > DEPTH_THRESHOLD:
        
            if (track_depth_angle > 0):
                depth_routine = sw3.RelativeDepth(-DEPTH_UNIT)
                
            if (track_depth_angle < 0):
                depth_routine = sw3.RelativeDepth(DEPTH_UNIT)
        else:
            depth_routine = sw3.NullRoutine()
            centered = True

        # check if yaw is centered
        if abs(track_buoy.theta) <= CENTER_THRESHOLD:
            centered = True*centered

        # if yaw and depth are centered, advance to the next state!
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
            
        # otherwise, stop and adjust yaw
        else:
            sw3.nav.do(sw3.CompoundRoutine(
                stop_routine,
                yaw_routine
            ))

    def approach_timeout(self, approach_angle):
        self.next_state()
        '''state
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
            sw3.Forward(BACKWARD_SPEED, 10),
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
