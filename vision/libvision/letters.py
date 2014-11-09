
import ctypes
from . import cmodules


class Rect(object):

    def __init__(self, crect):
        # area of the rectangle
        self.area = crect.contents.area

        # center of the rectangle
        self.center = (crect.contents.c_x, crect.contents.c_y)

        # direction towards the skinny edge
        self.theta = crect.contents.theta


def find_bins(img_in):
    """"find 2x1 size rectangles in image"""
    num_rects = ctypes.c_int()
    crects = cmodules.shape_detect.find_bins(img_in, ctypes.pointer(num_rects))

    rects = [Rect(crects[i]) for i in range(0, num_rects.value)]
    cmodules.shape_detect.free_bins(crects, num_rects)

    return rects
