
import math

import cv

from entities.base import VisionEntity
import libvision

class PathEntity(VisionEntity):

    name = "PathEntity"
    camera_name = "down"

    def __init__(self):

        # Thresholds
        self.lower_hue = 200
        self.upper_hue = 360
        self.hue_bandstop = 0
        self.min_saturation = 0
        self.max_saturation = 110
        self.min_value = 220
        self.max_value = 255
        self.theta_threshold = 0.1
        self.hough_threshold = 20
        self.lines_to_consider = 4 # Only consider the strongest so many lines

        #TODO: Add a number of times in a row the path has to be seen in order
        #      for it to be considered reliable.

        # Position/orientation
        self.theta = None
        self.center = None

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

    def find(self, frame, debug=True):
        found_path = False

        # HSV Color Filter
        binary = libvision.filters.hsv_filter(frame,
            self.lower_hue,
            self.upper_hue,
            self.min_saturation,
            self.max_saturation,
            self.min_value,
            self.max_value,
            self.hue_bandstop,
        )
        if debug:
            color_filtered = cv.CloneImage(binary)

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

        if found_path:
            #TODO: Add a kalman filter (or something) to the center reading
            self.center = self.find_centroid(binary)

            # Move the origin to the center of the image (and round)
            self.center = (
                cv.Round(self.center[0] - frame.width),
                cv.Round(self.center[1] - frame.height)
            )

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
            libvision.misc.draw_lines(frame, lines)
            if found_path:
                cv.Circle(frame, self.center, 5, (0,255,0))

        return found_path

    def find_centroid(self, binary):
        mat = cv.GetMat(binary)
        print mat
        moments = cv.Moments(mat)
        return (moments.m10/moments.m00, moments.m01/moments.m00)

    def __repr__(self):
        return "<PathEntity center=%s theta=%s>" % (self.center, self.theta)
