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


class HedgeTestEntity(VisionEntity):

    def init(self):

        # Thresholds For Line Finding
        self.vertical_thresholdG = .2  # How close to verticle lines must be
        self.vertical_thresholdR = .25  # How close to verticle lines must be
        self.horizontal_threshold = 0.5  # How close to horizontal lines must be
        self.hough_threshold = 150
        self.max_range = 135

        self.hor_threshold = 2

        self.left_pole = None
        self.right_pole = None
        self.seen_crossbar = False
        self.crossbar_depth = None

        # Adaptive threshold parameters (G)
        self.adaptive_thresh_blocksize = 35  # 35 for just green #29 for just red
        self.adaptive_thresh = 2

        self.GR_Threshold0 = 50

        self.GR_Threshold1 = 5

    def process_frame(self, frame):
        numpy_frame = libvision.cv_to_cv2(frame)
        svr.debug("Original", frame)

        numpy_frame = cv2.medianBlur(numpy_frame, 7)
        debug_frame = numpy_frame.copy()
        numpy_frame = cv2.cvtColor(numpy_frame, cv2.COLOR_BGR2HSV)

        (h, s, v) = cv2.split(numpy_frame)

        binary = h

        binary = cv2.adaptiveThreshold(binary, 255,
                                       cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY_INV,
                                       self.adaptive_thresh_blocksize,
                                       self.adaptive_thresh)

        # Morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        binary = cv2.dilate(binary, kernel)
        binary = cv2.dilate(binary, kernel)

        # Hough Transform
        raw_lines = cv2.HoughLinesP(binary,
                                    rho=1,
                                    theta=math.pi / 180,
                                    threshold=self.hough_threshold,
                                    minLineLength=50,
                                    maxLineGap=10)

        if raw_lines is None:
            raw_lines = []
        else:
            raw_lines = raw_lines[0]

        def slope(line):
            """ Determine the slope [in degrees] of a line """
            (x1, y1, x2, y2) = line

            p1 = (x1, y1)
            p2 = (x2, y2)

            leftx = min(x1, x2)

            if p1[0] == leftx:
                left = p1
                right = p2
            else:
                right = p1
                left = p2

            slope = (right[1]-left[1]) / (right[0]-left[0])

            return slope

        def angle(line):
            sl = slope(line)
            return math.degrees(math.atan2(sl, 1))

        def length(line):
            (x1, y1, x2, y2) = line
            return ((x2-x1)**2 + (y2-y1)**2) ** .5

        def center(line):
            """ Determine the center of a line """
            (x1, y1, x2, y2) = line

            p1 = (x1, y1)
            p2 = (x2, y2)

            leftx = min(x1, x2)

            if p1[0] == leftx:
                left = p1
                right = p2
            else:
                right = p1
                left = p2

            centerx = int(left[0] + length(line)/2*math.cos(math.atan2(slope(line), 1)))
            centery = int(left[1] + length(line)/2*math.sin(math.atan2(slope(line), 1)))

            return (centerx, centery)

        def is_vertical(line):
            return 60 <= abs(angle(line)) <= 90

        def is_horizontal(line):
            return 0 <= abs(angle(line)) <= 30

        def get_avg_endpoints(lines):
            lefts = []
            rights = []

            for line in lines:
                (x1, y1, x2, y2) = line

                p1 = (x1, y1)
                p2 = (x2, y2)

                leftx = min(x1, x2)

                if p1[0] == leftx:
                    left = p1
                    right = p2
                else:
                    right = p1
                    left = p2

                lefts.append(left)
                rights.append(right)

            return (average_pts(lefts), average_pts(rights))

        def get_med_endpoints(lines):
            lefts = []
            rights = []

            for line in lines:
                (x1, y1, x2, y2) = line

                p1 = (x1, y1)
                p2 = (x2, y2)

                leftx = min(x1, x2)

                if p1[0] == leftx:
                    left = p1
                    right = p2
                else:
                    right = p1
                    left = p2

                lefts.append(left)
                rights.append(right)

            return (bad_median(lefts, .25), bad_median(rights, .75))

        def average_pts(pts):
            num = len(pts)

            if num == 0:
                return None

            avg_x = sum(x for (x, y) in pts) / num
            avg_y = sum(y for (x, y) in pts) / num
            return (int(avg_x), int(avg_y))

        def median_pts(pts):
            num = len(pts)

            if num == 0:
                return None

            pts = sorted(pts, key=lambda x: x[0])
            return pts[num//2]

        def bad_median(pts, val=.5):
            num = len(pts)

            if num == 0:
                return None

            pts = sorted(pts, key=lambda x: x[0])
            return pts[int(num*val)]

        def get_normal_vec(line):
            sl = slope(line)
            return line

        h_lines = []
        v_lines = []

        for line in raw_lines:
            if is_horizontal(line):
                h_lines.append(line)
            elif is_vertical(line):
                v_lines.append(line)
            else:
                (x1, y1, x2, y2) = line
                cv2.line(debug_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if h_lines:
            self.seen_crossbar = False
            self.crossbar_depth = None

        for line in h_lines:
            (x1, y1, x2, y2) = line
            cv2.line(debug_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for line in v_lines:
            (x1, y1, x2, y2) = line
            cv2.line(debug_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        h_centers = [center(line) for line in h_lines]
        v_centers = sorted([center(line) for line in v_lines], key=lambda x: x[0])

        h_avg_center = median_pts(h_centers)
        v_avg_center = average_pts(v_centers)

        if h_avg_center:
            cv2.circle(debug_frame, h_avg_center, 5, (0, 0, 0), -1)

        if v_avg_center:
            cv2.circle(debug_frame, v_avg_center, 5, (0, 0, 0), -1)

        split_pt = None

        for i in range(len(v_centers)):

            if i < len(v_centers)-1 and v_centers[i+1][0] - v_centers[i][0] > 40:
                split_pt = i+1
                break

        left_pole_center = None
        right_pole_center = None

        if split_pt:
            left_centers = v_centers[:split_pt]
            right_centers = v_centers[split_pt:]

            avg_left = average_pts(left_centers)
            avg_right = average_pts(right_centers)

            left_pole_center = avg_left
            right_pole_center = avg_right

        elif v_avg_center and h_avg_center and h_avg_center[0] - v_avg_center[0] > 60:
            left_pole_center = v_avg_center
            cv2.circle(debug_frame, v_avg_center, 5, (0, 0, 0), -1)

        elif v_avg_center and h_avg_center and h_avg_center[0] - v_avg_center[0] < -60:
            right_pole_center = v_avg_center
            cv2.circle(debug_frame, v_avg_center, 5, (0, 0, 0), -1)

        else:
            avg_endpoints = get_med_endpoints(h_lines)
            lefts = avg_endpoints[0]
            rights = avg_endpoints[1]

            if lefts:
                cv2.circle(debug_frame, lefts, 5, (0, 0, 0), -1)

            if rights:
                cv2.circle(debug_frame, rights, 5, (0, 0, 0), -1)

            left_pole_center = None
            right_pole_center = None

        if left_pole_center:
            self.left_pole = None
            cv2.circle(debug_frame, left_pole_center, 5, (0, 0, 0), -1)

        if right_pole_center:
            self.right_pole = None
            cv2.circle(debug_frame, right_pole_center, 5, (0, 0, 0), -1)

        # median_slope_h = np.median(list(slope(line) for line in h_lines))
        # average_slope_v = None if len(v_lines) == 0 else sum(slope(line) for line in v_lines) / len(v_lines)

        # center_horiz =

        # points = []

        # for x1, y1, x2, y2 in raw_lines:
        #     points.append((x1, y1))
        #     points.append((x2, y2))

        # if points:
        #     rect = cv2.minAreaRect(np.array(points))
        #     box = cv2.cv.BoxPoints(rect)
        #     box = np.int0(box)

        #     # test aspect ratio & area, create bin if matches
        #     (x, y), (w, h), theta = rect

        #     cv2.drawContours(debug_frame, [box], 0, (0, 0, 255), 2)

        binary = libvision.cv2_to_cv(binary)
        svr.debug("Binary", binary)

        debug_frame = libvision.cv2_to_cv(debug_frame)
        svr.debug("Debug", debug_frame)

        # debug_frame = binary
        # debug_frame = libvision.cv2_to_cv(debug_frame)
        # svr.debug("debug", debug_frame)
        # svr.debug("Red", Rframe)
        # svr.debug("Green", Gframe)
        # svr.debug("Green Binary", Gbinary)
