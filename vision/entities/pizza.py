

from __future__ import division
import math

import cv

import svr

import random

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range

class Pizza(object):
    def __init__(self,type,center,angle,area):
        #ID number used when tracking bins
        self.id = 0

        #decisive type of letter in the bin
        self.type = type

        #center of bin
        self.center = center

        #direction of the bin
        self.angle = angle

        #area of the bin
        self.area = area

        #tracks timeout for bin
        self.timeout = 10

        #tracks our type decisions
        self.type_counts = [0,0,0,0,0]


def line_distance(corner_a, corner_b):
        distance = math.sqrt((corner_b[0]-corner_a[0])**2 + (corner_b[1]-corner_a[1])**2)
        return distance
def line_distance(corner_a, corner_b):
        distance = math.sqrt((corner_b[0]-corner_a[0])**2 + (corner_b[1]-corner_a[1])**2)
        return distance

def line_slope(corner_a, corner_b):
        if corner_a[0] != corner_b[0]:
                slope = (corner_b[1]-corner_a[1])/(corner_b[0]-corner_a[0])
                return slope

def angle_between_lines(slope_a, slope_b):
    if slope_a != None and slope_b != None and (1+slope_a*slope_b) != 0:
        angle = math.atan((slope_a - slope_b)/(1+slope_a*slope_b))
        return angle
    else: 
        angle = 0
        return angle

def midpoint(corner_a, corner_b):
        midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
        midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
        return [midpoint_x, midpoint_y]

def midpointx(corner_a, corner_b):
        midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
        return midpoint_x

def midpointy(corner_a, corner_b):
        midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
        return midpoint_y

def rect_midpointx(corner_a,corner_b,corner_c,corner_d):
        midpoint_x = (corner_a[0]+corner_b[0]+corner_c[0]+corner_d[0])/4
        return midpoint_x

def rect_midpointy(corner_a,corner_b,corner_c,corner_d):
        midpoint_y = (corner_a[1]+corner_b[1]+corner_c[1]+corner_d[1])/4
        return midpoint_y

def check_for_corner(line1,line2):
    corner_distance = 10
    angle_clarity_max = math.pi/2+.1
    angle_clarity_min = math.pi/2-.1

    if angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > angle_clarity_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < angle_clarity_max:
        if math.fabs(line1[0][0] - line2[0][0]) < corner_distance or math.fabs(line1[0][1] - line2[0][1]) < corner_distance or math.fabs(line1[1][0] - line2[1][0]) < corner_distance or math.fabs(line1[1][1] - line2[1][1]) < corner_distance:
            return True
    


class PizzaEntity(VisionEntity):

    def init(self):
	
#	self.vertical_threshold = 15*math.pi/180  # How close to vertical lines must be
#        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 120
        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 7
        self.max_range = 100

        #For Probalistic
        self.min_length = 2
        self.max_gap = 40

        #grouping
        self.max_corner_range = 15
        
        #For Rectangle Indentification Variables, look at function


        #how close the sizes of parallel lines of a bin must be to eachother
        self.size_threshold = 40
        #How close to the ideal 1:1 ratio the bin sides must be
        self.ratio_threshold = .7

    def process_frame(self, frame):
	debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
	cv.Copy(frame, debug_frame)


        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 3)
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
   
        cv.CvtColor(binary,debug_frame, cv.CV_GRAY2RGB)
	

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_PROBABILISTIC,
            rho=1,
            theta=math.pi/180,
            threshold=self.hough_threshold,
            param1=self.min_length,
            param2=self.max_gap
        )

	
        lines = []
        for line in raw_lines:
            lines.append(line)
        #Grouping lines depending on endpoint simularities
        for line1 in lines[:]:
            for line2 in lines[:]:
                if line1 in lines and line2 in lines and line1 != line2:
                    if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range and math.fabs(line1[0][1] - line2[0][1]) < self.max_corner_range and math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range and math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1])> line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)
                    elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range and math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range and math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range and math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1])> line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)
                      
        
        if len(lines) > 3:
            for line1 in lines:
                for line2 in lines:
                    for line3 in lines:
                        for line4 in lines:
                            if check_for_corner(line1,line2) and check_for_corner(line1, line3) and check_for_corner(line2,line4) and check_for_corner(line3,line4):
                                print "found"
                                line_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#                                cv.Line(debug_frame,line1[0],line1[1], line_color, 10, cv.CV_AA, 0)
#                                cv.Line(debug_frame,line2[0],line2[1], line_color, 10, cv.CV_AA, 0)
#                                cv.Line(debug_frame,line3[0],line3[1], line_color, 10, cv.CV_AA, 0)
#                                cv.Line(debug_frame,line4[0],line4[1], line_color, 10, cv.CV_AA, 0)

                        

              



        for line in lines:
            cv.Line(debug_frame, line[0], line[1], (0,255,255), 5, cv.CV_AA, 0)
            cv.Circle(debug_frame, line[0], 15, (255,0,0), 2,8,0)
            cv.Circle(debug_frame, line[1], 15, (255,0,0), 2,8,0)


        svr.debug("Bins", debug_frame)

