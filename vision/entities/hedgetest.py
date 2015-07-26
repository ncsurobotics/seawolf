from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision


def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1] - corner_a[1]) / (corner_b[0] - corner_a[0])
        return slope


def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0] - corner_a[0]) ** 2 +
                         (corner_b[1] - corner_a[1]) ** 2)
    return distance


def line_group_accept_test(line_group, line, max_range):
    '''
    Returns True if the line should be let into the line group.

    First calculates what the range of rho values would be if the line were
    added.  If the range is greater than max_range the line is rejected and
    False is returned.
    '''
    min_rho = line[0]
    max_rho = line[0]
    for l in line_group:
        if l[0] > max_rho:
            max_rho = l[0]
        if l[0] < min_rho:
            min_rho = l[0]
    return max_rho - min_rho < max_range


class Bar(object):

    def __init__(self, p1, p2, _theta):
        self.point1 = p1
        self.point2 = p2
        self.theta = _theta


class HedgeTestEntity(VisionEntity):

    def init(self):

        # Thresholds For Line Finding
        self.vertical_thresholdG = .2  # How close to verticle lines must be
        self.vertical_thresholdR = .7  # How close to verticle lines must be
        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_thresholdG = 200
        self.hough_thresholdR = 150
        self.max_range = 135

        self.min_length = 50
        self.max_gap = 10

        self.hor_threshold = 2

        self.left_pole = None
        self.right_pole = None
        self.seen_crossbar = False
        self.crossbar_depth = None

        # Adaptive threshold parameters (R)
        self.adaptive_thresh_blocksize = 29  # 35 for just green #29 for just red
        self.adaptive_thresh = 8

        # Adaptive threshold parameters (G)
        self.Gadaptive_thresh_blocksize = 35  # 35 for just green #29 for just red
        self.Gadaptive_thresh = 6
#
        self.GR_Threshold0 = 50

        self.GR_Threshold1 = 5

    def process_frame(self, frame):
        numpy_frame = libvision.cv_to_cv2(frame)
        numpy_frame = cv2.medianBlur(numpy_frame, 7)
        hsv_frame = cv2.cvtColor(numpy_frame, cv2.COLOR_BGR2HSV)
        (h, s, v) = cv2.split(hsv_frame)

        debug_frame = cv2.inRange(hsv_frame, np.array([25, 0, 205], dtype=np.uint8), np.array([60, 160, 255], dtype=np.uint8))
        # debug_frame = cv2.inRange(hsv_frame, np.array([25, 0, 0], dtype=np.uint8), np.array([45, 255, 255], dtype=np.uint8))

        debug_frame = libvision.cv2_to_cv(debug_frame)
        svr.debug("debug", debug_frame)
        numpy_frame = libvision.cv2_to_cv(numpy_frame)
        svr.debug("original", numpy_frame)

    def draw_lines(self):
        for ln in self.raw_reds:
            print ln.theta
            cv2.line(self.debug_frame, ln.point1, ln.point2, (40, 0, 255), 5)

        for ln in self.raw_greens:
            cv2.line(self.debug_frame, ln.point1, ln.point2, (0, 255, 0), 5)

        # Line Finding on Green pvc
        # Rframe = libvision.cv2_to_cv(Rframe)
        # Gframe = libvision.cv2_to_cv(self.debug_frame)
        # rBinary = libvision.cv2_to_cv(rBinary)
        # self.debug_frame = libvision.cv2_to_cv(self.debug_frame)
        # self.test_frame = libvision.cv2_to_cv(self.test_frame)
        # gBinary = libvision.cv2_to_cv(gBinary)

        # svr.debug("Original", self.test_frame)
        # svr.debug("Red", Rframe)
        # svr.debug("Green", Gframe)
