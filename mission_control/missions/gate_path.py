
from __future__ import division

from vision import entities
from missions.base import MissionBase
import math, sw3, time

MISSION_TIMEOUT = 5
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.3
DEPTH = 2
DELAY = 2
FIELD_OF_VIEW = 36
PATH_DEPTH = 8
CENTER_TIME = 5
MIN_ANGLE_THRESHOLD = 5
MAX_ANGLE_THRESHOLD = 175

class GateMission(MissionBase):

    def __init__(self):
        self.gate_seen = 0
        self.gate_lost = 0

    def init(self):
        sw3.nav.do(
            sw3.SetDepth(DEPTH),
        )
        time.sleep(DELAY)
        self.process_manager.start_process(entities.GateEntity, "gate", "forward", debug=True)
        self.process_manager.start_process(entities.PathEntity, "path", "down", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.HoldYaw(),
            sw3.Forward(FORWARD_SPEED),
        ))

    def step(self, vision_data):
        if not vision_data:
            return

            if vision_data['path']:
                path_data = vision_data['path']
                print path_data

                theta_x = path_data.x * FIELD_OF_VIEW * math.pi / 180  # path_data.x is percent of fram view . multiplying them gives you theta_x
                theta_y = path_data.y * FIELD_OF_VIEW * math.pi / 180  # path_data.y is percent of frame view . multiplying them gives you theta

                d = PATH_DEPTH - sw3.data.depth()  # depth between path and camera

                x = d * math.sin(theta_x)  # g1ves you the x distance from the frame center to path center
                y = d * math.sin(theta_y)  # gives you the y distance from the frame center to path center

                print "Status:Step   x ", x, "   y ", y

                if self.state == "centering":
                    self.state_centering(x, y)
                if self.state == "orienting":
                    return self.state_orienting(path_data)

            if vision_data['gate']:
                gate_data = vision_data['gate']
                print gate_data

                if gate_data.left_pole and gate_data.right_pole:
                    gate_center = DEGREE_PER_PIXEL * (gate_data.left_pole + gate_data.right_pole) / 2  # degrees

                    if abs(gate_center) < STRAIGHT_TOLERANCE:
                        sw3.nav.do(sw3.CompoundRoutine([
                            sw3.Forward(FORWARD_SPEED),
                            sw3.HoldYaw()
                        ]))
                    else:
                        print "Correcting Yaw", gate_center
                        sw3.nav.do(sw3.CompoundRoutine([
                            sw3.RelativeYaw(gate_center),
                            sw3.Forward(0.4)
                        ]))

    def state_centering(self, x, y):
        position_rho = math.sqrt(x ** 2 + y ** 2)  # hypotenuse-distance from frame center to path center
        position_phi = math.atan2(x, y) * (180 / math.pi)  # angle of center of path from current position
        print "State:Centering  dist ", position_rho, "  angle from current ", position_phi

        sw3.nav.do(sw3.Forward(0))
        yaw_routine = sw3.RelativeYaw(position_phi)
        forward_routine = sw3.Forward(FORWARD_SPEED, CENTER_TIME)
        sw3.nav.do(yaw_routine)
        yaw_routine.on_done(lambda x: sw3.nav.do(forward_routine))

        if position_rho <= CENTER_THRESHOLD:
            self.state = "orienting"

    def state_orienting(self, path_data):
        current_yaw = sw3.data.imu.yaw() * (math.pi / 180) % (2 * math.pi)
        path_angle = (path_data.theta + current_yaw) % math.pi

        sw3.nav.do(sw3.Forward(0))
        opposite_angle = (math.pi + path_angle) % (2 * math.pi)

        print "Status: Orienting   yaw ", current_yaw, " path_angle ", path_angle, " opposite_angle ", opposite_angle

        if sw3.util.circular_distance(self.reference_angle, opposite_angle) < sw3.util.circular_distance(self.reference_angle, path_angle):
            path_angle = opposite_angle

        if path_angle > math.math.pi:
            path_angle = path_angle - 2 * math.pi

        print "Orienting to", (180 / math.pi) * path_angle
        routine = sw3.SetYaw((180 / math.pi) * path_angle, timeout=15)
        routine.on_done(self.finish_mission)
        sw3.nav.do(routine)
        self.state = 'done'

        degree = path_data.theta * (180 / math.pi)

        # if degree <=  MIN_ANGLE_THRESHOLD or degree >= MAX_ANGLE_THRESHOLD:
        if degree <=  MIN_ANGLE_THRESHOLD:
            self.finish_mission()
