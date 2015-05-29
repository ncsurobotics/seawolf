from __future__ import division
import math
import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision
from entity_types.bin import Bin
import cv
import Image
import random


class BinsContourEntity(VisionEntity):

    def init(self):
        self.adaptive_thresh_blocksize = 15  # without canny, 15
        self.adaptive_thresh = 8  # without canny, 8
        self.mid_sep = 50
        self.min_area = 4500
        self.max_area = 14000
        self.recent_id = 1
        self.trans_thresh = 25

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 1
        self.seencount_thresh = 2
        self.lastseen_max = 5

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
                                                 self.adaptive_thresh)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel = np.ones((2,2), np.uint8)
        self.numpy_frame = cv2.erode(self.numpy_frame, kernel)
        self.numpy_frame = cv2.dilate(self.numpy_frame, kernel)

        self.adaptive_frame = self.numpy_frame.copy()

        # Find contours
        contours, hierarchy = cv2.findContours(self.numpy_frame,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

        self.raw_bins = []

        if len(contours) > 1:
            cnt = contours[0]
            cv2.drawContours(self.numpy_frame, contours, -1, (255, 255, 255), 3)

            for h, cnt in enumerate(contours):
                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

                # test aspect ratio & area, create bin if matches
                (x, y), (w, h), theta = rect
                if w > 0 and h > 0:
                    area = h * w
                    if self.min_area < area < self.max_area:
                        approx = cv2.approxPolyDP(
                            cnt, 0.01 * cv2.arcLength(cnt, True), True)

                        aspect_ratio = float(h) / w
                        # Depending on the orientation of the bin, "width" may be flipped with height, thus needs 2 conditions for each case
                        if 2 <= len(approx) < 12 and (.4 < aspect_ratio < .6 or 1.8 < aspect_ratio < 2.2):
                            new_bin = Bin(tuple(box[0]), tuple(
                                box[1]), tuple(box[2]), tuple(box[3]))
                            new_bin.id = self.recent_id
                            new_bin.area = area

                            # print "new bin created with slope: ", new_bin.line_slope

                            #print -theta
                            # if theta != 0:
                            #    new_bin.theta = np.pi*(-theta)/180
                            # else:
                            #    new_bin.theta = 0
                            self.recent_id += 1
                            self.raw_bins.append(new_bin)

        for bin in self.raw_bins:
            self.match_bins(bin)

        self.sort_bins()
        self.draw_bins()

        self.return_output()
        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(self.adaptive_frame)

        # svr.debug("processed", self.numpy_to_cv)
        # svr.debug("adaptive", self.adaptive_to_cv)
        # svr.debug("debug", self.debug_to_cv)
        self.debug_stream("debug", self.debug_frame)
        self.debug_stream("processed", self.numpy_frame)
        self.debug_stream("adaptive", self.adaptive_frame)
        for bin in self.confirmed:

            print type(bin.patch)
            self.debug_stream("Patch" + str(bin.id), bin.patch)
            # svr.debug("Patch"+str(bin.id),libvision.cv2_to_cv(bin.patch))
            print bin.id

            #svr.debug("Patch" + str(bin.id), bin.patch)

        # TODO, CLEAN THIS UP SOME
    def match_bins(self, target):
        found = 0
        for bin in self.confirmed:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(bin.midy - target.midy) < self.trans_thresh:
                bin.midx = target.midx
                bin.midy = target.midy
                bin.corner1 = target.corner1
                bin.corner2 = target.corner2
                bin.corner3 = target.corner3
                bin.corner4 = target.corner4
                bin.theta = target.theta
                bin.seencount += 3
                if bin.lastseen < self.lastseen_max:
                    bin.lastseen += 6
                found = 1

        for bin in self.candidates:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(bin.midy - target.midy) < self.trans_thresh:
                bin.midx = target.midx
                bin.midy = target.midy
                bin.corner1 = target.corner1
                bin.corner2 = target.corner2
                bin.corner3 = target.corner3
                bin.corner4 = target.corner4
                bin.theta = target.theta
                bin.seencount += 3
                if bin.lastseen < self.lastseen_max:
                    bin.lastseen += 6
                found = 1
        if found == 0:
            self.candidates.append(target)
            target.lastseen += 3

        # TODO, CLEAN THIS UP SOME
    def sort_bins(self):
        for bin in self.candidates[:]:
            bin.lastseen -= 2
            if bin.seencount >= self.seencount_thresh:
                self.confirmed.append(bin)
                self.candidates.remove(bin)
                print "confirmed appended"
            if bin.lastseen < self.lastseen_thresh:
                self.candidates.remove(bin)
        for bin in self.confirmed[:]:
            bin.lastseen -= 1
            if bin.lastseen < self.lastseen_thresh:
                self.confirmed.remove(bin)
                print "confirmed removed"

    def subimage(self, image, center, theta, width, height):
        print "theta is:", theta
        theta = theta
        image = libvision.cv2_to_cv(image)
        output_image = cv.CreateImage((int(width), int(height)), image.depth, image.nChannels)
        mapping = np.array([[np.cos(theta), -np.sin(theta), center[0]],
                            [np.sin(theta), np.cos(theta), center[1]]])
        map_matrix_cv = cv.fromarray(mapping)
        print mapping
        cv.GetQuadrangleSubPix(image, output_image, map_matrix_cv)
        return output_image

    def subimage2(self, image, center, theta, width, height):
        print "theta is:", theta
        M = cv2.getRotationMatrix2D(center, theta / np.pi * 180, 1.0)
        rotated = cv2.warpAffine(image, M, (image.shape[0], image.shape[1]))

        pts = [(center[0] - width / 2, center[1]), (center[0] + width / 2, center[1]), (center[0], center[1] - height / 2), (center[0], center[1] + height / 2)]

        cropped = rotated[int(center[1] - height / 2):int(center[1] + height / 2), int(center[0] - width / 2):int(center[0] + width / 2)]
        print cropped.shape
        cropped = cropped.copy()
        cv2.circle(rotated, center, 3, (255, 255, 255))
        for pt in pts:
            cv2.circle(rotated, (int(pt[0]), int(pt[1])), 4, (255, 0, 255))
        name = "Patches/" + str(int(theta * 1000)) + ".jpg"
        print name
        #cv2.imwrite(name, cropped)
        return cropped

    def draw_bins(self):
        self.ind_bins = []
        clr = (0, 0, 255)
        for bin in self.confirmed:

            bin.patch = self.subimage2(self.debug_frame, (int(bin.midx), int(bin.midy)),
                                       bin.theta, bin.width, bin.height)
            # cv.SaveImage('patch.jpg',patch)

            cv2.circle(self.debug_frame,
                       bin.corner1, 5, clr, -1)
            cv2.circle(self.debug_frame,
                       bin.corner2, 5, clr, -1)
            cv2.circle(self.debug_frame,
                       bin.corner3, 5, clr, -1)
            cv2.circle(self.debug_frame,
                       bin.corner4, 5, clr, -1)
            cv2.circle(self.debug_frame, (
                int(bin.midx), int(bin.midy)), 5, clr, -1)

            #cv2.rectangle(self.debug_frame, bin.corner1, bin.corner3, clr, 5)
            pts = np.array([bin.corner1, bin.corner2, bin.corner3, bin.corner4], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(self.debug_frame, [pts], True, (255, 0, 0), 4)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.debug_frame, "id=" + str(bin.id), (int(bin.midx) - 50, int(bin.midy) + 40), font, .8, clr, 1, cv2.CV_AA)

            cv2.putText(self.debug_frame, "corner1", (int(bin.corner1[0]), int(bin.corner1[1])), font, .8, clr, 1, cv2.CV_AA)

            # draw angle line
            m = math.tan(bin.theta)
            pt1 = (int(bin.midx), int(bin.midy))
            pt2 = (int(bin.midx + 10), int((10) * m + bin.midy))
            cv2.line(self.debug_frame, pt1, pt2, clr, 4, 8, 0)





# Angle is wrong. Fix it!!!!!!!!!ent
