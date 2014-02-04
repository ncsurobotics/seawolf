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
    frame = frame.copy() #makes the frame contiguous
    container = cv.fromarray(frame)
    cv_image = cv.GetImage(container)
    return cv_image


class BlobTesting(VisionEntity):
    def init(self):

        self.adaptive_thresh_blocksize = 41  # 27 before competition
        self.adaptive_thresh = 4 # 23 before competition #9 at competition #11 after hough line changes



    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        og_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, self.debug_frame)
        cv.Copy(self.debug_frame, og_frame)
        self.debug_numpy_frame = cv_to_cv2(self.debug_frame)

        #CV2 Transforms        
        self.numpy_frame = cv_to_cv2(self.debug_frame)

        self.numpy_frame = cv2.medianBlur(self.numpy_frame,7)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame,cv.CV_BGR2HSV) 
        #cv2.mixChannels(self.numpy_frame,self.numpy_single,fromTo, 1)
        #height, width, depth = self.numpy_frame.shape
        #print height, width, depth
        
        [self.frame1,self.frame2,self.frame3] = numpy.dsplit(self.numpy_frame,3)
        self.numpy_frame = self.frame1
        print self.frame1.shape
        
        self.temp_cv2frame = cv2_to_cv(self.numpy_frame)
        
        cv.AdaptiveThreshold(self.temp_cv2frame, self.temp_cv2frame,
                             255,
                             cv.CV_ADAPTIVE_THRESH_MEAN_C,
                             cv.CV_THRESH_BINARY_INV,
                             self.adaptive_thresh_blocksize,
                             self.adaptive_thresh,
        )
        
        kernel = cv.CreateStructuringElementEx(5, 5, 3, 3, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(self.temp_cv2frame, self.temp_cv2frame, kernel, 1)
        cv.Dilate(self.temp_cv2frame, self.temp_cv2frame, kernel, 1)
        self.numpy_frame = cv_to_cv2(self.temp_cv2frame)
        
        #cv2.adaptiveThreshold(self.numpy_frame,self.adaptive_thresh,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,self.adaptive_thresh_blocksize,3,self.numpy_frame)
        




        '''
        contours, hierarchy = cv2.findContours(self.numpy_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)>1: 
            cnt = contours[0]
            
            cv2.Contours(self.numpy_frame,contours,-1,(255,255,255),3)
            #cv2.drawContours(self.debug_numpy_frame,contours,-1,(0,255,0),3)

            #for h,cnt in enumerate(contours):
            #    mask = numpy.zeros(imgray.shape,np.uint8)
            #    cv2.drawContours(mask,[cnt],0,255,-1)
            #    mean = cv2.mean(im,mask = mask)
            
            hull = cv2.convexHull(cnt)

            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = numpy.int0(box)
            print box
            
            #if len(box > 1):
            #    cv2.drawContours(self.numpy_frame,box,0,(255,255,255),2)
        '''




        

 
        print type(self.numpy_frame)
        self.numpy_to_cv = cv2_to_cv(self.numpy_frame)
        #print type(self.numpy_to_cv)
        self.debug_final_frame = cv2_to_cv(self.debug_numpy_frame)
        
        

        svr.debug("CV", self.debug_final_frame)
        svr.debug("CV2", self.numpy_to_cv)
        #svr.debug("Original", og_frame)


