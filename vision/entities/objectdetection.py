from __future__ import division
import math
import cv2
import numpy
import svr
from base import VisionEntity
#import libvision


class VisionObject(object):

    def __init__(self, variant, bin_id):
        self.variant = variant
        self.bin_id = bin_id
        self.id = 0        # id identifies which bin your looking at
        self.lastseen = 2  # how recently you have seen this bin
        # how many times you have seen this bin (if you see it enough it
        # becomes confirmed)
        self.seencount = 1


class LBPCascade(VisionEntity):

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

        self.cascade = cv2.CascadeClassifier("../../object.xml")

    def draw_rects(self, frame, rects, color):
            for x1, y1, x2, y2 in self.candidates:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        self.candidates = self.cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)

        self.candiates = cv2.detect(gray, self.cascade)
        vis = frame.copy()
        self.draw_rects(vis, self.candidates, (0, 255, 0))

        svr.debug('facedetect', vis)
