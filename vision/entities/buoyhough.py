from __future__ import division
import math
import cv2
import cv2.cv as cv
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

    def __init__(self, xcoor, ycoor, radius, color, id):
        self.type = "buoy"
        self.centerx = xcoor
        self.centery = ycoor
        self.radius = radius
        self.color = color
        self.area = 0
        self.id = id        # id identifies which buoy your looking at
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
        self.adaptive_thresh_blocksize = 55 # 35: yellow, orange, 55: green
        self.adaptive_thresh = 10   # 35: yellow, 25: orange, 10: green

        # Hough buoy variables
        self.inv_res_ratio = 2
        self.center_sep = 100
        self.upper_canny_thresh = 40 # 40
        self.acc_thresh = 50 # 20, 50 with green settings
        self.min_radius = 0
        self.max_radius = 50

        self.recent_id = 1
        self.trans_thresh = 20

        self.conf_trans_thresh = 150

        self.growth_thresh = 20

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 0
        self.seencount_thresh = 9

        self.next_id = 0

    def process_frame(self, frame):

        # Debug numpy is CV2
        self.debug_frame = libvision.cv_to_cv2(frame)

        # CV2 Transforms
        self.numpy_frame = self.debug_frame.copy()
        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 5)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv2.COLOR_BGR2HSV)

        self.hsv_frame = self.numpy_frame

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

        self.raw_circles = []
        self.raw_buoys = []
        self.raw_circles = cv2.HoughCircles(
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
  
        if self.raw_circles is not None and len(self.raw_circles[0] > 0):
            for circle in self.raw_circles[0]:
                (x, y, radius) = circle
                new_buoy = Buoy(x, y, radius, "unknown", self.next_id)
                self.next_id += 1
                self.raw_buoys.append(new_buoy) 
                self.match_buoys(new_buoy)

        self.sort_buoys()
        

        if self.confirmed is not None and len(self.confirmed) > 0:
            for buoy in self.confirmed:
                cv2.circle(self.debug_frame, (int(buoy.centerx), int(buoy.centery)),
                           int(buoy.radius) + 10, (255, 255, 255), 5)
                colorHue = self.hsv_frame[buoy.centery + buoy.radius/2,buoy.centerx][0]
                if (colorHue >= 0 and colorHue < 45) or colorHue >= 300:
                    cv2.putText(self.debug_frame,str(buoy.id)+"RED", (int(buoy.centerx), int(buoy.centery)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
                    buoy.color = "red"
                elif (colorHue >= 70 and colorHue < 180):
                    cv2.putText(self.debug_frame,str(buoy.id)+"GRE", (int(buoy.centerx), int(buoy.centery)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
                    if buoy.color != "red" and buoy.color != "yellow":
                        print "switched from ", buoy.color
                        buoy.color = "green"
                else:
                    cv2.putText(self.debug_frame,str(buoy.id)+"YEL", (int(buoy.centerx), int(buoy.centery)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
                    buoy.color = "yellow"




        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(self.adaptive_frame)

        svr.debug("processed", self.numpy_to_cv)
        svr.debug("adaptive", self.adaptive_to_cv)
        svr.debug("debug", self.debug_to_cv)



        # Convert to output format
        self.output.buoys = []
        if self.confirmed is not None and len(self.confirmed) > 0:
            for buoy in self.confirmed:
                buoy.theta = buoy.centerx
                buoy.phi = buoy.centery
                buoy.id = buoy.id
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
                buoy.seencount += 1
                print "new seencount ", buoy.seencount
                buoy.lastseen += 10
                found = 1
        for buoy in self.confirmed:
            if math.fabs(buoy.centerx - target.centerx) < self.conf_trans_thresh and \
               math.fabs(buoy.centery - target.centery) < self.conf_trans_thresh:
                target.id = buoy.id
                buoy = target
                buoy.lastseen += 10
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
            print self.hsv_frame[buoy.centery,buoy.centerx]
            buoy.lastseen -= 1
            if buoy.lastseen < self.lastseen_thresh:
                self.confirmed.remove(buoy)
                #self.candidates.append(buoy)
                buoy.lastseen += 3
                print "confirmed removed"
        for buoy1 in self.confirmed[:]:
            for buoy2 in self.confirmed[:]:
                if buoy1 in self.confirmed and buoy2 in self.confirmed and buoy1 is not buoy2:
                    if math.fabs(buoy1.centerx - buoy2.centerx) < self.conf_trans_thresh and \
                       math.fabs(buoy1.centery - buoy2.centery) < self.conf_trans_thresh:
                        if buoy1.id < buoy2.id:
                            self.confirmed.remove(buoy2)
                        else:
                            self.confirmed.remove(buoy1)

