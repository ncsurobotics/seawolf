import math
import time
import ctypes
import libvision
import cv

from entities.base import VisionEntity

FILTER_TYPE = cv.CV_GAUSSIAN
FILTER_SIZE = 11
MIN_BLOB_SIZE = 11

class LettersEntity(VisionEntity):

    name = "LettersEntity"
    camera_name = "down"

    def __init__(self):

        self.xcenter = None 
        self.ocenter = None
        self.xscale = None
        self.oscale = None

    def initialize_non_pickleable(self,debug=True):

        if debug:
            cv.NamedWindow("Binary")
            cv.NamedWindow("Filtered")

    def find(self, frame, debug=True):

        #import pdb 
        #pdb.set_trace()

        filtered = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Smooth(frame, filtered, FILTER_TYPE, FILTER_SIZE, FILTER_SIZE)  
        #detect correctly colored regions
        binary = libvision.cmodules.target_color_hsv.find_target_color_hsv(frame, 120, 250, 250, 800, 800, 1)
       # dilated = cv.CreateImage(cv.GetSize(binary), 8, 3)
       # cv.Dilate(binary, dilated,None, 1)

        libvision.cmodules.shape_detect.detect_letters(binary)

        if debug:
            cv.ShowImage("Binary",binary)
            cv.ShowImage("Filtered",filtered)

        return False 

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return False # "<ExampleEntity position=%s>" % self.position
