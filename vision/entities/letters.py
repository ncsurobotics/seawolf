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
            cv.NamedWindow("Filtered")
            cv.NamedWindow("Binary")
            cv.NamedWindow("Indexed")

    def find(self, frame, debug=True):

        #import pdb 
        #pdb.set_trace()

        #smooth the image
        filtered = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Smooth(frame, filtered, FILTER_TYPE, FILTER_SIZE, FILTER_SIZE)  

        #detect correctly colored regions
        #binary = libvision.cmodules.target_color_hsv.find_target_color_hsv(filtered, 0, 250, 250, 800, 800, 1)
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(filtered, 250, 0, 0, 800, 800, 1.5)

        blob_indexed = cv.CreateImage(cv.GetSize(binary), 8, 1)
        blobs = libvision.blob.find_blobs(binary,blob_indexed,50,1)

        for i, blob in enumerate(blobs):
            #check for an x
            x_sighted = libvision.cmodules.shape_detect.match_X(blob_indexed, i+1, blob.centroid[0], blob.centroid[1],blob.roi[0],blob.roi[1],blob.roi[2],blob.roi[3])
            #check for an 0

        if debug:
            cv.ShowImage("Binary",binary)
            cv.ShowImage("Indexed",blob_indexed)
            cv.ShowImage("Filtered",filtered)

        return False 

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return False # "<ExampleEntity position=%s>" % self.position
