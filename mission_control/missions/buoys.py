
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

DEGREE_PER_PIXEL = 0.19
FORWARD_SPEED = 0.6

class BuoysMission(MissionBase):

    def __init__(self):
        self.correct_buoy_index = None

    def init(self):
        self.entity_searcher.start_search([
            entities.BuoysEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(FORWARD_SPEED), sw3.SetDepth(2)
        ]))
        self.initial_angle = sw3.data.imu.yaw

    def step(self, entity_found):

        if self.correct_buoy_index is None:

            # Pick out buoy that is most centered
            center_most_location = entity_found.buoy_locations[0]
            self.correct_buoy_index = 0
            for i, location in enumerate(entity_found.buoy_locations):
                if abs(location.x) < center_most_location.x:
                    center_most_location = location
                    self.correct_buoy_index = i

        location = entity_found.buoy_locations[self.correct_buoy_index]
        if location:
            sw3.nav.do(sw3.CompoundRoutine([
                sw3.RelativeYaw(location.x * DEGREE_PER_PIXEL),
                sw3.Forward(0.3)
            ]))
