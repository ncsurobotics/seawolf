from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision

from base import VisionEntity, Container


class Buoy(object):
    buoy_id = 0
    colors = {"red": (40, 0, 255),
              "green": (0, 255, 0),
              "blue": (255, 0, 0),
              "orange": (0, 200, 255),
              "unknown": (255, 255, 255),
              }

    def __init__(self, xcoor, ycoor, radius, color):
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


class BuoyContourEntity(VisionEntity):

    def init(self):
        self.output = Container()
        self.adaptive_thresh_blocksize = 31
        self.adaptive_thresh = 10
        self.min_area = 20
        self.max_area = 5000
        self.mid_sep = 50
        self.recent_id = 1
        self.trans_thresh = 30

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 0
        self.seencount_thresh = 2

    def process_frame(self, frame):
        # This is equivalent to the old routine, but it isn't actually necessary
        #height, width, depth = libvision.cv_to_cv2(frame).shape
        #self.debug_frame = np.zeros((height, width, 3), np.uint8)

        inv_res_ratio = 2
        center_sep = 100
        upper_canny_thresh = 40  # 40
        acc_thresh = 10  # 20, 50 with green settings
        min_radius = 3
        max_radius = 50

        # Debug numpy is CV2
        debug_frame = libvision.cv_to_cv2(frame)

        svr.debug("original", frame)

        # CV2 Transforms
        numpy_frame = debug_frame.copy()
        numpy_frame = cv2.medianBlur(numpy_frame, 5)
        numpy_frame = cv2.cvtColor(numpy_frame, cv2.COLOR_BGR2HSV)

        # Kernel for erosion/dilation
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # Split into HSV frames
        (h_frame, s_frame, v_frame) = cv2.split(numpy_frame)

        # Run inverse adaptive thresh on saturation channel
        s_adapt_thresh = cv2.adaptiveThreshold(s_frame,
                                               255,
                                               cv2.ADAPTIVE_THRESH_MEAN_C,
                                               cv2.THRESH_BINARY_INV,
                                               47,
                                               10)

        # Erode and dilate the value frame
        s_eroded = cv2.erode(s_adapt_thresh, kernel)
        s_dilated = cv2.dilate(s_eroded, kernel)

        # Threshold the value frame
        _, v_thresh = cv2.threshold(v_frame, 250, 255, cv2.THRESH_BINARY)

        # Erode and dilate the value frame
        v_eroded = cv2.erode(v_thresh, kernel)
        v_dilated = cv2.dilate(v_eroded, kernel)

        s_contours = s_dilated.copy()

        # Find contours on the dilated saturation channel
        s_cnt, hy = cv2.findContours(
            s_dilated,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        v_contours = v_dilated.copy()

        # Find contours on the dilated
        v_cnt, hy = cv2.findContours(
            v_dilated,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(s_contours) > 0:
            cv2.drawContours(s_contours, s_cnt, -1, (255, 255, 255), 3)

        if len(v_contours) > 0:
            cv2.drawContours(v_contours, v_cnt, -1, (255, 255, 255), 3)

        s_circles = cv2.HoughCircles(
            s_contours,
            cv2.cv.CV_HOUGH_GRADIENT,
            inv_res_ratio,
            center_sep,
            np.array([]),
            upper_canny_thresh,
            acc_thresh,
            min_radius,
            max_radius,
        )

        v_circles = cv2.HoughCircles(
            v_contours,
            cv2.cv.CV_HOUGH_GRADIENT,
            inv_res_ratio,
            center_sep,
            np.array([]),
            upper_canny_thresh,
            acc_thresh,
            min_radius,
            max_radius,
        )

        for circle in s_circles[0]:
            (x, y, radius) = circle
            cv2.circle(debug_frame, (int(x), int(y)), int(radius) + 10, (0, 255, 0), 5)

        # for circle in v_circles[0]:
        #     (x, y, radius) = circle
        #     cv2.circle(debug_frame, (int(x), int(y)), int(radius) + 10, (0, 0, 255), 5)


        # debug_to_cv = libvision.cv2_to_cv(v_circles)
        # svr.debug("v_frame", debug_to_cv)

        # debug_to_cv = libvision.cv2_to_cv(s_circles)
        # svr.debug("s_frame", debug_to_cv)

        debug_to_cv = libvision.cv2_to_cv(debug_frame)
        svr.debug("debug_frame", debug_to_cv)

    #   self.numpy_frame = self.frame2
    # Thresholding
    # self.numpy_frame = cv2.adaptiveThreshold(self.numpy_frame,
    # 255,
    # cv2.ADAPTIVE_THRESH_MEAN_C,
    # cv2.THRESH_BINARY_INV,
    # self.adaptive_thresh_blocksize,
    # self.adaptive_thresh)

    #     _, self.numpy_frame = cv2.threshold(self.numpy_frame, 7, 255, cv2.THRESH_BINARY_INV)

    #     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    #     kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    # kernel = np.ones((2,2), np.uint8)
    #     self.numpy_frame = cv2.erode(self.numpy_frame, kernel)
    #     self.numpy_frame = cv2.dilate(self.numpy_frame, kernel2)

    #     self.adaptive_frame = self.numpy_frame.copy()

    # Find contours
    #     contours, hierarchy = cv2.findContours(self.numpy_frame,
    #                                            cv2.RETR_EXTERNAL,
    #                                            cv2.CHAIN_APPROX_SIMPLE)
    #     self.raw_buoys = []

    #     if len(contours) > 0:
    #         cnt = contours[0]
    #         cv2.drawContours(
    #             self.numpy_frame, contours, -1, (255, 255, 255), 3)

    #         for h, cnt in enumerate(contours):
    #             approx = cv2.approxPolyDP(
    #                 cnt, 0.01 * cv2.arcLength(cnt, True), True)

    #             center, radius = cv2.minEnclosingCircle(cnt)
    #             x, y = center

    #             if len(approx) > 12:
    #                 if (radius > 30):
    #                     new_buoy = Buoy(int(x), int(y), int(radius), "unknown")
    #                     new_buoy.id = self.recent_id
    #                     self.recent_id += 1
    #                     self.raw_buoys.append(new_buoy)
    #                     cv2.drawContours(
    #                         self.numpy_frame, [cnt], 0, (0, 0, 255), -1)
    #                     self.raw_buoys.append(new_buoy)

    #     for buoy1 in self.raw_buoys[:]:
    #         for buoy2 in self.raw_buoys[:]:
    #             if buoy1 is buoy2:
    #                 continue
    #             if buoy1 in self.raw_buoys and buoy2 in self.raw_buoys and \
    #                math.fabs(buoy1.centerx - buoy2.centerx) > self.mid_sep and \
    #                math.fabs(buoy1.centery - buoy2.centery) > self.mid_sep:
    #                 if buoy1.radius < buoy2.radius:
    #                     self.raw_buoys.remove(buoy1)
    #                 elif buoy2.radius < buoy1.radius:
    #                     self.raw_buoys.remove(buoy2)

    #     for buoy in self.raw_buoys:
    #         self.match_buoys(buoy)

    #     self.sort_buoys()
    #     self.draw_buoys()

    #     self.return_output()

    #     self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
    #     self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
    #     self.adaptive_to_cv = libvision.cv2_to_cv(self.adaptive_frame)

    #     svr.debug("processed", self.numpy_to_cv)
    #     svr.debug("adaptive", self.adaptive_to_cv)
    #     svr.debug("debug", self.debug_to_cv)

    # Convert to output format
    #     self.output.buoys = []
    #     if self.raw_buoys is not None and len(self.raw_buoys) > 0:
    #         for buoy in self.raw_buoys:
    #             x = buoy.centerx
    #             y = buoy.centery
    #             buoy = Container()
    #             buoy.theta = x
    #             buoy.phi = y
    #             buoy.id = 1
    #             self.output.buoys.append(buoy)

    #     if self.output.buoys:
    #         self.return_output()
    #     return self.output

    # TODO, CLEAN THIS UP SOME
    # def match_buoys(self, target):
    #     found = 0
    #     for buoy in self.candidates:
    #         if math.fabs(buoy.centerx - target.centerx) < self.trans_thresh and \
    #            math.fabs(buoy.centery - target.centery) < self.trans_thresh:
    #             print buoy.seencount
    #             buoy.centerx = target.centerx
    #             buoy.centery = target.centery
    #             print "still ", buoy.seencount
    #             buoy.seencount += 2
    #             print "new seencount ", buoy.seencount
    #             buoy.lastseen += 6
    #             found = 1
    #     for buoy in self.confirmed:
    #         if math.fabs(buoy.centerx - target.centerx) < self.trans_thresh and \
    #            math.fabs(buoy.centery - target.centery) < self.trans_thresh:
    #             target.id = buoy.id
    #             buoy = target
    #             buoy.lastseen += 6
    #             found = 1
    #     if found == 0:
    #         self.candidates.append(target)
    #         target.lastseen + 3

    # TODO, CLEAN THIS UP SOME
    # def sort_buoys(self):
    #     for buoy in self.candidates[:]:
    #         print "last seen is ", buoy.lastseen
    #         print "seencount is ", buoy.seencount
    #         buoy.lastseen -= 1
    #         if buoy.seencount >= self.seencount_thresh:
    #             self.confirmed.append(buoy)
    #             print "confirmed appended"
    #         if buoy.lastseen < self.lastseen_thresh:
    #             self.candidates.remove(buoy)
    #     for buoy in self.confirmed[:]:
    #         buoy.lastseen -= 1
    #         if buoy.lastseen < self.lastseen_thresh:
    #             self.confirmed.remove(buoy)
    #             print "confirmed removed"

    # def draw_buoys(self):
    #     clr = (255, 0, 255)
    #     for buoy in self.raw_buoys:
    #         cv2.circle(self.debug_frame, (buoy.centerx, buoy.centery),
    #                    buoy.radius + 10, buoy.get_color(), 5)
    #         cv2.circle(
    #             self.debug_frame, (buoy.centerx, buoy.centery), 2, buoy.get_color(), 3)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(self.debug_final_frame, "theta=" + str(buoy.theta), (int(buoy.midx) - 50, int(buoy.midy) + 20), font, .4, clr, 1, cv2.CV_AA)
