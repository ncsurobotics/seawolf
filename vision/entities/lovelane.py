
from __future__ import division
import math

import cv
import pdb
from entities.base import VisionEntity
import libvision
from sw3.util import circular_average

def line_group_accept_test(line_group, line, max_range):
    '''
    Returns True if the line should be let into the line group.

    First calculates what the range of rho values would be if the line were
    added.  If the range is greater than max_range the line is rejected and
    False is returned.
    '''
    line_accepted = True
    for l in line_group:
        d00 = math.sqrt((l[0][0]-line[0][0])**2 \
            + (l[0][1]-line[0][1])**2)
        d01 = math.sqrt((l[0][0]-line[1][0])**2 \
            + (l[0][1]-line[1][1])**2)
        d10 = math.sqrt((l[1][0]-line[0][0])**2 \
            + (l[1][1]-line[0][1])**2)
        d11 = math.sqrt((l[1][0]-line[1][0])**2 \
            + (l[1][1]-line[1][1])**2)

        if ((d00 > max_range and d01 > max_range) or \
            (d10 > max_range and d11 > max_range) ):
            line_accepted = False
            break
    return line_accepted

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
        copy = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, copy)
        cv.SetImageROI(frame, (0, 0, 320, 240))
        cv.Resize(copy, frame, cv.CV_INTER_NN)

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

        '''
        if debug:
            for line in raw_lines:
                point = (line[0], line[1])
                color = (0,0,0)
                cv.Line(frame, line[0], line[1], color, 1, 8, 0) 
        '''

        
        # Get vertical lines
        vertical_lines = []
        for line in raw_lines:
            if(line[0][0] == line[1][0]):
                vertical_lines.append( line )
                continue
            slope = abs( (line[1][1]-line[0][1]) / (line[0][0]-line[1][0]) )
            if slope > self.vertical_threshold:
                vertical_lines.append( line )

        # Group vertical lines
        vertical_line_groups = []  # A list of line groups which are each a line list
        for line in vertical_lines:
            group_found = False
            for line_group in vertical_line_groups:

                if line_group_accept_test(line_group, line, self.max_range):
                    line_group.append(line)
                    group_found = True

            if not group_found:
                vertical_line_groups.append([line])

        # Average line groups into lines
        vertical_lines = []
        upper_pt = [0,0]
        lower_pt = [0,0]
        for line_group in vertical_line_groups:
            '''
            for line in line_group:
                if(line[0][1] < line[1][1]):
                    upper_pt[0]+=line[0][0]
                    upper_pt[1]+=line[0][1]
                    lower_pt[0]+=line[1][0]
                    lower_pt[1]+=line[1][1]
                else:
                    upper_pt[0]+=line[1][0]
                    upper_pt[1]+=line[1][1]
                    lower_pt[0]+=line[0][0]
                    lower_pt[1]+=line[0][1]
            line_count = len(line_group)
            upper_pt[0] = int(upper_pt[0] / line_count)
            upper_pt[1] = int(upper_pt[1] / line_count)
            lower_pt[0] =  int(lower_pt[0] / line_count)
            lower_pt[1] =  int(lower_pt[1] / line_count)
            line = ((upper_pt[0],upper_pt[1]), (lower_pt[0],lower_pt[1]))
            vertical_lines.append(line)
            '''
            vertical_lines.append(((line_group[0][0][0],line_group[0][0][1]),\
                (line_group[0][1][0],line_group[0][1][1])))

        # Get horizontal lines
        horizontal_lines = []
        for line in raw_lines:
            if(line[0][0] == line[1][0]):
                continue
            slope = abs( (line[1][1]-line[0][1]) / (line[0][0]-line[1][0]) )
            if slope < self.horizontal_threshold:
                horizontal_lines.append(line)

        # Group horizontal lines
        horizontal_line_groups = []  # A list of line groups which are each a line list
        for line in horizontal_lines:
            group_found = False
            for line_group in horizontal_line_groups:

                if line_group_accept_test(line_group, line, self.max_range):
                    line_group.append(line)
                    group_found = True

            if not group_found:
                horizontal_line_groups.append([line])

        # Average line groups into lines
        horizontal_lines = []
        left_pt = [0,0]
        right_pt = [0,0]
        for line_group in horizontal_line_groups:
            '''
            for line in line_group:
                if(line[0][1] < line[1][1]):
                    left_pt[0]+=line[0][0]
                    left_pt[1]+=line[0][1]
                    right_pt[0]+=line[1][0]
                    right_pt[1]+=line[1][1]
                else:
                    left_pt[0]+=line[1][0]
                    left_pt[1]+=line[1][1]
                    right_pt[0]+=line[0][0]
                    right_pt[1]+=line[0][1]
            line_count = len(line_group)
            left_pt[0] = int(left_pt[0] / line_count)
            left_pt[1] = int(left_pt[1] / line_count)
            right_pt[0] = int(right_pt[0] / line_count)
            right_pt[1] = int(right_pt[1] / line_count) 
            line = ((left_pt[0],left_pt[1]), (right_pt[0],right_pt[1]))
            horizontal_lines.append(line)
            '''
            horizontal_lines.append(((line_group[0][0][0],line_group[0][0][1]),\
                (line_group[0][1][0],line_group[0][1][1])))

        if debug:
            for line in vertical_lines:
                point = (line[0], line[1])
                color = (255,0,255)
                cv.Line(frame, line[0], line[1], color, 1, 8, 0) 
            for line in horizontal_lines:
                point = (line[0], line[1])
                color = (0,255,0)
                cv.Line(frame, line[0], line[1], color, 1, 8, 0) 

        '''
        if len(horizontal_line_groups) == 1:
            self.seen_crossbar = True
            if debug:
                rhos = map(lambda line: line[0], horizontal_line_groups[0])
                angles = map(lambda line: line[1], horizontal_line_groups[0])
                line = (sum(rhos)/len(rhos), circular_average(angles, math.pi))
                horizontal_lines = [line]
        else:
            self.seen_crossbar = False
            horizontal_lines = []

        for horizontal_lines in horizontal_line_groups:
            for vertical_lines in vertical_line_groups:
                pass #TODO: I stopped in the middle of writing stuff here...
        '''
        ''' Old stuff copied from gate:
        self.left_pole = None
        self.right_pole = None
        if len(vertical_lines) is 2:
            roi = cv.GetImageROI(frame)
            width = roi[2]
            height = roi[3]
            self.left_pole = round(min(vertical_lines[0][0], vertical_lines[1][0]), 2) - width/2
            self.right_pole = round(max(vertical_lines[0][0], vertical_lines[1][0]), 2) - width/2
        #TODO: If one pole is seen, is it left or right pole?
        '''
        '''
        if debug:
            cv.CvtColor(color_filtered, frame, cv.CV_GRAY2RGB)
            libvision.misc.draw_lines(frame, vertical_lines)
            libvision.misc.draw_lines(frame, horizontal_lines)
        '''
    def __repr__(self):
        return "<LoveLaneEntity>"  # TODO


def average_line(lines):
    rhos = map(lambda line: line[0], horizontal_line_groups[0])
    angles = map(lambda line: line[1], horizontal_line_groups[0])
    return (sum(rhos)/len(rhos), circular_average(angles, math.pi))
