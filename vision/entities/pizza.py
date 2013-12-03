from __future__ import division
import math

import cv

import svr

import random

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range

class Pizza(object):
    def __init__(self, corner1, corner2, corner3, corner4):
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4
      
        #ID number used when tracking bins
        self.id = 0

        #decisive type of letter in the bin
        self.type = type

        #center of bin
        self.center =  rect_midpoint(corner1, corner2, corner3, corner4)

        #direction of the bin
        self.angle = angle_between_lines(line_slope(corner1, corner2), 0)

        self.lastseen = 2


def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0] - corner_a[0])**2 + 
                         (corner_b[1] - corner_a[1])**2)
    return distance

def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1] - corner_a[1]) / (corner_b[0] - corner_a[0])
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
    return (midpoint_x, midpoint_y)

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


class PizzaEntity(VisionEntity):

    def init(self):
    
#   self.vertical_threshold = 15*math.pi/180  # How close to vertical lines must be
#        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 15
        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 8
        self.max_range = 100

        self.Boxes = []

        #For Probalistic
        self.min_length = 3
        self.max_gap = 40 #40

        #grouping
        self.max_corner_range = 100  #15
        
        #For Rectangle Indentification Variables, look at function

        self.min_corner_distance = 40  #40

        #min and max angle in order to only accept rectangles
        self.angle_min = math.pi/2-.03
        self.angle_max = math.pi/2+.03
        self.angle_min2 = math.pi/2-.03
        self.angle_max2 = math.pi/2+.03

        #how close the sizes of parallel lines of a bin must be to eachother
        self.size_threshold = 40
        #How close to the ideal 1:1 ratio the bin sides must be
        self.ratio_threshold = 1.15

        self.center_thresh = 20

        self.lastseen_thresh = 10
        

    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
        og_frame = cv.CreateImage(cv.GetSize(frame),8,3)
        cv.Copy(frame, self.debug_frame)
        cv.Copy(self.debug_frame, og_frame)

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1)
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
   
        cv.CvtColor(binary,self.debug_frame, cv.CV_GRAY2RGB)
    
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
        corners = []

        for line in raw_lines:
            lines.append(line)
            
        #Grouping lines depending on endpoint similarities

        for line1 in lines[:]:
            for line2 in lines[:]:
                if line1 in lines and line2 in lines and line1 != line2:
                    if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range and \
                       math.fabs(line1[0][1] - line2[0][1]) < self.max_corner_range and \
                       math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range and \
                       math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1]) > line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)
                    elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range and \
                         math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range and \
                         math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range and \
                         math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1]) > line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)

        for line in lines:
            corners.append(line[0])
            corners.append(line[1])
        
        for corner1 in corners:
            for corner2 in corners:
                for corner3 in corners:
                    for corner4 in corners:
                        #Checks that corners are not the same and are in the proper orientation
                        if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and \
                           corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0] and \
                           corner4[1] != corner3[1] and corner4[1] != corner2[1] and corner4[1] != corner1[1] and \
                           corner3[1] != corner2[1] and corner3[1] != corner1[1] and corner2[1] != corner1[1] and \
                           corner2[0] >= corner3[0] and corner1[1] >= corner4[1] and corner2[0] >= corner1[0]:
                            #Checks that the side ratios are correct
                            if math.fabs(line_distance(corner1, corner3) - line_distance(corner2, corner4)) < self.size_threshold and \
                               math.fabs(line_distance(corner1, corner2) - line_distance(corner3, corner4)) < self.size_threshold and \
                               math.fabs(line_distance(corner1, corner3) / line_distance(corner1, corner2)) < self.ratio_threshold and \
                               math.fabs(line_distance(corner1, corner2) / line_distance(corner1, corner3)) < self.ratio_threshold:
                                #^^^ CHANGED OR TO AND --> DID MUCH BETTER. CONSIDER CHANGING ON BINSCORNER

                                #Checks that angles are roughly 90 degrees
                                angle_cnr_2 = math.fabs(angle_between_lines(line_slope(corner1, corner2), line_slope(corner2, corner4)))
                                if self.angle_min < angle_cnr_2 < self.angle_max:
                                    angle_cnr_3 = math.fabs(angle_between_lines(line_slope(corner1, corner3), line_slope(corner3, corner4)))
                                    if self.angle_min2 < angle_cnr_3 < self.angle_max2:                   
                                        new_box = Pizza(corner1, corner2, corner3, corner4)
                                        self.match_Boxes(new_box)

        for Box in self.Boxes[:]:
            Box.lastseen -= 1
            if Box.lastseen < 0:
                self.Boxes.remove(Box)

        self.draw_pizza()      

        for line in lines:
            cv.Line(self.debug_frame,line[0],line[1], (255, 255, 0), 10, cv.CV_AA, 0)
            cv.Circle(self.debug_frame, line[0], 15, (255, 0, 0), 2, 8, 0)
            cv.Circle(self.debug_frame, line[1], 15, (255, 0, 0), 2, 8, 0)

        self.output.pizza = self.Boxes
        anglesum = 0
        for Box in self.Boxes:
            Box.theta = (Box.center[0] - frame.width/2) * 37 / (frame.width/2)
            Box.phi = -1 * (Box.center[1] - frame.height/2) * 36 / (frame.height/2)
            anglesum += Box.angle
        if len(self.output.pizza) > 0:           
            self.output.orientation = anglesum/len(self.output.pizza)
        else:
            self.output.orientation = None
        self.return_output()

        svr.debug("Pizza", self.debug_frame)
        svr.debug("Original", og_frame)


    def match_Boxes(self, target):
        if len(self.Boxes) == 0:
            self.Boxes.append(target)

        for Box in self.Boxes:
            if math.fabs(target.center[0] - Box.center[0]) < self.center_thresh and \
               math.fabs(target.center[1] - Box.center[1]) < self.center_thresh:
                Box.corner1 = target.corner1
                Box.corner2 = target.corner2
                Box.corner3 = target.corner3
                Box.corner4 = target.corner4
                Box.center = target.center
                Box.angle = target.angle
                if Box.lastseen < self.lastseen_thresh:
                    Box.lastseen += 3
                
            else:
                self.Boxes.append(target)
                
                Box.lastseen += 3

    def draw_pizza(self):
        print "Number of boxes:", len(self.Boxes)
        for Box in self.Boxes:
            line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv.Line(self.debug_frame, Box.corner1, Box.corner2, line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame, Box.corner1, Box.corner3, line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame, Box.corner3, Box.corner4, line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame, Box.corner2, Box.corner4, line_color, 10, cv.CV_AA, 0)
            font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, 1)
            cv.PutText(self.debug_frame, str("1"), (int(Box.corner1[0]), int(Box.corner1[1])), font, (0, 0, 255))
            cv.PutText(self.debug_frame, str("2"), (int(Box.corner2[0]), int(Box.corner2[1])), font, (0, 0, 255))
            cv.PutText(self.debug_frame, str("3"), (int(Box.corner3[0]), int(Box.corner3[1])), font, (0, 0, 255))
            cv.PutText(self.debug_frame, str("4"), (int(Box.corner4[0]), int(Box.corner4[1])), font, (0, 0, 255))
            center = (int(Box.center[0]), int(Box.center[1]))
            
            cv.Circle(self.debug_frame, center, 15, (255, 0, 0), 2, 8, 0)





