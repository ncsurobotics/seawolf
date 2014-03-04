# pylint: disable=E1101
from __future__ import division
import math
import cv
#import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range
#import msvcrt
import random
       

class HedgeREntity(VisionEntity):

    def init(self):

        #Adaptive threshold parameters
        self.adaptive_thresh_blocksize = 29 #35 for just green #29 for just red
        self.adaptive_thresh = 23

        #Adaptive threshold parameters
        self.Gadaptive_thresh_blocksize = 35 #35 for just green #29 for just red
        self.Gadaptive_thresh = 6

        #Good features parameters

        self.max_corners = 18
        self.quality_level = .55

        self.min_distance = 15
        self.good_features_blocksize = 24
        
        #min and max angle in order to only accept rectangles
        self.angle_min = math.pi/2-.12
        self.angle_max = math.pi/2+.12
        self.angle_min2 = math.pi/2-.12
        self.angle_max2 = math.pi/2+.12

        #how close the sizes of parallel lines of a bin must be to eachother
        self.size_threshold = .5
        #How close to the ideal 2:1 ratio the bin sides must be
        self.ratio_threshold = .75
        
        #How far a bin may move and still be considered the same bin
        self.MaxTrans = 40

        self.MaxCornerTrans = 10

        #Minimum number the seencount can be before the bin is lost
        self.last_seen_thresh = 0

        self.last_seen_max = 20

        #How many times a bin must be seen to be accepted as a confirmed bin
        self.min_seencount = 3
 
        #How close the perimeter of a bin must be when compared to the perimeter of other bins
        self.perimeter_threshold = 0.25

        self.area_thresh = 3000 

        self.corners = []
        self.candidates = []
        self.confirmed  = []
        self.new = []
        self.angles = []


    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        self.test_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        Gframe = cv.CreateImage(cv.GetSize(frame), 8, 3)

        cv.Copy(frame, self.debug_frame)
        cv.Copy(frame, self.test_frame)
        cv.Copy(frame, Gframe)

	# Red frame

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 3) #1 for only green pvc #3 for red pvc
        cv.Copy(hsv, binary)
        cv.SetImageCOI(hsv, 0)
        
        #Adaptive Threshold
        cv.AdaptiveThreshold(binary, binary,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY_INV,
            self.adaptive_thresh_blocksize,
            self.adaptive_thresh,
        )

        # Morphology
        kernel = cv.CreateStructuringElementEx(5, 5, 3, 3, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(binary, binary, kernel, 1)
        cv.Dilate(binary, binary, kernel, 1)
        
        cv.CvtColor(binary, self.debug_frame, cv.CV_GRAY2RGB)

	#Green frame

        cv.Smooth(Gframe, Gframe, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(Gframe), 8, 3)
        binary = cv.CreateImage(cv.GetSize(Gframe), 8, 1)
        cv.CvtColor(Gframe, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1) #1 for only green pvc #3 for red pvc
        cv.Copy(hsv, binary)
        cv.SetImageCOI(hsv, 0)
        
        #Adaptive Threshold
        cv.AdaptiveThreshold(binary, binary,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY_INV,
            self.Gadaptive_thresh_blocksize,
            self.Gadaptive_thresh,
        )

        # Morphology
        kernel = cv.CreateStructuringElementEx(5, 5, 3, 3, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(binary, binary, kernel, 1)
        cv.Dilate(binary, binary, kernel, 1)
        
        cv.CvtColor(binary, Gframe, cv.CV_GRAY2RGB)
        
 
        svr.debug("Bins", self.debug_frame)
        svr.debug("Bins2", self.test_frame)
        svr.debug("Bins3", Gframe)



