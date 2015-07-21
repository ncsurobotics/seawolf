from __future__ import division
import math
import cv
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
        slope = (corner_b[1] - corner_a[1]) / (corner_b[0] - corner_a[0])
        return slope


def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0] - corner_a[0]) ** 2 +
                         (corner_b[1] - corner_a[1]) ** 2)
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


class HedgeYEntity(VisionEntity):

    def init(self):

        # Thresholds For Line Finding
        self.vertical_thresholdG = .2  # How close to verticle lines must be
        self.vertical_thresholdR = .25  # How close to verticle lines must be
        self.horizontal_threshold = 0.5  # How close to horizontal lines must be
        self.hough_thresholdG = 150
        self.hough_thresholdR = 150
        self.max_range = 135

        self.min_length = 50
        self.max_gap = 10

        self.hor_threshold = 2

        self.left_pole = None
        self.right_pole = None
        self.seen_crossbar = False
        self.crossbar_depth = None

        # Adaptive threshold parameters (R)
        self.adaptive_thresh_blocksize = 29  # 35 for just green #29 for just red
        self.adaptive_thresh = 23

        # Adaptive threshold parameters (G)
        self.Gadaptive_thresh_blocksize = 35  # 35 for just green #29 for just red
        self.Gadaptive_thresh = 6

        self.GR_Threshold0 = 50

        self.GR_Threshold1 = 5

    def process_frame(self, frame):
        self.numpy_frame = libvision.cv_to_cv2(frame)
        self.debug_frame = self.numpy_frame.copy()
        self.test_frame = self.numpy_frame.copy()

        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 7)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv2.COLOR_BGR2HSV)

        (rf1, rf2, rf3) = cv2.split(self.numpy_frame)

        Rbinary = rf3
        Gbinary = rf1

        # Adaptive Threshold
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

        Rframe = cv2.cvtColor(Rbinary, cv2.COLOR_GRAY2RGB)
        Gframe = cv2.cvtColor(Gbinary, cv2.COLOR_GRAY2RGB)

        # Hough Transform
        raw_linesG = cv2.HoughLines(Gbinary,
                                    rho=1,
                                    theta=math.pi / 180,
                                    threshold=self.hough_thresholdG)

        # Get vertical lines
        vertical_linesG = []
        for line in raw_linesG[0]:
            rho = line[0]
            theta = line[1]
            if theta < self.vertical_thresholdG or \
                    theta > math.pi - self.vertical_thresholdG:

                vertical_linesG.append((abs(rho), theta))

        # Group vertical lines
        vertical_line_groupsG = []  # A list of line groups which are each a line list
        for line in vertical_linesG:
            group_found = False
            for line_group in vertical_line_groupsG:

                if line_group_accept_test(line_group, line, self.max_range):
                    line_group.append(line)
                    group_found = True

            if not group_found:
                vertical_line_groupsG.append([line])

        # Average line groups into lines
        vertical_linesG = []
        for line_group in vertical_line_groupsG:
            rhos = map(lambda line: line[0], line_group)
            angles = map(lambda line: line[1], line_group)
            line = (sum(rhos) / len(rhos), circular_average(angles, math.pi))
            vertical_linesG.append(line)

        # Get horizontal lines
        horizontal_lines = []
        for line in raw_linesG[0]:
            rho = line[0]
            theta = line[1]
            dist_from_horizontal = (math.pi / 2 + line[1]) % math.pi
            if dist_from_horizontal < self.horizontal_threshold or \
                    dist_from_horizontal > math.pi - self.horizontal_threshold:

                horizontal_lines.append((abs(line[0]), line[1]))

        # Group horizontal lines
        horizontal_line_groups = []  # A list of line groups which are each a line list
        print "Horizontal lines: ",
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
            rhos = map(lambda line: line[0], horizontal_line_groups[0])
            angles = map(lambda line: line[1], horizontal_line_groups[0])
            line = (sum(rhos) / len(rhos), circular_average(angles, math.pi))
            horizontal_lines = [line]
        else:
            self.seen_crossbar = False
            horizontal_lines = []

        self.left_pole = None
        self.right_pole = None

        Rframe = libvision.cv2_to_cv(Rframe)
        Gframe = libvision.cv2_to_cv(self.debug_frame)
        Rbinary = libvision.cv2_to_cv(Rbinary)
        self.debug_frame = libvision.cv2_to_cv(self.debug_frame)
        self.test_frame = libvision.cv2_to_cv(self.test_frame)
        Gbinary = libvision.cv2_to_cv(Gbinary)

        if len(vertical_linesG) is 2:
            roi = cv.GetImageROI(frame)
            width = roi[2]
            height = roi[3]
            self.left_pole = round(min(vertical_linesG[0][0], vertical_linesG[1][0]), 2) - width / 2
            self.right_pole = round(max(vertical_linesG[0][0], vertical_linesG[1][0]), 2) - width / 2
        # TODO: If one pole is seen, is it left or right pole?

        # Calculate planar distance r (assuming we are moving perpendicular to
        # the hedge)
        if self.left_pole and self.right_pole:
            theta = abs(self.left_pole - self.right_pole)
            self.r = 3 / math.tan(math.radians(theta / 2))
        else:
            self.r = None

        if self.r and self.seen_crossbar:
            bar_phi = (-1 * horizontal_lines[0][0] + Gframe.height / 2) / (Gframe.height / 2) * 32
            self.crossbar_depth = self.r * math.atan(math.radians(bar_phi))
        else:
            self.crossbar_depth = None

        # Line Finding on Red pvc
        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_linesR = cv.HoughLines2(Rbinary, line_storage, cv.CV_HOUGH_STANDARD,
                                    rho=1,
                                    theta=math.pi / 180,
                                    threshold=self.hough_thresholdR,
                                    param1=0,
                                    param2=0
                                    )

        # Get vertical lines
        vertical_linesR = []
        for line in raw_linesR:
            if line[1] < self.vertical_thresholdR or \
               line[1] > math.pi - self.vertical_thresholdR:

                vertical_linesR.append((abs(line[0]), line[1]))

        # Group vertical lines
        vertical_line_groupsR = []  # A list of line groups which are each a line list
        for line in vertical_linesR:
            group_found = False
            for line_group in vertical_line_groupsR:

                if line_group_accept_test(line_group, line, self.max_range):
                    line_group.append(line)
                    group_found = True

            if not group_found:
                vertical_line_groupsR.append([line])

        # Average line groups into lines
        vertical_linesR = []
        for line_group in vertical_line_groupsR:
            rhos = map(lambda line: line[0], line_group)
            angles = map(lambda line: line[1], line_group)
            line = (sum(rhos) / len(rhos), circular_average(angles, math.pi))
            vertical_linesR.append(line)
        '''
        for red_line in vertical_linesR:
            print "Red Line:", red_line[0],", ",red_line[1]
        for green_line in vertical_linesG:
            print "Green Line:", green_line[0],", ",green_line[1]
        '''
        for red_line in vertical_linesR:
            for green_line in vertical_linesG[:]:
                if math.fabs(green_line[0] - red_line[0]) < self.GR_Threshold0 and \
                   math.fabs(green_line[1] - red_line[1]) < self.GR_Threshold1:
                    vertical_linesG.remove(green_line)

        for red_line in vertical_linesR:
            print "New Red Line:", red_line[0], ", ", red_line[1]
        for green_line in vertical_linesG:
            print "New Green Line:", green_line[0], ", ", green_line[1]

        if len(vertical_linesR) is 0:
            print "No Red Found"

        self.left_pole = None
        self.right_pole = None
        if len(vertical_linesR) is 2:
            roi = cv.GetImageROI(frame)
            width = roi[2]
            height = roi[3]
            self.left_pole = round(min(vertical_linesR[0][0], vertical_linesR[1][0]), 2) - width / 2
            self.right_pole = round(max(vertical_linesR[0][0], vertical_linesR[1][0]), 2) - width / 2
        # TODO: If one pole is seen, is it left or right pole?

        # Calculate planar distance r (assuming we are moving perpendicular to
        # the hedge)
        if self.left_pole and self.right_pole:
            theta = abs(self.left_pole - self.right_pole)
            self.r = 3 / math.tan(math.radians(theta / 2))
        else:
            self.r = None

        for i in range(len(vertical_linesR[:])):
            if vertical_linesR[i][1] > math.pi / 2:
                vertical_linesR[i] = (vertical_linesR[i][0], -(math.pi - vertical_linesR[i][1]))
                print "Line changed to ", vertical_linesR[i]
        for line in vertical_linesR:
            print line
            if line[1] > math.pi / 2:
                line = (line[0], math.pi - line[1])
                print "Line changed to ", line

        libvision.misc.draw_lines(Gframe, vertical_linesG)
        libvision.misc.draw_lines(Gframe, horizontal_lines)
        libvision.misc.draw_lines(Rframe, vertical_linesR)

        # there was a merge error, these 3 lines conflicted b/c your copy out of date

        for line in vertical_linesR:
            roi = cv.GetImageROI(frame)
            width = roi[2]
            height = roi[3]
            x = line[0] * math.cos(line[1])
            y = line[0] * math.sin(line[1])
            cv.Circle(Rframe, (int(x), int(y)), 5, (0, 255, 0), -1, 8, 0)
            if x > width or y > width or x < 0 or y < 0:
                print "Lost point  ", x

        svr.debug("Original", self.test_frame)
        svr.debug("Red", Rframe)
        svr.debug("Green", Gframe)
