from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity, Container
import libvision


class Buoy(object):
    buoy_id = 0
    colors = {"red": (40, 0, 255),
              "green": (0, 255, 0),
              "blue": (255, 0, 0),
              "orange": (0, 200, 255),
              "unknown": (255, 255, 255),
              }

    def __init__(self, xcoor, ycoor, radius, color):
        self.output = Container()
        self.type = "buoy"
        self.centerx = xcoor
        self.centery = ycoor
        self.radius = radius
        self.color = color
        self.area = 0
        self.id = 0        # id identifies which buoy your looking at
        self.lastseen = 2  # how recently you have seen this buoy
        # how many times you have seen this buoy (if you see it enough it
        # becomes confirmed)
        self.seencount = 1

    def get_color(self):
        try:
            return Buoy.colors[self.color]
        except KeyError:
            return Buoy.colors["unknown"]


class BuoyHoughEntity(VisionEntity):

    def init(self):

        # Adaptive threshold variables
        self.adaptive_thresh_blocksize = 35
        self.adaptive_thresh = 15

        # Hough buoy variables
        self.inv_res_ratio = 2
        self.center_sep = 50
        self.upper_canny_thresh = 40 # 40 250 200
        self.acc_thresh = 80
        self.min_radius = 5
        self.max_radius = 100

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

        # for buoy1 in self.raw_buoys[:]:
        #     for buoy2 in self.raw_buoys[:]:
        #         if buoy1 is buoy2:
        #             continue
        #         if buoy1 in self.raw_buoys and buoy2 in self.raw_buoys and \
        #            math.fabs(buoy1.centerx - buoy2.centerx) > self.mid_sep and \
        #            math.fabs(buoy1.centery - buoy2.centery) > self.mid_sep:
        #             if buoy1.area < buoy2.area:
        #                 self.raw_buoys.remove(buoy1)
        #             elif buoy2.area < buoy1.area:
        #                 self.raw_buoys.remove(buoy2)
        #
        # for buoy in self.raw_buoys:
        #     self.match_buoys(buoy)
        #
        # self.sort_buoys()
        # self.draw_buoys()
        #
        # self.return_output()

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

    # TODO, CLEAN THIS UP SOME
    def match_buoys(self, target):
        found = 0
        for buoy in self.candidates:
            if math.fabs(buoy.centerx - target.centerx) < self.trans_thresh and \
               math.fabs(buoy.centery - target.centery) < self.trans_thresh:
                print buoy.seencount
                buoy.centerx = target.centerx
                buoy.centery = target.centery
                print "still ", buoy.seencount
                buoy.seencount += 2
                print "new seencount ", buoy.seencount
                buoy.lastseen += 6
                found = 1
        for buoy in self.confirmed:
            if math.fabs(buoy.centerx - target.centerx) < self.trans_thresh and \
               math.fabs(buoy.centery - target.centery) < self.trans_thresh:
                target.id = buoy.id
                buoy = target
                buoy.lastseen += 6
                found = 1
        if found == 0:
            self.candidates.append(target)
            target.lastseen + 3

        # TODO, CLEAN THIS UP SOME
    def sort_buoys(self):
        for buoy in self.candidates[:]:
            print "last seen is ", buoy.lastseen
            print "seencount is ", buoy.seencount
            buoy.lastseen -= 1
            if buoy.seencount >= self.seencount_thresh:
                self.confirmed.append(buoy)
                print "confirmed appended"
            if buoy.lastseen < self.lastseen_thresh:
                self.candidates.remove(buoy)
        for buoy in self.confirmed[:]:
            buoy.lastseen -= 1
            if buoy.lastseen < self.lastseen_thresh:
                self.confirmed.remove(buoy)
                print "confirmed removed"

    def draw_buoys(self):
        clr = (255, 0, 255)
        for buoy in self.raw_buoys:
            cv2.circle(self.debug_frame, (buoy.centerx, buoy.centery),
                       buoy.radius + 10, buoy.get_color(), 5)
            cv2.circle(
                self.debug_frame, (buoy.centerx, buoy.centery), 2, buoy.get_color(), 3)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(self.debug_final_frame, "theta=" + str(buoy.theta), (int(buoy.midx) - 50, int(buoy.midy) + 20), font, .4, clr, 1, cv2.CV_AA)
