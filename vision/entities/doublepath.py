
import math
from time import time

import cv

from entities.base import VisionEntity
import libvision
from sw3.util import circular_average

class Path(object):
    def __init__(self, center, theta, image_center):
        self.center = center
        self.theta = theta
        self.image_center = image_center

class DoublePathEntity(VisionEntity):

    name = "DoublePathEntity"
    camera_name = "down"

    def __init__(self):

        # Thresholds
        self.lower_hue = 60
        self.upper_hue = 220
        self.hue_bandstop = 1
        self.min_saturation = 0
        self.max_saturation = 110
        self.min_value = 100
        self.max_value = 255
        self.theta_threshold = 0.1
        self.hough_threshold = 40
        self.lines_to_consider = 4 # Only consider the strongest so many lines
        self.seen_in_a_row_threshold = 2 # Must see path this many times in a row before reporting it

        self.paths = []

        self.seen_in_a_row = 0

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("lower_hue", 360)
            self.create_trackbar("upper_hue", 360)
            self.create_trackbar("hue_bandstop", 1)
            self.create_trackbar("min_saturation")
            self.create_trackbar("max_saturation")
            self.create_trackbar("min_value")
            self.create_trackbar("max_value")
            self.create_trackbar("hough_threshold", 100)
            self.create_trackbar("lines_to_consider", 10)

    def lines_in_roi(self, frame, binary, path):
        """
        frame - debug output frame
        binary - input binary map
        roi - roi to consider
        """

        cv.SetImageROI(binary, path.roi)
        found_path = False
        theta = None
        center = None

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
                angles = map(lambda line: line[1], lines)
                theta = circular_average(angles, math.pi)

        cv.ResetImageROI(binary)

        if found_path:
            image_center = path.centroid
            # Move the origin to the center of the image
            center = (
                image_center[0] - frame.width/2,
                image_center[1]*-1 + frame.height/2
            )
            return Path(center, theta, image_center)
        else:
            return None


    def find(self, frame, debug=True):
        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        #use RGB color finder 
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(frame,250,125,0,1500,800,.3)

        if debug:
            color_filtered = cv.CloneImage(binary)

        # Morphology
        # We size the kernel to about the width of a path.
        # TODO: If we ever uncomment this, speed it up with
        #       cv.MorphologyEx
        '''
        kernel = cv.CreateStructuringElementEx(7, 7, 3, 3, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(binary, binary, kernel, 1)
        cv.Dilate(binary, binary, kernel, 1)
        '''

        # Get Edges
        cv.Canny(binary, binary, 30, 40)

        path_blobs = libvision.blob.find_blobs(binary, binary, 100, 2, 255)
        
        found_paths = []
        for path_blob in path_blobs:
            path = self.lines_in_roi(frame, binary, path_blob)
            if path:
                found_paths.append(path)

        if found_paths:
            self.seen_in_a_row += 1
        else:
            self.seen_in_a_row = 0
        
        if debug:

            # Show color filtered
            color_filtered_rgb = cv.CreateImage(cv.GetSize(frame), 8, 3)
            cv.CvtColor(color_filtered, color_filtered_rgb, cv.CV_GRAY2RGB)
            cv.SubS(color_filtered_rgb, (255, 0, 0), color_filtered_rgb)
            cv.Sub(frame, color_filtered_rgb, frame)

            # Show edges
            binary_rgb = cv.CreateImage(cv.GetSize(frame), 8, 3)
            cv.CvtColor(binary, binary_rgb, cv.CV_GRAY2RGB)
            cv.Add(frame, binary_rgb, frame)  # Add white to edge pixels
            cv.SubS(binary_rgb, (0, 0, 255), binary_rgb)
            cv.Sub(frame, binary_rgb, frame)  # Remove all but Red

            # Show lines
            for path in found_paths:
                rounded_center = (
                    round(path.image_center[0]),
                    round(path.image_center[1]),
                    )
                cv.Circle(frame, rounded_center, 5, (0,255,0))
                libvision.misc.draw_lines(frame, [(frame.width/2, path.theta)])

        if self.seen_in_a_row >= self.seen_in_a_row_threshold:
            self.paths = found_paths
            return True
        else:
            return False

    def __repr__(self):
        return "<DoublePathEntity> %s" % \
            (repr([(p.center, "%.3f" % (p.theta,)) for p in self.paths]),)
