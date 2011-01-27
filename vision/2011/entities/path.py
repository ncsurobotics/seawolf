
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
        self.min_value = 0
        self.max_value = 255
        self.theta_threshold = 0.1
        self.hough_threshold = 20

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

        # Color Filter
        binary = libvision.filters.hsv_filter(frame,
            self.min_hue,
            self.max_hue,
            self.min_saturation,
            self.max_saturation,
            self.min_value,
            self.max_value,
        )
        color_filtered = cv.CloneImage(binary) #XXX

        # Morphology
        kernel = cv.CreateStructuringElementEx(5, 5, 2, 2, cv.CV_SHAPE_ELLIPSE)
        cv.Dilate(binary, binary, kernel, 2)
        cv.Erode(binary, binary, kernel, 2)

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

        # If there are at least 2 lines and they don't varry much... There's a
        # path!
        #for rho, theta in lines:
            #print theta,
        #print
        if len(lines) >= 2:
            max_theta = lines[0][1]
            min_theta = lines[0][1]
            total_theta = 0
            for rho, theta in lines:
                total_theta += theta
                if max_theta < theta:
                    max_theta = theta
                if min_theta < theta:
                    min_theta = theta
            if max_theta - min_theta < self.theta_threshold:
                found_path = True
                self.theta = total_theta / len(lines) # Average

        if debug:
            cv.CvtColor(binary, frame, cv.CV_GRAY2RGB)
            libvision.misc.draw_lines(frame, lines, 3)

        return found_path

    def __repr__(self):
        return "<PathEntity theta=%s>" % self.theta
