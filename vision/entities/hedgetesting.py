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

class Bar(object):
    def __init__(self, p1, p2, _theta):
        self.point1 = p1
        self.point2 = p2
        self.theta = _theta

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

        rBinary = rf2
       # rBinary = cv2.bitwise_not(rBinary)
        gBinary = rf1

        #Adaptive Threshold
        rBinary = cv2.adaptiveThreshold(rBinary, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        self.adaptive_thresh_blocksize,
                                        self.adaptive_thresh)

        gBinary = cv2.adaptiveThreshold(gBinary, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        self.Gadaptive_thresh_blocksize,
                                        self.Gadaptive_thresh)

        rFrame = rBinary.copy()
        gFrame = gBinary.copy()

        # Morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        rBinary = cv2.erode(rBinary, kernel)
        rBinary = cv2.dilate(rBinary, kernel)
        gBinary = cv2.erode(gBinary, kernel)
        gBinary = cv2.dilate(gBinary, kernel)

        gray = cv2.cvtColor(self.numpy_frame,cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray,150,200,apertureSize = 3)

        lines = cv2.HoughLines(edges,1,np.pi/180,275)
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b)) # Here i have used int() instead of rounding the decimal value, so 3.8 --> 3
            y1 = int(y0 + 1000*(a)) # But if you want to round the number, then use np.around() function, then 3.8 --> 4.0
            x2 = int(x0 - 1000*(-b)) # But we need integers, so use int() function after that, ie int(np.around(x))
            y2 = int(y0 - 1000*(a))
            cv2.line(debug_frame,(x1,y1),(x2,y2),(0,255,0),2)

        rFrame = libvision.cv2_to_cv(rFrame)
        gFrame = libvision.cv2_to_cv(gFrame)
        self.debug_frame = libvision.cv2_to_cv(self.debug_frame)
        # svr.debug("Rframe", rFrame)
        # svr.debug("Gframe", gFrame)
        svr.debug("debug", self.debug_frame)

    def reduce_lines(self):
        for ln in self.raw_reds[:]:
            if abs(ln.theta) < 30:
                self.raw_greens.append(ln)
                self.raw_reds.remove(ln)

    def draw_lines(self):
        for ln in self.raw_reds:
            print ln.theta
            cv2.line(self.debug_frame, ln.point1, ln.point2, (40, 0, 255), 5)

        for ln in self.raw_greens:
            cv2.line(self.debug_frame, ln.point1, ln.point2, (0, 255, 0), 5)

        # # Line Finding on Green pvc
        # Rframe = libvision.cv2_to_cv(Rframe)
        # Gframe = libvision.cv2_to_cv(self.debug_frame)
        # rBinary = libvision.cv2_to_cv(rBinary)
        # self.debug_frame = libvision.cv2_to_cv(self.debug_frame)
        # self.test_frame = libvision.cv2_to_cv(self.test_frame)
        # gBinary = libvision.cv2_to_cv(gBinary)

        # svr.debug("Original", self.test_frame)
        # svr.debug("Red", Rframe)
        # svr.debug("Green", Gframe)
