
from __future__ import division
from time import time

import entities
from missions.base import MissionBase
import sw3
import seawolf

DEGREE_PER_PIXEL = 0.1
DEPTH_PER_PIXEL = -1/50
INITIAL_FORWARD_SPEED = 0.2
TRACKING_FORWARD_SPEED = 0.4
MISSION_TIMEOUT = 16

class BuoysMission(MissionBase):

    def __init__(self):
        self.correct_buoy_index = None
        self.seen_count = 0
        self.first_seen = None

    def init(self):
        self.entity_searcher.start_search([
            entities.BuoysEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(INITIAL_FORWARD_SPEED), sw3.SetDepth(6)
        ]))
        self.initial_angle = sw3.data.imu.yaw

    def step(self, entity_found):

        # Complete mission if timeout has passed
        if not entity_found:
            sw3.nav.do(sw3.Forward(0.8))
            return True

        # Check if this our first time seeing the buoys
        if self.correct_buoy_index is None:

            # Pick out buoy that is most centered
            center_most_location = entity_found.buoy_locations[0]
            self.correct_buoy_index = 0
            for i, location in enumerate(entity_found.buoy_locations):
                if abs(location.x) < center_most_location.x:
                    center_most_location = location
                    self.correct_buoy_index = i

            self.first_seen = time()
            self.set_entity_timeout(MISSION_TIMEOUT)

        # If center buoy was found, go towards it
        location = entity_found.buoy_locations[self.correct_buoy_index]

        if location and time()-self.first_seen < 15:
            yaw_routine = sw3.RelativeYaw(location.x * DEGREE_PER_PIXEL)
            new_depth_heading = location.y * DEPTH_PER_PIXEL
            depth_routine = sw3.RelativeDepth(new_depth_heading)
            forward_routine = sw3.Forward(TRACKING_FORWARD_SPEED)
            compound_routine = sw3.CompoundRoutine([
                yaw_routine, depth_routine, forward_routine
            ])
            sw3.nav.do(compound_routine)

            print "Yaw relative:", location.x * DEGREE_PER_PIXEL

