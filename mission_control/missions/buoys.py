
from __future__ import division
from time import time

import entities
from missions.base import MissionBase
import sw3
import seawolf

DEGREE_PER_PIXEL = 0.03
SCALE_POWER = .3
DEPTH_PER_PIXEL = -1/50
INITIAL_FORWARD_SPEED = 0.2
TRACKING_FORWARD_SPEED = 0.4

INITIAL_DEPTH = 5.5
DEPTH_ERROR_MARGIN = 0.5 #how close to initial depth we must be before starting to correct from vision
MISSION_TIMEOUT = 27  # Total time after seeing first buoy we have to run the mission

class BuoysMission(MissionBase):

    def __init__(self):
        self.correct_buoy_index = None
        self.seen_count = 0
        self.first_seen = None
        self.initial_depth_achieved = False

    def init(self):
        self.entity_searcher.start_search([
            entities.BuoysEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(INITIAL_FORWARD_SPEED), sw3.SetDepth(INITIAL_DEPTH)
        ]))
        self.initial_angle = sw3.data.imu.yaw

    def step(self, entity_found):

        # Complete mission after we've seen it for MISSION_TIMEOUT seconds
        self.set_entity_timeout(0.1)
        #debug
        if self.first_seen:
            print "we have seen the buoys for ",time()-self.first_seen,"seconds"

        if self.first_seen and time() - self.first_seen > MISSION_TIMEOUT:
            return True

        # Don't run mission if we didn't see it
        elif not entity_found:
            return False

        # Check if this our first time seeing the buoys
        if self.correct_buoy_index is None:

            # Pick out buoy that is most centered
            center_most_location = entity_found.buoy_locations[0]
            self.correct_buoy_index = 0
            print entity_found.buoy_locations
            for i, location in enumerate(entity_found.buoy_locations):
                if abs(location.x) < center_most_location.x:
                    center_most_location = location
                    self.correct_buoy_index = i

            self.first_seen = time()

        # If center buoy was found, go towards it
        location = entity_found.buoy_locations[self.correct_buoy_index]

        # Start correcting depth after reached INITIAL_DEPTH
        if sw3.data.depth >= INITIAL_DEPTH - DEPTH_ERROR_MARGIN:
            self.initial_depth_achieved = True
            print "initial depth achieved"

        if location and time()-self.first_seen < MISSION_TIMEOUT:
            yaw_correction = location.x * DEGREE_PER_PIXEL
            if entity_found.buoy_scale:
                temp_scale = entity_found.buoy_scale
                temp_scale -= 1
                temp_scale *= SCALE_POWER
                temp_scale += 1
                temp_scale = max(0, temp_scale)
                temp_scale = min(1, temp_scale)

                yaw_correction *=  temp_scale
                print "temp_scale = ",temp_scale

            yaw_routine = sw3.RelativeYaw(yaw_correction)
            new_depth_heading = location.y * DEPTH_PER_PIXEL
            depth_routine = sw3.RelativeDepth(new_depth_heading)
            forward_routine = sw3.Forward(TRACKING_FORWARD_SPEED)
            if self.initial_depth_achieved:
                compound_routine = sw3.CompoundRoutine([
                    yaw_routine, depth_routine, forward_routine
                ])
            else:
                compound_routine = sw3.CompoundRoutine([
                    yaw_routine, forward_routine
                ])
            sw3.nav.do(compound_routine)

            print "Yaw relative:", yaw_correction

        return False
