from __future__ import division
import math

import cv

import svr

import random

from base import VisionEntity
import libvision


def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0]-corner_a[0])**2 + 
                         (corner_b[1]-corner_a[1])**2)
    return distance

def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1]-corner_a[1]) / (corner_b[0] - corner_a[0])
        return slope

def angle_between_lines(slope_a, slope_b):
    if slope_a is not None and slope_b is not None and (1+slope_a*slope_b) != 0:
        angle = math.atan((slope_a - slope_b) / (1+slope_a*slope_b))
        return angle
    else: 
        angle = 0
        return angle

def midpoint(corner_a, corner_b):
    midpoint_x = (corner_b[0] - corner_a[0])/2 + corner_a[0]
    midpoint_y = (corner_b[1] - corner_a[1])/2 + corner_a[1]
    return [midpoint_x, midpoint_y]

def midpointx(corner_a, corner_b):
    midpoint_x = (corner_b[0] - corner_a[0])/2 + corner_a[0]
    return midpoint_x

def midpointy(corner_a, corner_b):
    midpoint_y = (corner_b[1] - corner_a[1])/2 + corner_a[1]
    return midpoint_y

def rect_midpoint(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0])/4
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1])/4
    return [midpoint_x, midpoint_y]

def rect_midpointx(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0])/4
    return midpoint_x

def rect_midpointy(corner_a, corner_b, corner_c, corner_d):
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1])/4
    return midpoint_y

def average_corners(corner_a, corner_b):
    average_corner = [0,0]
    average_corner[0] = (corner_a[0] + corner_b[0])/2
    average_corner[1] = (corner_a[1] + corner_b[1])/2
    return average_corner

def check_for_corner(line1, line2):
    angle_clarity_max = math.pi/2 +.1
    angle_clarity_min = math.pi/2 -.1
    corner_distance = 10
    corner_angle = angle_between_lines(line_slope(line1[0], line1[1]),
                                       line_slope(line2[0], line2[1]))

    if  angle_clarity_min < corner_angle < angle_clarity_max:
        if (math.fabs(line1[0][0] - line2[0][0]) < corner_distance or
            math.fabs(line1[0][1] - line2[0][1]) < corner_distance or
            math.fabs(line1[1][0] - line2[1][0]) < corner_distance or
            math.fabs(line1[1][1] - line2[1][1]) < corner_distance):
            return True
    
class BinsContourEntity(VisionEntity):
    def init(self):

        self.adaptive_thresh_blocksize = 35
        self.adaptive_thresh = 4

    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        og_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, self.debug_frame)
        cv.Copy(self.debug_frame, og_frame)

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1)  #3 before competition #2 at competition
        cv.Copy(hsv, binary)
        cv.SetImageCOI(hsv, 0)

        cv.AdaptiveThreshold(binary, binary,
                             255,
                             cv.CV_ADAPTIVE_THRESH_MEAN_C,
                             cv.CV_THRESH_BINARY_INV,
                             self.adaptive_thresh_blocksize,
                             self.adaptive_thresh,
        )

        # Morphology
        kernel = cv.CreateStructuringElementEx(5, 5, 3, 3, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(binary, binary, kernel, 1)
        cv.Dilate(binary, binary, kernel, 1)

        # Get Edges
        #cv.Canny(binary, binary, 30, 40)

        cv.CvtColor(binary, self.debug_frame, cv.CV_GRAY2RGB)

        svr.debug("Bins", self.debug_frame)