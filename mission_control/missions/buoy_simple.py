
from __future__ import division
from time import time

from vision import entities
from missions.base import MissionBase
from vision import process_manager
import sw3
import seawolf as sw

import svr

FORWARD_SPEED = 0.6
BUOY_CENTER_THRESHOLD = 5
DEPTH_BUMP= 3

class SimpleBuoyMission(MissionBase):

    def init(self):
        self.process_manager.start_process(entities.BuoyTestEntity,"buoy", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.Forward(FORWARD_SPEED),
            sw3.SetDepth(DEPTH_BUMP),
            sw3.HoldYaw(),
        ))
        self.start_angle = sw.var.get("YawPID.Heading")
        self.set_timer("mission_timeout", 15, self.finish_mission)

        self.tracking_buoy_id = None  # State variable for bump_buoy()

    def step(self, vision_data):
        if not vision_data:
            return
        buoys = vision_data['buoy'].buoys
        print buoys
        if self.bump_buoy(buoys):
            self.finish_mission()

    def bump_buoy(self, buoys, depth=None):


        # Check if we saw all 3 buoys
        # found_buoys = filter(lambda x: x.found, buoys)
        found_buoys = buoys
        
        if found_buoys:
            found_buoys.sort(key=lambda x: x.theta)

        if len(found_buoys) == 3:
            print "found 3 buoys"
            # Assign tracking_buoy_id to middle buoy
            self.tracking_buoy_id = found_buoys[1].id
        
        """
        elif found_buoys:
            for buoy in found_buoys:
                absolute_theta = buoy.theta + sw3.data.imu.yaw()
                buoy.center_distance = sw3.util.circular_distance(absolute_theta, self.start_angle, 180, -180)
            found_buoys.sort(key=lambda x: x.center_distance)
            if found_buoys[0].center_distance < BUOY_CENTER_THRESHOLD:
                self.tracking_buoy_id = found_buoys[0].id
        """

#what does this conditional do?
        if self.tracking_buoy_id != None:

            self.delete_timer("mission_timeout")

            # Get tracking buoy from its id
            tracking_buoy = None
            for buoy in buoys:
                if buoy.id == self.tracking_buoy_id:
                    tracking_buoy = buoy

            # Correct if we saw it
            if tracking_buoy:
                print tracking_buoy.phi
                self.last_seen = time()
                if depth:
                    depth_routine = sw3.SetDepth(depth)
                else:
                    depth_routine = sw3.RelativeDepth(-(tracking_buoy.phi)/5)
                    print "Adjusting depth:", -tracking_buoy.phi/5
                print "Adjusting Yaw:", tracking_buoy.theta
                sw3.nav.do(sw3.CompoundRoutine(
                    depth_routine,
                    sw3.Forward(FORWARD_SPEED),
                    sw3.RelativeYaw(tracking_buoy.theta),
                ))

            # Consider ending the mission if we didn't see it
            elif time() - self.last_seen > 10:
                self.tracking_buoy_id = None
                print "Lost buoy, finishing"
                return True

