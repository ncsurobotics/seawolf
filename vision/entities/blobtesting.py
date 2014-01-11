from __future__ import division
import math

import cv
import cv2

import numpy

import svr

from base import VisionEntity
import libvision


def cv_to_cv2(frame):
    '''Convert a cv image into cv2 format.
        
    Keyword Arguments:
    frame -- a cv image
    Returns a numpy array that can be used by cv2.
    '''
    cv2_image = numpy.asarray(frame[:,:])
    return cv2_image
        
        
def cv2_to_cv(frame):
    '''Convert a cv2 image into cv format.
        
    Keyword Arguments:
    frame -- a cv2 numpy array representing an image.
    Returns a cv image.
    '''
    container = cv.fromarray(frame)
    cv_image = cv.GetImage(container)
    return cv_image


class BlobTesting(VisionEntity):
    def init(self):

        self.adaptive_thresh_blocksize = 35  # 27 before competition
        self.adaptive_thresh = 7  # 23 before competition #9 at competition #11 after hough line changes



    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        og_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, self.debug_frame)
        cv.Copy(self.debug_frame, og_frame)

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1)  
        cv.Copy(hsv, binary)
        cv.SetImageCOI(hsv, 0)

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

        # Get Edges
        #cv.Canny(binary, binary, 30, 40)

        cv.CvtColor(binary, self.debug_frame, cv.CV_GRAY2RGB)
        
        self.numpy_frame = cv_to_cv2(self.debug_frame)
        self.numpy_frame = self.numpy_frame[:,:,1]
        print self.numpy_frame.shape
        
        contours, hierarchy = cv2.findContours(self.numpy_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


        #contours, hierarchy = cv2.findContours(self.numpy_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


        svr.debug("Bins", self.debug_frame)
        #svr.debug("Original", og_frame)


