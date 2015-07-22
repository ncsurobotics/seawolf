# pylint: disable=E1101
from __future__ import division
import math

import cv
import os
import svr

from base import VisionEntity
import libvision
from sw3.util import circular_average

# maximum buoy translation allowed between frames
MAX_X_TRANS = 30
MAX_Y_TRANS = 30

# maximum allowed change in width
MAX_CHANGE_WIDTH = 40

# how many frames a buoy may go missing before flagged as lost
CONFIRMED_BUOY_TIMEOUT = 5

# how many consequtive frames a candidate is allowed to go missing
CANDIDATE_BUOY_TIMEOUT = 3

# required seen threshold to accept a buoy
CANDIDATE_SEEN_THRESH = 2

# dictionaries of colors
COLORS = {0: cv.RGB(127, 127, 127), 1: cv.RGB(255, 0, 0), 2: cv.RGB(0, 255, 0), 3: cv.RGB(255, 255, 0)}


class Buoy(object):

    '''an imaged buoy'''

    def __init__(self):

        # Identification Number
        self.id = None

        # coordinate of upper left corner
        self.x = None
        self.y = None

        # width
        self.width = None

        # Which Color we believe the buoy to be
        self.color = None

        # Frames since last sighting
        self.last_seen = None

        # Keeps track of how often we have seen this buoy
        self.seen_count = None

        # Color used in debug windows
        self.debug_color = None


class BuoyTestEntity(VisionEntity):

    def init(self):

        # Total Number of Buoys Found
        self.buoy_count = 0

        # Thresholds
        self.minsize = 20
        self.maxsize = 40
        # Buoy Classes
        self.new = []
        self.candidates = []
        self.confirmed = []
        self.lost = []
        #self.debug = True

        if self.debug:
           # windows
        #    cv.NamedWindow("BuoyTest")

            # random number generator used for choosing debug colors
            self.rng = cv.RNG()

    def process_frame(self, frame):

        # Get Channels
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        grey = libvision.misc.get_channel(hsv, 2)

        # load a haar classifier
        #hc = cv.Load("/home/seawolf/software/seawolf5/vision/output.xml")
        hc = cv.Load(os.path.join(os.path.dirname(os.path.dirname(__file__)), "./cascades/buoy_cascade_4.xml"))
        #hc = cv.Load("/home/seawolf/software/seawolf5/vision/buoy_cascade_4.xml")

        # use classifier to detect buoys
        minsize = (int(self.minsize), int(self.minsize))
        maxsize = (int(self.maxsize), int(self.maxsize))
        buoys = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), min_size=minsize)

        # compute average buoy size and extract to a list
        avg_w = 0
        for (x, y, w, h), n in buoys:

            # create a buoy class for this new buoys
            new_buoy = self.new_buoy(x, y, w)

            # make note of size
            avg_w = avg_w + w

            # add this buoy to our list of new buoys
            self.new.append(new_buoy)

        # update search size based on sizes found this frame
        if buoys:
            avg_w = avg_w / len(buoys)
            self.minsize = int(avg_w * .7)
            self.maxsize = int(avg_w * 1.3)

            # determine color of new buoys (if possible)
            libvision.buoy_analyzer(frame, self.new)

        # sort these new buoys into appropriate tier
        self.sort_buoys()  # must be called every frame for upkeep

        #######  DEBUG #######
        if self.debug:

            # display confirmed buoys
            for confirmed in self.confirmed:
                x = confirmed.x
                y = confirmed.y
                w = confirmed.width

                # draw rectangles on frame
                cv.Rectangle(frame, (x, y), (x + w, y + w), confirmed.debug_color, thickness=6)
                cv.Rectangle(frame, (x, y), (x + w, y + w), COLORS[confirmed.color], thickness=-1)

            # show debug frame
            svr.debug("BuoyTest", frame)

        ####### END DEBUG #######

        self.output.buoys = self.confirmed
        for buoy in self.output.buoys:
            buoy.theta = (buoy.x - frame.width / 2) * 37 / (frame.width / 2)
            buoy.phi = -1 * (buoy.y - frame.height / 2) * 36 / (frame.height / 2)
        self.return_output()

    def sort_buoys(self):

        # perform upkeep on confirmed buoys
        for confirmed in self.confirmed:

            # increment how long ago we saw this buoy.  If it gets
            # matched, this number will be reset
            confirmed.last_seen += 1
            confirmed.seen_count -= 1

            # check if this buoy can be matched to a new buoy
            self.match_buoys(confirmed)

            # if this buoy hasn't been seen recently, mark it as lost
            if confirmed.last_seen > CONFIRMED_BUOY_TIMEOUT:
                self.lost.append(confirmed)
                self.confirmed.remove(confirmed)

        # perform upkeep on candidates
        for candidate in self.candidates:

            # increment how long ago we saw this buoy.  If it gets
            # matched, this number will be reset
            candidate.last_seen += 1
            candidate.seen_count -= 1

            # check if this buoy can be matched to a new buoy
            self.match_buoys(candidate)

            # if this buoy hasn't been seen recently, stop tracking
            if candidate.last_seen > CANDIDATE_BUOY_TIMEOUT:
                self.candidates.remove(candidate)

            # if seen count has grown large enough, accept this buoy
            if candidate.seen_count >= CANDIDATE_SEEN_THRESH:
                if self.debug:
                    # assign this buoy a debug color
                    r = int(cv.RandReal(self.rng) * 255)
                    g = int(cv.RandReal(self.rng) * 255)
                    b = int(cv.RandReal(self.rng) * 255)
                    candidate.debug_color = cv.RGB(r, g, b)
                candidate.id = self.buoy_count
                self.buoy_count += 1
                self.confirmed.append(candidate)
                self.candidates.remove(candidate)

        # perform upkeep on lost buoys
        # TODO use lost buoys for anything, likely will depend on color

        # make any remaining new buoys their own candidate
        for new in self.new:
            self.candidates.append(new)
            self.new.remove(new)

    def match_buoys(self, target):
        '''matches buoys in the self.new list to a target buoy'''

        # check if any of the new buoys match this confirmed buoy
        for buoy in self.new:
            if abs(buoy.x - target.x) > MAX_X_TRANS:
                continue
            if abs(buoy.y - target.y) > MAX_Y_TRANS:
                continue
            if abs(buoy.width - target.width) > MAX_CHANGE_WIDTH:
                continue

            # this is a match, update confirmed buoy
            target.color = buoy.color
            target.x = buoy.x
            target.y = buoy.y
            target.width = buoy.width
            target.last_seen = 0
            target.seen_count += 2  # effectually increase by 1 if seen, -1 if not seen
            # TODO handle color

            # remove this new buoy that has been matched
            self.new.remove(buoy)
            break

    def new_buoy(self, x, y, w):
        '''intialize a new buoy'''
        new_buoy = Buoy()
        new_buoy.x = x
        new_buoy.y = y
        new_buoy.width = w
        new_buoy.last_seen = 0
        new_buoy.seen_count = 0

        return new_buoy

    def __repr__(self):
        return "<BuoyEntity>"
