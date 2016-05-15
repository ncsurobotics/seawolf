

from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3, time


MISSION_TIMEOUT = 500
DEGREE_PER_PIXEL = 0.10
FORWARD_SPEED = 0.3
DELAY = 2
DEPTH = 4

class ReverseHedgeMission(MissionBase):

    def __init__(self):
        self.hedge_seen = 0
        self.hedge_lost = 0
        self.mission_timeout = MISSION_TIMEOUT

    def init(self):
        sw3.nav.do(sw3.SetDepth(DEPTH))
        time.sleep(DELAY)
        self.process_manager.start_process(entities.HedgeEntity, "hedge", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.Forward(FORWARD_SPEED),
            sw3.HoldYaw(),
        ))

    def step(self, vision_data):
        self.mission_timeout -= 1
        if not vision_data:
            return
        hedge_data = vision_data['hedge']
        if not hedge_data:
            return

        print hedge_data

        if hedge_data:
            hedge_center = None
            if hedge_data.right_pole and hedge_data.left_pole:
                hedge_center = DEGREE_PER_PIXEL * (hedge_data.left_pole + hedge_data.right_pole) / 2  # degrees

            elif hedge_data.center_pole is not None:
                hedge_center = hedge_data.center_pole

            self.hedge_seen += 1
            self.hedge_lost = 0

            if hedge_center is not None:
                if abs(gate_center) < STRAIGHT_TOLERANCE:
                    sw3.nav.do(sw3.CompoundRoutine([
                        sw3.Forward(FORWARD_SPEED),
                        sw3.HoldYaw()
                    ]))
                else:
                    print "Correcting Yaw", hedge_center
                    sw3.nav.do(sw3.CompoundRoutine([
                        sw3.RelativeYaw(hedge_center + 2),
                        sw3.Forward(FORWARD_SPEED),
                    ]))
        elif self.hedge_seen >= 5:
            self.hedge_lost += 1

        if self.hedge_lost > 1 or self.mission_timeout <= 0:
            sw3.nav.do(sw3.SequentialRoutine(
                sw3.RelativeYaw(180),
                sw3.Forward(-1*FORWARD_SPEED, 5)
            ))
            time.sleep(self.mission_timeout)
            self.finish_mission()
