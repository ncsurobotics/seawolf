

from __future__ import division

from vision import entities
from missions.base import MissionBase
from vision import process_manager
import sw3

MISSION_TIMEOUT = 3
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.3
DEPTH_OVERBAR = 3

class HedgeMission(MissionBase):

  #  def __init__(self):

    def init(self):
        self.process_manager.start_process(entities.HedgeEntity, "hedge", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.Forward(FORWARD_SPEED),
            #sw3.SetDepth(5.0),
            sw3.HoldYaw(),
        ))
        self.set_timer("hedge_timeout", 45, self.finish_mission)

    def step(self, vision_data):
        if not vision_data: return
        hedge_data = vision_data['hedge']
        
        print hedge_data
        current_depth = sw3.data.depth()

        #desired_depth = current_depth + hedge_data.crossbar_depth - DEPTH_OVERBAR
        
        if hedge_data and hedge_data.crossbar_depth is not None:

            if hedge_data.right_pole is not None and hedge_data.left_pole is not None:
                hedge_center = (hedge_data.left_pole + hedge_data.right_pole)/2  # degrees

            elif hedge_data.center_pole is not None:
                hedge_center = hedge_data.center_pole

            desired_depth = current_depth + hedge_data.crossbar_depth - DEPTH_OVERBAR
            # If both poles are seen, point toward it then go forward.
            self.set_timer("mission_timeout", 3, self.finish_mission)

            print "Correcting Yaw", hedge_center
            sw3.nav.do(sw3.CompoundRoutine([
                sw3.RelativeYaw(hedge_center+2),
                sw3.Forward(FORWARD_SPEED),
                sw3.SetDepth(desired_depth)
            ]))
