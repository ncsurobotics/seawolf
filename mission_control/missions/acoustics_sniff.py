from __future__ import division
import sys
sys.path.append("/home/seawolf/software/acoustics/host_communication/seawolf/")
import time

from vision import entities
import acoustics_client
from missions.base import MissionBase
import sw3
import math
from math import pi
from sw3 import util

import seawolf as sw

PORT_NAME = '/dev/ttyUSB3'
YAW_TOLERANCE = 10
# acoustics 
EPOCH_STALE = 5 # time before a message goes stale
MAX_DATA_RATE = 5


DO_ROTATE_SEARCH = True




class AcousticsMission(MissionBase):

    def init(self):
        '''runs at start of mission '''
        #self.process_manager.start_process(entities.PathEntity, "path", "forward", debug=True)
        self.acoustics = acoustics_client.Acoustics()
        self.acoustics.connect(PORT_NAME)

        # acoustics data integrity parameters
        self.trusted_angle_range = 60
        self.basicly_zero_range = 20

        self.states = ['searching',
        'verify',
        'accepted',
        ]

        # setup ratelimiter
        self.rate_limiter = Rate_Limiter(msg_rate=5)
        
        

    def step(self, vision_data):
        #if not vision_data:

        # pick next state
        if self.state == 'searching':
            self.state_searching()
        elif self.state == 'verify':
            self.state_verify()
        elif self.state == 'accepted':
            self.state_accepted()
        elif not (self.state in self.states):
            raise ValueError("{} is not an acceptable state".format(self.state))


            if abs(rel_yaw) > YAW_TOLERANCE:
                # change yaw and go forward
                sw3.nav.do(
                    sw3.CompoundRoutine(
                        sw3.RelativeYaw(-rel_yaw), 
                        sw3.Forward(.3)
                        )
                    )

            time.sleep(6)
    def set_course(self, forward, rel_yaw, get_obj=False):
        """Changes the course of the robot as it's searching
        for the pinger.
        ARGS:
            forward: how fast to go forward
            rel_yaw: how much to change the relative yaw heading"""

        # change heading and move forward (or backward)
        if not get_obj:
            sw3.nav.do(sw3.CompoundRoutine(
                sw3.RelativeYaw(rel_yaw), 
                sw3.Forward(forward),
                )
            )

            return

        else:
            set_course_routine = sw3.CompoundRoutine(
                sw3.RelativeYaw(rel_yaw), 
                sw3.Forward(forward),
                )
            )

            # deliver an object to the caller
            return set_course_routine
        

    def get_acoustics_data(self):
        ac_data = self.acoustics.get_data()

        if ac_data['error'] == 0:
            self.epoch     = ac_data['data']['epoch']
            self.rel_yaw   = -ac_data['data']['heading']['ab']
            self.rel_pitch =  ac_data['data']['heading']['cd']

            if self.epoch > 5:
                print "data is stale. will try again later"
                return None

            # if data recieved, and no error present, return the data
            return ac_data

        else:
            return None

    
    def iterate_yaw_orientation(self):
        seawolf.nav.do(sw3.RelativeYaw(10))

    def state_searching(self):
        # get fresh acoustics data
        self.get_acoustics_data()

        # check if yaw heading is close to 0 degrees
        if (abs(self.rel_yaw) <= self.basicly_zero_range/2.0):
            self.set_state('verify')

        elif self.data_is_fresh():
            if (abs(self.rel_yaw) >= self.trusted_angle_range/2.0):
            #  rotate the robot, with a PID based constant slow turn
            self.iterate_yaw_orientation()

        else:
            # data is not fresh. do nothing until fresh data is aquired
            pass

        # 

    def set_state(self, substate):

    def state_verify(self):
        # get fresh acoustics data
        self.get_acoustics_data()


        # if pinger was inside range, trim the robot ~30 degrees.
        last_pinger_location = self.rel_yaw


class Rate_Limiter(self, msg_rate=None):
    def __init__(self):
        # waiting parameters
        self.timea = 0

        if msg_rate is None:
            self.msg_rate = None
            self.msg_interval = None
        else:
            self.change_msg_rate(msg_rate)

    def change_msg_rate(self, msg_rate):
        self.msg_rate = msg_rate
        self.msg_interval = 1.0/msg_rate

    def smart_wait(self, reset_when_done=True):
        timeb = time.time()
        
        exit_flg = False

        # block until wait is sufficient
        while exit_flg == False:
            if timeb >= self.timea + self.msg_interval:
                exit_flg = True
            else:
                continue
        
        # return after exit the wait loop
        return

        


        if reset_when_done:
            self.start_timer()

    def start_timer
        self.timea = time.time()

        