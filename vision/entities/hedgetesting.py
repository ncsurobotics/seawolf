# pylint: disable=E1101
from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range
#import msvcrt
import random


def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1]-corner_a[1])/(corner_b[0]-corner_a[0])
        return slope


def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0]-corner_a[0])**2 +
                         (corner_b[1]-corner_a[1])**2)
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

class HedgeTestingEntity(VisionEntity):

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

        #Adaptive threshold parameters (R)
        self.adaptive_thresh_blocksize = 29  #35 for just green #29 for just red
        self.adaptive_thresh = 8

        #Adaptive threshold parameters (G)
        self.Gadaptive_thresh_blocksize = 35 #35 for just green #29 for just red
        self.Gadaptive_thresh = 6
# 
        self.GR_Threshold0 = 50

        self.GR_Threshold1 = 5

    def process_frame(self, frame):
        self.numpy_frame = libvision.cv_to_cv2(frame)
        self.debug_frame = self.numpy_frame.copy()

        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 7)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv2.COLOR_BGR2HSV)

        (rf1, rf2, rf3) = cv2.split(self.numpy_frame)
        # RF2-inverted for red
        # RF1 for green

        Rbinary = rf2
       # Rbinary = cv2.bitwise_not(Rbinary)
        Gbinary = rf1

        #Adaptive Threshold
        Rbinary = cv2.adaptiveThreshold(Rbinary, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        self.adaptive_thresh_blocksize,
                                        self.adaptive_thresh)

        Gbinary = cv2.adaptiveThreshold(Gbinary, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        self.Gadaptive_thresh_blocksize,
                                        self.Gadaptive_thresh)


        # Morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        Rbinary = cv2.erode(Rbinary, kernel)
        Rbinary = cv2.dilate(Rbinary, kernel)
        Gbinary = cv2.erode(Gbinary, kernel)
        Gbinary = cv2.dilate(Gbinary, kernel)

        Rcontours, Rhierarchy = cv2.findContours(Rbinary,
                                               cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE)

        Gcontours, Ghierarchy = cv2.findContours(Gbinary,
                                               cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE)
        self.raw_reds = []
        self.raw_greens = []

        if len(Rcontours) > 1:
            cnt = Rcontours[0]
            #cv2.drawContours(self.numpy_frame, Rcontours, -1, (255, 255, 255), 3)

            for h, cnt in enumerate(Rcontours):
                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

                # test aspect ratio & area, create bin if matches
                (x, y), (w, h), theta = rect
                x, y, w, h = int(x), int(y), int(w), int(h)
                if w > 0 and h > 0:
                    area = h * w
                    if 500 < area < 20000:
                        aspect_ratio = float(h) / w
                        # Depending on the orientation of the bin, "width" may be flipped with height, thus needs 2 conditions for each case
                        if .01 < aspect_ratio < .2 or 8 < aspect_ratio < 100:
                            cv2.line(self.debug_frame, tuple(box[0]), tuple(box[2]), (40, 0, 255), 5)

        if len(Gcontours) > 1:
            cnt = Gcontours[0]
            #cv2.drawContours(self.numpy_frame, Gcontours, -1, (255, 255, 255), 3)

            for h, cnt in enumerate(Gcontours):
                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

                # test aspect ratio & area, create bin if matches
                (x, y), (w, h), theta = rect
                x, y, w, h = int(x), int(y), int(w), int(h)
                if w > 0 and h > 0:
                    area = h * w
                    if 500 < area < 20000:
                        aspect_ratio = float(h) / w
                        # Depending on the orientation of the bin, "width" may be flipped with height, thus needs 2 conditions for each case
                        if .01 < aspect_ratio < .2 or 8 < aspect_ratio < 100:
                            cv2.line(self.debug_frame, tuple(box[0]), tuple(box[2]), (0, 255, 0), 5)


        def reduce_lines(self):
            pass


        def draw_lines(self):
            pass



        Rbinary = libvision.cv2_to_cv(Rbinary)
        Gbinary = libvision.cv2_to_cv(Gbinary)
        self.debug_frame = libvision.cv2_to_cv(self.debug_frame)
        svr.debug("Rframe", Rbinary)
        svr.debug("Gframe", Gbinary)
        svr.debug("debug", self.debug_frame)

        # # Line Finding on Green pvc
        # Rframe = libvision.cv2_to_cv(Rframe)
        # Gframe = libvision.cv2_to_cv(self.debug_frame)
        # Rbinary = libvision.cv2_to_cv(Rbinary)
        # self.debug_frame = libvision.cv2_to_cv(self.debug_frame)
        # self.test_frame = libvision.cv2_to_cv(self.test_frame)
        # Gbinary = libvision.cv2_to_cv(Gbinary)

        # svr.debug("Original", self.test_frame)
        # svr.debug("Red", Rframe)
        # svr.debug("Green", Gframe)
