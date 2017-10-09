
from __future__ import division
import sys
sys.path.append("/home/seawolf/acoustics/host_communication/seawolf")
import time

from vision import entities
from acoustics import Acoustics
from missions.base import MissionBase
import sw3
import math
from math import pi
from sw3 import util

import seawolf as sw

"""Robot will try to track pinger untill pitch array reads heading in behind of robot.
Prone to stopping when the robot is turned 90 degrees from the pinger.
"""

PORT_NAME = '/dev/ttyUSB3'
YAW_TOLERANCE = 10
ACOUSTICS_SAMPLING_INTERVAL = 5

# always try to record data from this test

# assume previous mission set a heading and a forward recon speed

# make sure any relative yaw adjustments are done for fresh pinger data

# if pitch array reads near 90  degrees, go a little fast

# if data goes stale, slow down

# use pitch array to say when the pinger is beneath the robot

# have discreet speeds for proximity to the pinger (slow, medium, fast)t

# TODO: timeout. not needed now because it the last thing we're doing at robosub 2016s




class AcousticsMission1(MissionBase):

    def init(self):
        '''runs at start of mission '''
        #self.process_manager.start_process(entities.PathEntity, "path", "forward", debug=True)
        self.acoustics = Acoustics()
        self.acoustics.connect(PORT_NAME)

        # enable logger
        self.acoustics.start_logger('acoustics1_{}'.format(time.time()))

        # pinger object variable
        self.ac_data = None

        # pinger tracking variables
        self.last_yaw_reading = None
        self.last_pitch_reading = None
        self.epoch = None
        self.ping_age = None
        
        self.listening = True

        # state variables
        self.ping_stale = True
        self.action = 'init'
        self.ping_used = False
        #['init','drive_to_pinger','no_ping','over_pinger']

    def stop(self):
        sw3.nav.do(sw3.Forward(0))
        self.finish_mission()

    def change_heading(self, forward, rel_yaw):
        if abs(rel_yaw) > YAW_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine(
                        sw3.RelativeYaw(-rel_yaw), 
                        sw3.Forward(forward)
                        )
                    )

    def listen_for_ping(self):

        self.ac_data = self.acoustics.get_data()

        if self.ac_data['error'] == 0:
            # check if ping received was pretty old
            self.ping_age = self.ac_data['data']['epoch']
            self.epoch = time.time() - self.ping_age
            #print "ping_age is {} (epoch = {})".format(self.ping_age, self.epoch)
            
            if self.ping_age > ACOUSTICS_SAMPLING_INTERVAL:
                print "hi"
                print "data is stale. will try again later"
                self.ping_stale = True
                self.ping_used = False # new ping. It likely hasn't been used yet.
                return None
            else:
                self.ping_stale = False

            

            # grab pinger information
            self.last_yaw_reading = self.ac_data['data']['heading']['ab']
            self.last_pitch_reading =   -self.ac_data['data']['heading']['cd']

            if self.ping_age < 2: 
                print "PING!!! yaw={}, pitch={}".format(self.last_yaw_reading,
                self.last_pitch_reading)

            
            return self.ac_data

        else:
            print "ERROR received"

        # if nothing happend, report no ping    
        return None

    def step(self, vision_data):
        #if not vision_data:
        #    return
        print "action = {}".format(self.action)
        if self.listening:
            self.listen_for_ping()

        
        if self.action == 'init':   
            if self.ping_stale:
                return
            else:
                self.change_heading( 0.0, self.last_yaw_reading)
                self.action = 'drive_to_pinger'

                # mark ping as used
                self.ping_used = False

        elif self.action == 'drive_to_pinger':
            if self.ping_stale or self.ping_used:
                return
            else:
                self.change_heading( 0.0, self.last_yaw_reading)
                self.ping_used = True
                
                #if self.last_pitch_reading < 10:
                #    self.stop()

    
