

from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3

FORWARD_SPEED = 0.3
DELAY = 2

class ReverseHedgeMission(MissionBase):

  #  def __init__(self):

    def init(self):
        sw3.nav.do(sw3.SetDepth(4))
        time.sleep(DELAY)
        self.process_manager.start_process(entities.HedgeYEntity, "hedge", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.Forward(FORWARD_SPEED),
            sw3.HoldYaw(),
        ))
        self.found = 0

    def step(self, vision_data):
        if not vision_data:
            return
        hedge_data = vision_data['hedge']

        if hedge_data and hedge_data.crossbar_depth is not None:
            hedge_center = None

            if hedge_data.right_pole is not None and hedge_data.left_pole is not None:
                hedge_center = (hedge_data.left_pole + hedge_data.right_pole) / 2  # degrees

            elif hedge_data.center_pole is not None:
                hedge_center = hedge_data.center_pole

            if hedge_center is not None:
                print "Correcting Yaw", hedge_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(hedge_center + 2),
                    sw3.Forward(FORWARD_SPEED)
                ]))
                self.found += 1

        elif not hedge_data and self.found >= 3:
            sw3.nav.do(sw3.SequentialRoutine(
                sw3.RelativeYaw(180),
                sw3.Forward(-1*FORWARD_SPEED, 5)
            ))
            self.finish_mission()
