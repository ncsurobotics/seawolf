
import math

import cv

from entities.base import VisionEntity
import libvision

class PathEntity(VisionEntity):

    name = "PathEntity"
    camera_name = "down"

    def __init__(self):

        # Thresholds
        self.min_hue = 200
        self.max_hue = 360
        self.min_saturation = 0
        self.max_saturation = 110
        self.min_value = 220
        self.max_value = 255
        self.theta_threshold = 0.1
        self.hough_threshold = 15
        self.lines_to_consider = 4 # Only consider the strongest so many lines

        # Position/orientation
        self.theta = None

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("min_hue", 360)
            self.create_trackbar("max_hue", 360)
            self.create_trackbar("min_saturation")
            self.create_trackbar("max_saturation")
            self.create_trackbar("min_value")
            self.create_trackbar("max_value")
            self.create_trackbar("hough_threshold")

    def find(self, frame, debug=True):
        found_path = False

        # HSV Color Filter
        binary = libvision.filters.hsv_filter(frame,
            self.min_hue,
            self.max_hue,
            self.min_saturation,
            self.max_saturation,
            self.min_value,
            self.max_value,
        )

        # Morphology
        # We size the kernel to about the width of a path.
        kernel = cv.CreateStructuringElementEx(15, 15, 7, 7, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(binary, binary, kernel, 1)
        cv.Dilate(binary, binary, kernel, 1)

        # Get Edges
        cv.Canny(binary, binary, 30, 40)

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_STANDARD,
            rho=1,
            theta=math.pi/180,
            threshold=self.hough_threshold,
            param1=0,
            param2=0
        )
        lines = lines[:self.lines_to_consider] # Limit number of lines

        # If there are at least 2 lines and they are close to parallel...
        # There's a path!
        if len(lines) >= 2:

            # Find: min, max, average
            theta_max = lines[0][1]
            theta_min = lines[0][1]
            total_theta = 0
            for rho, theta in lines:
                total_theta += theta
                if theta_max < theta:
                    theta_max = theta
                if theta_min > theta:
                    theta_min = theta

            theta_range = theta_max - theta_min
            # Near verticle angles will wrap around from pi to 0.  If the range
            # crosses this verticle line, the range will be way too large.  To
            # correct for this, we always take the smallest angle between the
            # min and max.
            if theta_range > math.pi/2:
                theta_range = math.pi - theta_range

            if theta_range < self.theta_threshold:
                found_path = True
                #TODO: Implement circular angle averaging!  The average will be
                #      flat out WRONG if the angles are near verticle!
                self.theta = total_theta / len(lines)

        #TODO: If path is found, find the center

        if debug:
            cv.CvtColor(binary, frame, cv.CV_GRAY2RGB)
            libvision.misc.draw_lines(frame, lines)

        return found_path

    def __repr__(self):
        return "<PathEntity theta=%s>" % self.theta
