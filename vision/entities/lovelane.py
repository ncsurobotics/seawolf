
from __future__ import division
import math

import cv
import pdb
from entities.base import VisionEntity
import libvision
from sw3.util import circular_average
from copy import copy

LANE_DIRECTION = -1  # -1 is L ; 1 is backwards L 
VERT_THRESHOLD = 50  #required sepperation of endpoints
HORZ_THRESHOLD = 50 
ANGULAR_TOLERANCE = .06 #how strict our right angle must be

class LoveLaneEntity(VisionEntity):

    name = "LoveLaneEntity"
    camera_name = "forward"

    def __init__(self):

        # Thresholds
        self.vertical_threshold = 0.75  # min slope of verticle lines 
        self.horizontal_threshold = 0.25  # max slope of horizontal lines
        self.hough_threshold = 30
        self.hough_gap = 30 #maximum gap in a line segment
        self.hough_min_length = 30 #minimum length of a line segment
        self.adaptive_thresh_blocksize = 9
        self.adaptive_thresh = 3
        self.max_range = 100 #how far in pixels endpoints of segments must be
                            #to be considered a new line

        self.vert_pole = None
        self.horz_pole = None
        self.seen_crossbar = False

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("adaptive_thresh", 20)
            self.create_trackbar("hough_threshold", 100)

    def draw_point(self, frame, point, c=(255, 255, 255)):
        x, y = point
        w, h = cv.GetSize(frame)
        for i in range(x - 2, x + 2):
            i = min(w - 1, max(0, i))
            for j in range(y - 2, y + 2):
                j = min(h - 1, max(0, j))
                cv.Set2D(frame, j, i, c)

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
        cv.SetImageCOI(hsv, 3)
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
        cv.Dilate(binary, binary, None, 1)
        cv.Erode(binary, binary, None, 1)

        # Filter out small blobs
        libvision.blob.find_blobs(binary, binary, 7, 32, 255)

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

        #verify that we found something
        if not raw_lines:
            print "No lines"
            return False

        if debug:
            #draw lines
            for line in raw_lines:
                color = (0,0,0)
                cv.Line(frame, line[0], line[1], color, 1, 8, 0) 

        #find the three corners of the L
        toppoint = []
        bottomleft = []
        bottomright = []

        for line in raw_lines:
            for point in line:
                if not toppoint:
                    toppoint = copy(point)
                    bottomleft = copy(point)
                    bottomright = copy(point)
                    continue

                y_thresh_top = toppoint[1] + LANE_DIRECTION*(point[0]-toppoint[0])
                y_thresh_bot_left = bottomleft[1] - (point[0]-bottomleft[0])
                y_thresh_bot_right = bottomright[1] + (point[0]-bottomright[0])
                if point[1] < y_thresh_top:
                    toppoint = copy(point)
                if point[1] > y_thresh_bot_left:
                    bottomleft = copy(point)
                if point[1] > y_thresh_bot_right:
                    bottomright = copy(point)

        self.draw_point(frame, toppoint, (255, 0, 0))
        self.draw_point(frame, bottomleft, (0, 255, 0))
        self.draw_point(frame, bottomright, (0, 0, 255))

        #analyze corners
        if LANE_DIRECTION == 1:
            vert_distance = math.sqrt((toppoint[0]-bottomleft[0])**2+(toppoint[1]-bottomleft[1])**2)
            diag_distance = math.sqrt((toppoint[0]-bottomright[0])**2+(toppoint[1]-bottomright[1])**2)
        else:
            vert_distance = math.sqrt((toppoint[0]-bottomright[0])**2+(toppoint[1]-bottomright[1])**2)
            diag_distance = math.sqrt((toppoint[0]-bottomleft[0])**2+(toppoint[1]-bottomleft[1])**2)
        horz_distance = math.sqrt((bottomright[0]-bottomleft[0])**2+(bottomright[1]-bottomleft[1])**2)
        
        #check that the corners are reasonably sepperated
        if vert_distance < VERT_THRESHOLD or horz_distance < HORZ_THRESHOLD:
            print "Sides too short"
            return False

        #check that the three endpoints form roughly a right angle
        hypo_length = math.sqrt(vert_distance**2+horz_distance**2)
        if abs(hypo_length - diag_distance)/hypo_length > ANGULAR_TOLERANCE:
            print "Too un-right"
            return False
        
        found_lane = True
        # compute the center
        if LANE_DIRECTION == 1:
            centerx = ( toppoint[0] + bottomright[0]) / 2
            centery = ( toppoint[1] + bottomright[1]) / 2
        else:
            centerx = ( toppoint[0] + bottomleft[0]) / 2
            centery = ( toppoint[1] + bottomleft[1]) / 2

        self.center = adjust_location((centerx,centery), frame.width, frame.height)
        self.scale = diag_distance

        if debug:
            #circle endpoints
            centertop = (toppoint[0],toppoint[1])
            centerbotleft = (bottomleft[0], bottomleft[1])
            centerbotright = (bottomright[0], bottomright[1])
            colortop = (255,0,255)
            colorbotl = (0,255,0)
            colorbotr = (0, 0, 255)
            cv.Circle(frame, centertop, 5, colortop, 2, 8, 0)
            cv.Circle(frame, centerbotleft, 5, colorbotl, 2, 8, 0)
            cv.Circle(frame, centerbotright, 5, colorbotr, 2, 8, 0)
            
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

