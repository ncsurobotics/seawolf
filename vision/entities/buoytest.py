

from __future__ import division
import math

import cv

from entities.base import VisionEntity
import libvision
from sw3.util import circular_average

class BuoyTestEntity(VisionEntity):

    def init(self):

        # Thresholds
        self.minsize = 20
        self.maxsize = 60

        if self.debug:
            #windows
            cv.NamedWindow("Buoy Debug")

    def process_frame(self, frame):

        # Get Channels
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3);
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        grey = libvision.misc.get_channel(hsv, 2)

        # load a haar classifier
        hc = cv.Load("/home/seawolf/software/seawolf5/vision/buoy_cascade_4.xml")

        #use classifier to detect buoys
        self.minsize = 20
        minsize = (int(self.minsize), int(self.minsize))
        maxsize = (int(self.maxsize), int(self.maxsize))
        buoys = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), min_size = minsize, max_size = maxsize)

        #draw rectangles and compute average buoys size
        avg_w = 0
        for (x,y,w,h),n in buoys:
            cv.Rectangle(grey, (x,y), (x+w, y+h), 255)
            avg_w = avg_w + w
        if buoys:
            avg_w = avg_w / len(buoys)
            self.minsize = int(avg_w * .7)
            self.maxsize = int(avg_w * 1.3)

        if self.debug:
            #show debug frame
            cv.ShowImage("Buoy Debug", grey)

            #print buoy size
            if buoys:
                print "buoy size = ", avg_w

    def __repr__(self):
        return "<BuoyEntity>"
