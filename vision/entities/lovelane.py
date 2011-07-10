
from __future__ import division
import math

import cv
import pdb
from entities.base import VisionEntity
import libvision
from sw3.util import circular_average
from copy import copy

LANE_DIRECTION = -1 #  1 is L ; -1 is backwards L 
XTHRESHOLD = 80     #required sepperation of endpoints
YTHRESHOLD = 80 

class LoveLaneEntity(VisionEntity):

    name = "LoneLaneEntity"
    camera_name = "forward"

    def __init__(self):

        # Thresholds
        self.vertical_threshold = 0.75  # min slope of verticle lines 
        self.horizontal_threshold = 0.25  # max slope of horizontal lines
        self.hough_threshold = 10
        self.hough_gap = 50 #maximum gap in a line segment
        self.hough_min_length = 15 #minimum length of a line segment
        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 15
        self.max_range = 100 #how far in pixels endpoints of segments must be
                            #to be considered a new line

        self.vert_pole = None
        self.horz_pole = None
        self.seen_crossbar = False

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("adaptive_thresh", 20)
            self.create_trackbar("hough_threshold", 100)

    def find(self, frame, debug=True):

        # Resize image to 320x240
        img_copy = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, img_copy)
        cv.SetImageROI(frame, (0, 0, 320, 240))
        cv.Resize(img_copy, frame, cv.CV_INTER_NN)

        found_lovelane = False

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 2)
        cv.Copy(hsv, binary)  # Binary image now contains saturation channel
        cv.SetImageCOI(hsv, 0)

        # Adaptive Filter
        cv.AdaptiveThreshold(binary, binary,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY_INV,
            self.adaptive_thresh_blocksize,
            self.adaptive_thresh,
        )

        # Morphology
        cv.Erode(binary, binary, None, 1)
        cv.Dilate(binary, binary, None, 1)
        if debug:
            color_filtered = cv.CloneImage(binary)

        # Get Edges
        cv.Canny(binary, binary, 30, 40)

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_PROBABILISTIC, 
            rho=1,
            theta=math.pi/180,
            threshold=self.hough_threshold,
            param1=self.hough_min_length,
            param2=self.hough_gap
        )

        #find the two endpoints of the L
        toppoint = []
        bottompoint = []

        for line in raw_lines:
            for point in line:
                if not toppoint:
                    toppoint = copy(point)
                    bottompoint = copy(point)
                    continue

                y_thresh_top = toppoint[1] + LANE_DIRECTION*(point[0]-toppoint[0])
                y_thresh_bot = bottompoint[1] + LANE_DIRECTION*(point[0]-bottompoint[0])
                if point[1] < y_thresh_top:
                    toppoint = copy(point)
                if point[1] > y_thresh_bot:
                    bottompoint = copy(point)

        #check that top and bottom points make sense
        xdistance = abs(toppoint[0] - bottompoint[0])
        ydistance = abs(toppoint[1] - bottompoint[1])

        if  xdistance > XTHRESHOLD and ydistance > YTHRESHOLD:
            #we probably see the lane
            found_lane = True
            centerx = ( toppoint[0] + bottompoint[0] ) / 2
            centery = ( toppoint[1] + bottompoint[1] ) / 2
            self.center = adjust_location((centerx,centery), frame.width, frame.height)
            self.scale = math.sqrt(xdistance**2+ydistance**2)

        else:
            #this probably isn't a lane
            found_lane = False

                
        if debug:
            #circle endpoints
            centertop = (toppoint[0],toppoint[1])
            centerbot = (bottompoint[0], bottompoint[1])
            colortop = (255,0,255)
            colorbot = (0,255,0)
            cv.Circle(frame, centertop, 5, colortop, 2, 8, 0)
            cv.Circle(frame, centerbot, 5, colorbot, 2, 8, 0)
            
            #draw lines
            for line in raw_lines:
                color = (0,0,0)
                cv.Line(frame, line[0], line[1], color, 1, 8, 0) 

            #mark center of lane
            if found_lane:
                center_color = (0,0,255)
                cv.Circle(frame,(centerx, centery),9,center_color, 2, 8, 0)
            
        return  found_lane

    def __repr__(self):
        return "<LoveLaneEntity>"  # TODO

def adjust_location(location, width, height):
    '''
    Move origin to center and flip along horizontal axis.  Right
    and up will then be positive, which makes more sense for
    mission control.
    '''
    return (
        location[0] - width/2,
        -1*location[1] + height/2
    )

