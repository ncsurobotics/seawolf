

from __future__ import division

from vision import entities
from missions.base import MissionBase
from vision import process_manager
import sw3

MISSION_TIMEOUT = 3
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.4
DEPTH_OVERBAR = 2

class HedgeMission(MissionBase):

  #  def __init__(self):

    def init(self):
        self.process_manager.start_process(entities.HedgeEntity, "hedge", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.Forward(FORWARD_SPEED),
            sw3.HoldYaw()
        ))

    def step(self, vision_data):
        if not vision_data: return
        hedge_data = vision_data['hedge']
        
        print hedge_data
        current_depth = sw3.data.depth()

     #   desired_depth = current_depth + hedge_data.crossbar_depth - DEPTH_OVERBAR
        
        if hedge_data and hedge_data.left_pole and hedge_data.right_pole:
            hedge_center = (hedge_data.left_pole + hedge_data.right_pole)/2  # degrees
            desired_depth = current_depth + hedge_data.crossbar_depth - DEPTH_OVERBAR
            # If both poles are seen, point toward it then go forward.
            self.set_entity_timeout(MISSION_TIMEOUT)
            


            if abs(hedge_center) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.Forward(FORWARD_SPEED),
                    sw3.HoldYaw(),#TODO:check if holdyaw is right
                    sw3.SetDepth(desired_depth)
                ]))
               # if self.hedge_seen > 10:
                #    print "Heading Locked"
                 #   self.finish_mission()
                 #   return
            else:
                print "Correcting Yaw", hedge_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(hedge_center),
                    sw3.Forward(0.4)
                ]))
