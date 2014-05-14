from __future__ import division
import math
import cv
import cv2
import numpy
import svr
from base import VisionEntity
#import libvision
from entity_types.bin import Bin

def cv_to_cv2(frame):
    '''Convert a cv image into cv2 format.
        
    Keyword Arguments:
    frame -- a cv image
    Returns a numpy array that can be used by cv2.
    '''
    cv2_image = numpy.asarray(frame[:, :])
    return cv2_image


def cv2_to_cv(frame):
    '''Convert a cv2 image into cv format.
        
    Keyword Arguments:
    frame -- a cv2 numpy array representing an image.
    Returns a cv image.
    '''
    frame = frame.copy()  # makes the frame contiguous
    container = cv.fromarray(frame)
    cv_image = cv.GetImage(container)
    return cv_image


# class Bin(object):
#     bin_id = 0
#     """ an imaged bin b """

#     def __init__(self, corner1, corner2, corner3, corner4):
#         self.corner1 = corner1
#         self.corner2 = corner2
#         self.corner3 = corner3
#         self.corner4 = corner4
#         self.corners = [corner1, corner2, corner3, corner4]
#         self.midx = rect_midpointx(corner1, corner2, corner3, corner4)
#         self.midy = rect_midpointy(corner1, corner2, corner3, corner4)
#         self.area = line_distance(
#             corner1, corner2) * line_distance(corner1, corner4)
#         self.id = 0        # id identifies which bin your looking at
#         self.lastseen = 2  # how recently you have seen this bin
#         # how many times you have seen this bin (if you see it enough it
#         # becomes confirmed)
#         self.seencount = 1


# def line_distance(corner_a, corner_b):
#     distance = math.sqrt((corner_b[0] - corner_a[0]) ** 2 +
#                          (corner_b[1] - corner_a[1]) ** 2)
#     return distance


# def rect_midpointx(corner_a, corner_b, corner_c, corner_d):
#     midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0]) / 4
#     return midpoint_x


# def rect_midpointy(corner_a, corner_b, corner_c, corner_d):
#     midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1]) / 4
#     return midpoint_y


class BlobTesting(VisionEntity):

    def init(self):

        self.adaptive_thresh_blocksize = 15
        self.adaptive_thresh = 7
        self.mid_sep = 50
        self.min_area = 10000

        self.recent_id = 1

        self.trans_thresh = 25

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 0
        self.seencount_thresh = 2

    def process_frame(self, frame):
        # Creation of frames
        self.debug_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, self.debug_frame)
        self.debug_numpy_frame = cv_to_cv2(self.debug_frame)

        # CV2 Transforms
        self.numpy_frame = cv_to_cv2(self.debug_frame)

        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 7)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv.CV_BGR2HSV)

        [self.frame1, self.frame2, self.frame3] = numpy.dsplit(
            self.numpy_frame, 3)
        #Change the frame number to determine what channel to focus on
        self.numpy_frame = self.frame3

        '''Temporarily converts the image to a cv frame to do the adaptive threshold '''
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

        self.adaptive_frame = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.Copy(self.temp_cv2frame, self.adaptive_frame)
        '''Returns the frame to a cv2 image'''
        self.numpy_frame = cv_to_cv2(self.temp_cv2frame)

        '''Begins finding contours'''
        contours, hierarchy = cv2.findContours(
            self.numpy_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.raw_bins = []
        if len(contours) > 1:
            cnt = contours[0]
            cv2.drawContours(
                self.numpy_frame, contours, -1, (255, 255, 255), 3)
            self.masks = []
            pts = []
            for h, cnt in enumerate(contours):
                mask = numpy.zeros(self.numpy_frame.shape, numpy.uint8)
                cv2.drawContours(mask, [cnt], 0, 255, -1)
                mean = cv2.mean(cv_to_cv2(self.debug_frame), mask=mask)
                self.masks.append(mask)

                hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = numpy.int0(box)
                new_bin = Bin(tuple(box[0]), tuple(
                    box[1]), tuple(box[2]), tuple(box[3]))
                new_bin.id = self.recent_id
                self.recent_id = self.recent_id + 1
                self.raw_bins.append(new_bin)
                for pt in box:
                    type(tuple(pt))
                    cv2.circle(self.numpy_frame, tuple(
                        pt), 5, (255, 255, 255), -1, 8, 0)
                    pts.append(pt)

                '''Removes bins that have centers too close to others (to prevent bins inside bins), and bins that are too small'''
                for bin1 in self.raw_bins[:]:
                    for bin2 in self.raw_bins[:]:
                        if bin1 in self.raw_bins and bin2 in self.raw_bins and math.fabs(bin1.midx - bin2.midx) < self.mid_sep and math.fabs(bin1.midy - bin2.midy) < self.mid_sep:
                            if bin1.area < bin2.area:
                                self.raw_bins.remove(bin1)
                            elif bin2.area < bin1.area:
                                self.raw_bins.remove(bin2)
                        if bin1 in self.raw_bins and bin2 in self.raw_bins:
                            if bin1.area < self.min_area:
                                self.raw_bins.remove(bin1)
                            if bin2.area < self.min_area and bin2 in self.raw_bins:
                                self.raw_bins.remove(bin2)

        for bin in self.raw_bins:
            self.match_bins(bin)
        self.sort_bins()

        self.numpy_to_cv = cv2_to_cv(self.numpy_frame)
        self.debug_final_frame = cv2_to_cv(self.debug_numpy_frame)
        self.draw_bins()

        svr.debug("CV", self.debug_final_frame)
        svr.debug("CV2", self.numpy_to_cv)
        svr.debug("Adaptive", self.adaptive_frame)

    def match_bins(self, target):
        found = 0
        for bin in self.candidates:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and math.fabs(bin.midy - target.midy) < self.trans_thresh:
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
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and math.fabs(bin.midy - target.midy) < self.trans_thresh:
                target.id = bin.id
                bin = target
                bin.lastseen += 6
                found = 1
        if found == 0:
            self.candidates.append(target)
            target.lastseen + 3

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
        for bin in self.raw_bins:
            cv.Circle(self.debug_final_frame,
                      bin.corner1, 5, (0, 255, 0), -1, 8, 0)
            cv.Circle(self.debug_final_frame,
                      bin.corner2, 5, (0, 255, 0), -1, 8, 0)
            cv.Circle(self.debug_final_frame,
                      bin.corner3, 5, (0, 255, 0), -1, 8, 0)
            cv.Circle(self.debug_final_frame,
                      bin.corner4, 5, (0, 255, 0), -1, 8, 0)
            cv.Circle(self.debug_final_frame, (
                int(bin.midx), int(bin.midy)), 5, (0, 255, 0), -1, 8, 0)
