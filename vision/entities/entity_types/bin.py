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
        self.midx = rect_midpointx(corner1, corner2, corner3, corner4)
        self.midy = rect_midpointy(corner1, corner2, corner3, corner4)
        self.area = line_distance(
            corner1, corner2) * line_distance(corner1, corner4)
        self.id = 0        # id identifies which bin your looking at
        self.lastseen = 2  # how recently you have seen this bin
        # how many times you have seen this bin (if you see it enough it
        # becomes confirmed)
        self.seencount = 1


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
