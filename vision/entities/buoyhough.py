from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity, Container
import libvision


class BuoyHoughEntity(VisionEntity):

    def init(self):

        # Adaptive threshold variables
        self.adaptive_thresh_blocksize = 21 # 35: yellow, orange, 55: green
        self.adaptive_thresh = 6   # 35: yellow, 25: orange, 10: green

        # Hough buoy variables
        self.inv_res_ratio = 2
        self.center_sep = 100
        self.upper_canny_thresh = 40 # 40
        self.acc_thresh = 10 # 20, 50 with green settings
        self.min_radius = 0
        self.max_radius = 50

    def init(self):
        self.adaptive_thresh_blocksize = 29
        self.adaptive_thresh = 15
        self.min_area = 500
        self.max_area = 5000
        self.mid_sep = 50
        self.recent_id = 1
        self.trans_thresh = 30

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 0
        self.seencount_thresh = 2

    def process_frame(self, frame):

        # Debug numpy is CV2
        self.debug_frame = libvision.cv_to_cv2(frame)

        # CV2 Transforms
        self.numpy_frame = self.debug_frame.copy()
        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 5)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv2.COLOR_BGR2HSV)

        (self.frame1, self.frame2, self.frame3) = cv2.split(self.numpy_frame)
        # Change the frame number to determine what channel to focus on
        self.numpy_frame = self.frame2

        # Thresholding
        self.numpy_frame = cv2.adaptiveThreshold(self.numpy_frame,
                                                 255,
                                                 cv2.ADAPTIVE_THRESH_MEAN_C,
                                                 cv2.THRESH_BINARY_INV,
                                                 self.adaptive_thresh_blocksize,
                                                 self.adaptive_thresh)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))

        self.numpy_frame = cv2.erode(self.numpy_frame, kernel)
        self.numpy_frame = cv2.dilate(self.numpy_frame, kernel2)

        self.adaptive_frame = self.numpy_frame.copy()

        self.numpy_frame = cv2.Canny(self.adaptive_frame, 100, 250, apertureSize=3)

        self.raw_buoys = cv2.HoughCircles(
                                self.numpy_frame, 
                                cv2.cv.CV_HOUGH_GRADIENT,
                                self.inv_res_ratio, 
                                self.center_sep,
                                np.array([]),
                                self.upper_canny_thresh,
                                self.acc_thresh,
                                self.min_radius,
                                self.max_radius,
                        )

        if self.raw_buoys is not None and len(self.raw_buoys[0]) > 0:
            for buoy in self.raw_buoys[0]:
                (x, y, radius) = buoy
                cv2.circle(self.debug_frame, (int(x), int(y)),
                           int(radius) + 10, (255, 255, 255), 5)


        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(self.adaptive_frame)

        svr.debug("processed", self.numpy_to_cv)
        svr.debug("adaptive", self.adaptive_to_cv)
        svr.debug("debug", self.debug_to_cv)



        # Convert to output format
        self.output.buoys = []
        if self.raw_buoys is not None and len(self.raw_buoys[0]) > 0:
            for buoy in self.raw_buoys[0]:
                (x, y, radius) = buoy
                buoy = Container()
                buoy.theta = x
                buoy.phi = y
                buoy.id = 1
                self.output.buoys.append(buoy)

        if self.output.buoys:
            self.return_output()
        return self.output

