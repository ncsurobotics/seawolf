
from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3, time

MISSION_TIMEOUT = 400
TIMEOUT_ENABLED = False
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = .9
SLOW_FORWARD_SPEED = 0.4

RECKON_TIME = 10
GATE_LOST_THRESHOLD = 30
DEPTH = 4
DELAY = 2

class GateMission(MissionBase):

    def __init__(self):
        self.gate_seen = 0
        self.gate_lost = 0
        self.mission_timeout = MISSION_TIMEOUT

    def init(self):
        # dive, but keep heading at same time
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.HoldYaw(),
            sw3.SetDepth(DEPTH)
        ))

        # give some time for the dive to complete
        time.sleep(DELAY)

        # start vision
        self.process_manager.start_process(entities.GateEntity, "gate", "forward", debug=True)

        # go forward
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.HoldYaw(),
            sw3.Forward(FORWARD_SPEED),
        ))

    def step(self, vision_data):
        if TIMEOUT_ENABLED:
            self.mission_timeout -= 1

        if not vision_data:
            return
        gate_data = vision_data['gate']
        if not gate_data:
            return
        print gate_data

        if gate_data and gate_data.left_pole and gate_data.right_pole:
            gate_center = DEGREE_PER_PIXEL * (gate_data.left_pole + gate_data.right_pole) / 2  # degrees

            # If both poles are seen, point toward it then go forward.
            self.gate_seen += 1
            self.gate_lost = 0

            if abs(gate_center) < STRAIGHT_TOLERANCE:
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.Forward(FORWARD_SPEED),
                    sw3.HoldYaw()
                ]))
            else:
                print "Correcting Yaw", gate_center
                sw3.nav.do(sw3.CompoundRoutine([
                    sw3.RelativeYaw(gate_center),
                    sw3.Forward(SLOW_FORWARD_SPEED)
                ]))
        elif self.gate_seen >= 15:
            self.gate_lost += 1

        if self.gate_lost > GATE_LOST_THRESHOLD or self.mission_timeout <= 0:
            print("Gate lost: %s , timeout: %s" % (self.gate_lost>5, self.mission_timeout <= 0))
            if self.mission_timeout <= 0:
                print "Gate Mission Timeout!"

            # we're done with gate. move forward for a bit, and move on
            print "going forward (dead reckoning)"
            sw3.nav.do(sw3.Forward(FORWARD_SPEED, RECKON_TIME))
            time.sleep(RECKON_TIME)

            print "Heading Locked"
            self.finish_mission()
            return
