
from __future__ import division
import math
import time

import cv

import svr

from base import VisionEntity
import libvision

import sw3
from sw3.util import circular_average
import seawolf as sw

import math
from math import pi

def circular_distance(a, b, high=180, low=-180):
    '''Finds the signed distance between a and b in a circular fashion.

    high and low are the ends of the wraparound point.  Going any higher than
    high wraps around to low.

    '''

    a -= low
    b -= low
    diff = high - low

    a = a % diff
    b = b % diff
    if abs(a - b) < diff/2:
        return a-b
    elif a - b > 0:
        return diff - (a-b)
    else:
        return (a-b) + diff

class Path(object):
    def __init__(self):
        self.angles = []
        self.angle = 0
        self.verified = False

        self.lines = None
        self.blobs = None
        self.theta = None
        self.center = None

    def add(self, angle):
        self.angles.append(angle)
        self.angle = sw3.util.circular_average(self.angles, -180, 180)

    def count(self):
        return len(self.angles)

class PathManager(object):
    def __init__(self, angle_hint):
        self.paths = []
        self.grouping_angle_threshold = 10
        self.min_path_count = 5
        self.all_lines = []

        self.angle_hint = angle_hint
        self.start_angle = sw3.data.imu.yaw()

    def get_absolute_angle(self, theta):
        angle_hint = sw3.util.add_angle(self.start_angle, self.angle_hint)

        if theta > pi / 2:
            theta = -(pi - theta)
        path_offset = theta * (180 / pi)

        angle = sw3.util.add_angle(sw3.data.imu.yaw(), path_offset)

        if angle_hint < 0 and circular_distance(angle, sw3.util.add_angle(angle_hint, 90)) > 0:
            angle = sw3.util.add_angle(angle, -180)
        elif angle_hint > 0 and circular_distance(angle, sw3.util.add_angle(angle_hint, -90)) < 0:
            angle = sw3.util.add_angle(angle, 180)

        return angle

    def add_lines(self, lines):
        lines = [(line[0], self.get_absolute_angle(line[1])) for line in lines]
        for line in lines:
            if line[1] > 180 or line[1] < -180:
                raise Exception()

        self.all_lines.extend(lines)

        angles = [line[1] for line in lines]
        for angle in angles:
            added = False
            for path in self.paths:
                if abs(circular_distance(path.angle, angle)) < self.grouping_angle_threshold:
                    added = True
                    path.add(angle)
                    break

            if not added:
                path = Path()
                path.add(angle)
                self.paths.append(path)

    def line_distance(self, a, b):
        angle_distance = circular_distance(a[1], b[1])**2
        rho_distance = (a[0] - b[0])**2 * 1e-1
        return (angle_distance + rho_distance)**0.5

    def line_average(self, *lines):
        angle = sw3.util.circular_average([line[1] for line in lines], 180, -180)
        rho = sum([line[0] for line in lines]) / len(lines)
        return (rho, angle)

    def get_paths(self):
        paths = filter(lambda path: path.count() >= self.min_path_count, self.paths)
        paths.sort(key=lambda path: path.count(), reverse=True)
        return paths[:2]

    def classify(self, lines):
        """ Segment the given lines and assign the line clusters to paths """

        paths = self.get_paths()

        if len(paths) < 2:
            return None

        for path in paths:
            path.lines = list()

        absolute_lines = [(line, self.get_absolute_angle(line[1])) for line in lines]

        for line, absolute_angle in absolute_lines:
            paths.sort(key=lambda path: abs(circular_distance(path.angle, absolute_angle)))
            path = paths[0]
            if abs(circular_distance(path.angle, absolute_angle)) < self.grouping_angle_threshold:
                path.lines.append(line)

        for path in paths:
            path.theta = sw3.util.circular_average([line[1] for line in path.lines], pi, 0)

        return paths

    def blob_in_path(self, path, x, y):
        if len(path.lines) == 0:
            return False

        rho_max = max([line[0] for line in path.lines])
        rho_min = min([line[0] for line in path.lines])
        r = sw3.util.euclid_distance((x, y), (0, 0))
        rho = r * math.cos(path.theta - math.atan2(y, x))

        #print x, y, rho_min, rho, rho_max

        if rho_min < rho < rho_max:
            return True

        return False

    def assign_blobs(self, paths, blobs):
        for path in paths:
            path.blobs = list()

        for blob in blobs:
            x, y = blob.centroid
            for path in paths:
                if self.blob_in_path(path, x, y):
                    path.blobs.append(blob)
                    path.verified = True
                    break

        return paths

    def process(self, lines, blobs):
        self.add_lines(lines)
        paths = self.classify(lines)

        if not paths:
            return None

        paths = self.assign_blobs(paths, blobs)
        #print
        #print paths

        paths = filter(lambda path: path.verified, paths)
        #print [path.blobs for path in paths]
        #print

        if len(paths) == 2:
            return paths
        else:
            return None

class DoublePathEntity(VisionEntity):
    name = "Path"

    def init(self, which_path=1, angle_hint=-70):
        self.which_path = which_path
        self.angle_hint = angle_hint
        self.path = None

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
        self.lines_to_consider = 10 # Only consider the strongest so many lines
        self.seen_in_a_row_threshold = 2 # Must see path this many times in a row before reporting it

        # Position/orientation
        self.theta = None
        self.center = None

        self.seen_in_a_row = 0

        self.path_manager = PathManager(self.angle_hint)

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
        self.output.found = False

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        #use RGB color finder
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(frame,250,125,0,1500,500,.3)
        color_filtered = cv.CloneImage(binary)

        blob_map = cv.CloneImage(binary)
        blobs = libvision.blob.find_blobs(binary, blob_map, min_blob_size=50, max_blobs=10)

        if not blobs:
            return

        binary = cv.CloneImage(blob_map)
        mapping = [0] * 256
        for blob in blobs:
            mapping[blob.id] = 255
        libvision.greymap.greymap(blob_map, binary, mapping)

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

        if not lines:
            return

        paths = self.path_manager.process(lines, blobs)

        if paths and not self.path:
            # If path[1] is clockwise of paths[0]
            distance  = circular_distance(paths[1].angle, paths[0].angle)

            print
            print "Distance: ", distance
            print paths[1].angle, paths[0].angle

            if distance > 0:
                self.path = paths[self.which_path]
            else:
                self.path = paths[1 - self.which_path]

            print self.path.angle, self.path.theta
            print

        if paths and self.path in paths and self.path.blobs:
            temp_map = cv.CloneImage(blob_map)

            mapping = [0] * 256
            for blob in self.path.blobs:
                mapping[blob.id] = 255
            libvision.greymap.greymap(blob_map, temp_map, mapping)
            center = self.find_centroid(temp_map)

            svr.debug("map", temp_map)

            self.path.center = (
                 center[0] - (frame.width / 2),
                -center[1] + (frame.height / 2)
            )

            self.output.found = True
            self.output.theta = self.path.theta
            self.output.x = self.path.center[0] / (frame.width / 2)
            self.output.y = self.path.center[1] / (frame.height / 2)
            print self.output

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
            if self.output.found:
                rounded_center = (
                    int(round(center[0])),
                    int(round(center[1])),
                    )
                cv.Circle(frame, rounded_center, 5, (0,255,0))
                libvision.misc.draw_lines(frame, [(frame.width/2, self.path.theta)])
            else:
                libvision.misc.draw_lines(frame, lines)

            svr.debug("Path", frame)

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
