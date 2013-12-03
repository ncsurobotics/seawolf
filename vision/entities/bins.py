

from __future__ import division
import math

import cv

import svr

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range


class Bin(object):

    def __init__(self, type, center, angle, area):
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
        self.type_counts = [0, 0, 0, 0, 0]


def line_group_accept_test(line_group, line, max_range):
    """
    Returns True if the line should be let into the line group.

    First calculates what the range of rho values would be if the line were
    added.  If the range is greater than max_range the line is rejected and
    False is returned.
    """

    theta = line[1]
    

#    if circular_range(

#    min_rho = line[0]
#    max_rho = line[0]
#    for l in line_group:
#        if l[0] > max_rho:
#            max_rho = l[0]
#        if l[0] < min_rho:
#            min_rho = l[0]
#    return max_rho - min_rho < max_range


class BinsEntity(VisionEntity):

    def init(self):
    
#   self.vertical_threshold = 15*math.pi/180  # How close to vertical lines must be
#        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 180
        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 6
        self.max_range = 100

    def process_frame(self, frame):
        debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
        cv.Copy(frame, debug_frame)
        
        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 2)
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
   
        cv.CvtColor(binary, debug_frame, cv.CV_GRAY2RGB)
    
        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_STANDARD,
                                   rho=1,
                                   theta=math.pi/180,
                                   threshold=self.hough_threshold,
                                   param1=0,
                                   param2=0
                                   )
    
        line_groups = []  # A list of line groups which are each a line list
            
        for line in raw_lines:
            group_found = False
            for line_group in line_groups:

                if line_group_accept_test(line_group, line, self.max_range):
                    line_group.append(line)
                    group_found = True

            if not group_found:
                line_groups.append([line])

            # Average line groups into lines
            lines = []
            for line_group in line_groups:
                rhos = map(lambda line: line[0], line_group)
                angles = map(lambda line: line[1], line_group)
                line = (sum(rhos)/len(rhos), circular_average(angles, math.pi))
                lines.append(line)

        
        libvision.misc.draw_lines(debug_frame, raw_lines)
           # cv.CvtColor(color_filtered,debug_frame, cv.CV_GRAY2RGB)
        svr.debug("Bins", debug_frame)

