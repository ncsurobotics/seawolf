#This entity detects the white pvc box surrounding the 
# base of the buoys

from __future__ import division
import math

import cv

from entities.base import VisionEntity
import libvision
from sw3.util import circular_average

TRACKING_THRESHOLD = 4 #how many consecutive frames we must see a bar
TRAVEL_THRESHOLD = 25 #how far a bar is allowed to travel between frames

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

class BuoyBoxEntity(VisionEntity):

    name = "BuoyBoxEntity"
    camera_name = "down"

    def __init__(self):

        # Thresholds
        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 50
        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 7
        self.max_range = 60
        self.prev_rho = None
        self.tracking_counter = 0

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("adaptive_thresh", 20)
            self.create_trackbar("hough_threshold", 100)

    def find(self, frame, debug=True):

        found_gate = False

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Adaptive Filter
        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1)
        cv.Copy(hsv, binary)  # Binary image now contains saturation channel

        cv.AdaptiveThreshold(binary, binary,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY_INV,
            self.adaptive_thresh_blocksize,
            self.adaptive_thresh,
        )

        if debug:
            color_filtered = cv.CloneImage(binary)

        # Get Edges
        cv.Canny(binary, binary, 30, 40)

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_STANDARD,
            rho=1,
            theta=math.pi/180,
            threshold=self.hough_threshold,
            param1=0,
            param2=0
        )

        # Get horizontal lines
        horizontal_lines = []
        for line in raw_lines:
            dist_from_horizontal = (math.pi/2 + line[1]) % math.pi
            if dist_from_horizontal < self.horizontal_threshold or \
                dist_from_horizontal > math.pi-self.horizontal_threshold:

                horizontal_lines.append( (abs(line[0]), line[1]) )
                
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

        if len(horizontal_line_groups) is 1:
            self.seen_crossbar = True
        else:
            self.seen_crossbar = False
            horizontal_lines = []

        if debug:
            libvision.misc.draw_lines(frame, horizontal_lines)

        #if we see 1 horizontal line cluster, record the average rho
        if not self.seen_crossbar:
            self.tracking_counter = 0
            return False

        avg_rho = 0
        for line in horizontal_line_groups[0]:
            avg_rho += line[0]
        avg_rho /= len(horizontal_line_groups[0])

        #if this is close to the previous rho, increment counter
        if self.prev_rho and abs(avg_rho - self.prev_rho) < TRAVEL_THRESHOLD:
            self.tracking_counter += 1 

        self.prev_rho = avg_rho
        
        print "average rho = ",avg_rho, "tracking counter = ",self.tracking_counter 

        #if counter is high enough, return true
        if self.tracking_counter >= TRACKING_THRESHOLD:
            return True
        else:
            return False

    def __repr__(self):
        return "<BuoyBox>"
