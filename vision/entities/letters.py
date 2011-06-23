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
            #cv.NamedWindow("Filtered")
            cv.NamedWindow("Binary")
            #cv.NamedWindow("Indexed")
            #cv.NamedWindow("Python Debug")
            #cv.NamedWindow("Features")

    def find(self, frame, debug=True):

        #import pdb 
        #pdb.set_trace()

        if debug:
            debug = cv.CreateImage(cv.GetSize(frame), 8, 3)
            debug = cv.CloneImage(frame)

        #smooth the image
        #filtered = cv.CreateImage(cv.GetSize(frame), 8, 3)
        #cv.Smooth(frame, filtered, FILTER_TYPE, FILTER_SIZE, FILTER_SIZE)  

        #detect correctly colored regions
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(frame, 250, 0, 0, 2000, 800, 1)

        #collect blobs
        blob_indexed = cv.CreateImage(cv.GetSize(binary), 8, 1)
        blobs = libvision.blob.find_blobs(binary,blob_indexed,50,2)

        #analyze blobs
        for i, blob in enumerate(blobs):
            #check if the blob is a letter  
            letter_found = libvision.cmodules.shape_detect.match_letters(blob_indexed, i+1, blob.centroid[0], blob.centroid[1],blob.roi[0],blob.roi[1],blob.roi[2],blob.roi[3])

            if debug and letter_found != 0:
                center = (blob.roi[0] + blob.roi[2]/2 , blob.roi[1] + blob.roi[3]/2)
                color = (0,0,0)
                if letter_found == 1:
                    color = (0,255,0)
                if letter_found == 2:
                    color = (0,0,255)
                cv.Circle(debug,center, 5, color, 2, 8, 0) 
        '''
        #do feature detection
        grayscale = cv.CreateImage(cv.GetSize(frame),cv.IPL_DEPTH_8U,1)
        cv.CvtColor(frame,grayscale,cv.CV_RGB2GRAY)
        evalues = cv.CreateImage(cv.GetSize(frame),cv.IPL_DEPTH_32F,1)
        temp = cv.CreateImage(cv.GetSize(frame),cv.IPL_DEPTH_32F,1)
        corner_count = 10
        quality_level = .1
        min_distance = 50.0
        block_size = 3
        corners = cv.GoodFeaturesToTrack(grayscale, evalues, temp, corner_count, quality_level, min_distance, None, block_size, 0)

        if debug:
            #mark corners on the features image
            features = cv.CreateImage(cv.GetSize(frame),8,3)
            features = cv.CloneImage(frame)
            for i,pairs in enumerate(corners):
                corner_color = (255,255,0)
                cv.Circle(features, pairs, 5, corner_color, 1, 3,0)
        '''
        if debug:
#            cv.ShowImage("Features", features)
            cv.ShowImage("Binary",binary)
            #cv.ShowImage("Indexed",blob_indexed)
            #cv.ShowImage("Filtered",filtered)
            #cv.ShowImage("Python Debug",debug)

        return False 

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return False # "<ExampleEntity position=%s>" % self.position
