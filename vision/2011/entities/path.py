
import math

import cv

from entities.base import VisionEntity
import libvision

class PathEntity(VisionEntity):

    name = "PathEntity"
    camera_name = "down"

    def __init__(self):

        '''
        self.min_hue = 0
        self.max_hue = 100
        self.min_saturation = 0
        self.max_saturation = 95
        self.min_value = 0
        self.max_value = 255
        '''

        self.min_hue = 200
        self.max_hue = 360
        self.min_saturation = 0
        self.max_saturation = 60
        self.min_value = 0
        self.max_value = 255

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("min_hue", 360)
            self.create_trackbar("max_hue", 360)
            self.create_trackbar("min_saturation")
            self.create_trackbar("max_saturation")
            self.create_trackbar("min_value")
            self.create_trackbar("max_value")

    def find(self, frame, debug=True):

        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_RGB2HSV)

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

        # Get edges
        cv.Canny(binary, binary, 30, 40)

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_STANDARD,
            rho=1,
            theta=math.pi/180,
            threshold=20,
            param1=0,
            param2=0
        )

        if debug:
            #cv.CvtColor(binary, frame, cv.CV_GRAY2RGB)
            cv.CvtColor(color_filtered, frame, cv.CV_GRAY2RGB)

            libvision.misc.draw_lines(frame, lines, 3)

        return True

    def __repr__(self):
        return "<%s>" % self.name
