from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision
from entity_types.bin import Bin


class BinsContourEntity(VisionEntity):

    def init(self):
        self.adaptive_thresh_blocksize = 15
        self.adaptive_thresh = 8
        self.mid_sep = 50
        self.min_area = 4500
        self.max_area = 14000
        self.recent_id = 1
        self.trans_thresh = 25

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 0
        self.seencount_thresh = 2

    def process_frame(self, frame):
        # This is equivalent to the old routine, but it isn't actually necessary
        #height, width, depth = libvision.cv_to_cv2(frame).shape
        #self.debug_frame = np.zeros((height, width, 3), np.uint8)

        # Debug numpy is CV2
        self.debug_frame = libvision.cv_to_cv2(frame)

        # CV2 Transforms
        self.numpy_frame = self.debug_frame.copy()
        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 5)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv2.COLOR_BGR2HSV)

        (self.frame1, self.frame2, self.frame3) = cv2.split(self.numpy_frame)
        # Change the frame number to determine what channel to focus on
        self.numpy_frame = self.frame3

        # Thresholding
        self.numpy_frame = cv2.adaptiveThreshold(self.numpy_frame,
                              255,
                              cv2.ADAPTIVE_THRESH_MEAN_C,
                              cv2.THRESH_BINARY_INV,
                              self.adaptive_thresh_blocksize,
                              self.adaptive_thresh
                              )

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel = np.ones((2,2), np.uint8)
        self.numpy_frame = cv2.erode(self.numpy_frame, kernel)
        self.numpy_frame = cv2.dilate(self.numpy_frame, kernel)

        self.adaptive_frame = self.numpy_frame.copy()

        # Find contours
        contours, hierarchy = cv2.findContours(self.numpy_frame,
                                               cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE)
        self.raw_bins = []

        if len(contours) > 1:
            cnt = contours[0]
            cv2.drawContours(
                self.numpy_frame, contours, -1, (255, 255, 255), 3)
            self.masks = []
            pts = []

            for h, cnt in enumerate(contours):
                mask = np.zeros(self.numpy_frame.shape, np.uint8)
                cv2.drawContours(mask, [cnt], 0, 255, -1)
                #mean = cv2.mean(self.debug_numpy_fram), mask=mask)
                self.masks.append(mask)

                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

                # test aspect ratio & area, create bin if matches
                (x, y), (w, h), theta = rect
                if w > 0 and h > 0:
                    area = h * w
                    if self.min_area < area < self.max_area:
                        aspect_ratio = float(h) / w
                        if .4 < aspect_ratio < .6 or 1.8 < aspect_ratio < 2.2:   # Depending on the orientation of the bin, "width" may be flipped with height, thus needs 2 conditions                     
                            new_bin = Bin(tuple(box[0]), tuple(
                                box[1]), tuple(box[2]), tuple(box[3]))
                            new_bin.id = self.recent_id
                            new_bin.theta = -theta
                            self.recent_id = self.recent_id + 1
                            self.raw_bins.append(new_bin)

            # Removes bins that have centers too close to others (to prevent bins inside bins)
            for bin1 in self.raw_bins[:]:
                for bin2 in self.raw_bins[:]:
                    if bin1 is bin2:
                        continue
                    if bin1 in self.raw_bins and bin2 in self.raw_bins and \
                       math.fabs(bin1.midx - bin2.midx) < self.mid_sep and \
                       math.fabs(bin1.midy - bin2.midy) < self.mid_sep:
                        if bin1.area < bin2.area:
                            self.raw_bins.remove(bin1)
                        elif bin2.area < bin1.area:
                            self.raw_bins.remove(bin2)

        for bin in self.raw_bins:
            self.match_bins(bin)

        self.debug_final_frame = self.debug_frame

        self.sort_bins()
        self.draw_bins()

        self.return_output()

        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(self.adaptive_frame)

        svr.debug("processed", self.numpy_to_cv)
        svr.debug("adaptive", self.adaptive_to_cv)
        svr.debug("debug", self.debug_to_cv)

        # TODO, CLEAN THIS UP SOME
    def match_bins(self, target):
        found = 0
        for bin in self.candidates:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(bin.midy - target.midy) < self.trans_thresh:
                print bin.seencount
                bin.midx = target.midx
                bin.midy = target.midy
                bin.corner1 = target.corner1
                bin.corner2 = target.corner2
                bin.corner3 = target.corner3
                bin.corner4 = target.corner4
                print "still ", bin.seencount
                bin.seencount += 2
                print "new seencount ", bin.seencount
                bin.lastseen += 6
                found = 1
        for bin in self.confirmed:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(bin.midy - target.midy) < self.trans_thresh:
                target.id = bin.id
                bin = target
                bin.lastseen += 6
                found = 1
        if found == 0:
            self.candidates.append(target)
            target.lastseen + 3

        # TODO, CLEAN THIS UP SOME
    def sort_bins(self):
        for bin in self.candidates[:]:
            print "last seen is ", bin.lastseen
            print "seencount is ", bin.seencount
            bin.lastseen -= 1
            if bin.seencount >= self.seencount_thresh:
                self.confirmed.append(bin)
                print "confirmed appended"
            if bin.lastseen < self.lastseen_thresh:
                self.candidates.remove(bin)
        for bin in self.confirmed[:]:
            bin.lastseen -= 1
            if bin.lastseen < self.lastseen_thresh:
                self.confirmed.remove(bin)
                print "confirmed removed"

    def draw_bins(self):
        clr = (255, 0, 255)
        for bin in self.raw_bins:
            cv2.circle(self.debug_final_frame,
                       bin.corner1, 5, clr, -1)
            cv2.circle(self.debug_final_frame,
                       bin.corner2, 5, clr, -1)
            cv2.circle(self.debug_final_frame,
                       bin.corner3, 5, clr, -1)
            cv2.circle(self.debug_final_frame,
                       bin.corner4, 5, clr, -1)
            cv2.circle(self.debug_final_frame, (
                int(bin.midx), int(bin.midy)), 5, clr, -1)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(self.debug_final_frame, "theta=" + str(bin.theta), (int(bin.midx) - 50, int(bin.midy) + 20), font, .4, clr, 1, cv2.CV_AA)
