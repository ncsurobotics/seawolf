from __future__ import division
import math
from base_object import BaseObject


class Bin(BaseObject):
    bin_id = 0
    """ an imaged bin b """

    def __init__(self, corner1, corner2, corner3, corner4):
        BaseObject.__init__(self)
        self.type = "bin"
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4
        self.corners = [corner1, corner2, corner3, corner4]
        #self.theta = 0
        self.midx = rect_midpointx(corner1, corner2, corner3, corner4)
        self.midy = rect_midpointy(corner1, corner2, corner3, corner4)
        self.area = 0
        self.id = 0        # id identifies which bin your looking at
        self.lastseen = 2  # how recently you have seen this bin
        # how many times you have seen this bin (if you see it enough it
        # becomes confirmed)
        self.seencount = 1



        dy = (self.corner2[1] - self.corner1[1])
        dx = (self.corner2[0] - self.corner1[0])
        self.line_slope = dy / dx
        
        size1 = line_distance(corner1,corner2)
        size2 = line_distance(corner1,corner4)
        if size1 < size2:
            self.width = size1
            self.height = size2
            #self.theta = angle_between_lines(corner1,corner3,corner2)
            self.theta = line_angle(corner1,corner2)
        else:
            self.width = size2
            self.height = size1
            #self.theta = angle_between_lines(corner1,corner2,corner3)
            self.theta = line_angle(corner1,corner4)



def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0] - corner_a[0]) ** 2 +
                         (corner_b[1] - corner_a[1]) ** 2)
    return distance


def rect_midpointx(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0]) / 4
    return midpoint_x


def rect_midpointy(corner_a, corner_b, corner_c, corner_d):
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1]) / 4
    return midpoint_y


def angle_between_lines(corner_a, corner_b, corner_c):
    slope_a = line_slope(corner_a, corner_b)
    slope_b = line_slope(corner_a, corner_c)

    if slope_a is not None and slope_b is not None and (1 + slope_a * slope_b) != 0:
        angle = math.atan((slope_a - slope_b) / (1 + slope_a * slope_b))
        return angle
    else:
        angle = 0
        return angle


def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1] - corner_a[1])/(corner_b[0] - corner_a[0])

        return slope

def line_angle(corner_a,corner_b):
    slope_a = line_slope(corner_a,corner_b)
    slope_b = 0
 
    if slope_a is not None:
        angle = math.atan((slope_a - slope_b)/(1+slope_a*slope_b))
        #angle = slope_a
        return angle
    else: 
        angle = 5
        return angle


