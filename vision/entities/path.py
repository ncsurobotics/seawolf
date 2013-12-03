

from __future__ import division
import math

import cv

import svr

from base import VisionEntity
import libvision
from sw3.util import circular_average

class PathEntity(VisionEntity):
    name = "Path"

    def init(self):

        # Thresholds
        self.lower_hue = 60
        self.upper_hue = 220
        self.hue_bandstop = 1
        self.min_saturation = 0
        self.max_saturation = 110
        self.min_value = 100
        self.max_value = 255
        self.theta_threshold = 0.1
        self.hough_threshold = 55
        self.lines_to_consider = 4 # Only consider the strongest so many lines
        self.seen_in_a_row_threshold = 2 # Must see path this many times in a row before reporting it

        # Position/orientation
        self.theta = None
        self.center = None

        self.seen_in_a_row = 0

        if self.debug:
            '''
            cv.NamedWindow("Path")
            self.create_trackbar("lower_hue", 360)
            self.create_trackbar("upper_hue", 360)
            self.create_trackbar("hue_bandstop", 1)
            self.create_trackbar("min_saturation")
            self.create_trackbar("max_saturation")
            self.create_trackbar("min_value")
            self.create_trackbar("max_value")
            self.create_trackbar("hough_threshold", 100)
            self.create_trackbar("lines_to_consider", 10)
            '''

    def process_frame(self, frame):
        found_path = False
        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        #use RGB color finder
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(frame, 250, 125, 0, 1500, 500, .3)

        if self.debug:
            color_filtered = cv.CloneImage(binary)

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
        lines = lines[:self.lines_to_consider]  # Limit number of lines

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
            # Near vertical angles will wrap around from pi to 0.  If the range
            # crosses this vertical line, the range will be way too large.  To
            # correct for this, we always take the smallest angle between the
            # min and max.
            if theta_range > math.pi/2:
                theta_range = math.pi - theta_range

            if theta_range < self.theta_threshold:
                found_path = True

                angles = map(lambda line: line[1], lines)
                self.theta = circular_average(angles, math.pi)

        if found_path:
            self.seen_in_a_row += 1
        else:
            self.seen_in_a_row = 0

        #stores whether or not we are confident about the path's presence
        object_present = False

        if self.seen_in_a_row >= self.seen_in_a_row_threshold:
            object_present = True
            self.image_coordinate_center = self.find_centroid(binary)
            # Move the origin to the center of the image
            self.center = (
                self.image_coordinate_center[0] - frame.width/2,
                self.image_coordinate_center[1]*-1 + frame.height/2
            )

        if self.debug:

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
            if self.seen_in_a_row >= self.seen_in_a_row_threshold:
                rounded_center = (
                    int(round(self.image_coordinate_center[0])),
                    int(round(self.image_coordinate_center[1])),
                )
                cv.Circle(frame, rounded_center, 5, (0, 255, 0))
                libvision.misc.draw_lines(frame, [(frame.width/2, self.theta)])
            else:
                libvision.misc.draw_lines(frame, lines)

            #cv.ShowImage("Path", frame)
            svr.debug("Path", frame)

        #populate self.output with infos
        self.output.found = object_present
        self.output.theta = self.theta
        if self.center:
            #scale center coordinates of path based on frame size
            self.output.x = self.center[0]/(frame.width/2)
            self.output.y = self.center[1]/(frame.height/2)
        else:
            self.output.x = None
            self.output.y = None

        if self.output.found and self.center:
            print self.output

        self.return_output()

    def find_centroid(self, binary):
        mat = cv.GetMat(binary)
        moments = cv.Moments(mat)
        return (
            int(moments.m10/moments.m00),
            int(moments.m01/moments.m00)
        )

    def __repr__(self):
        if self.theta is None:
            theta = None
        else:
            theta = round((180/math.pi)*self.theta, 2)
        return "<PathEntity center=%s theta=%s>" % \
            (self.center, theta)
