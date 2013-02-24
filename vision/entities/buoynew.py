
from __future__ import division
from collections import namedtuple
from itertools import combinations
from time import time
from math import sqrt

import cv

import svr

from base import VisionEntity, Container
import libvision

Point = namedtuple("Point", ["x", "y"])

############################### Tuning Values ###############################
INIT_TRACKING_THRESHOLD = 6  # Frames to see buoys before tracking
TRACKING_MIN_Z_SCORE = 10
TRACKING_ALPHA = 0.2
MOVEMENT_THRESHOLD = 50  # Pixel distance the buoys are considered the same when finding buoys to track
CANDIDATE_TIMEOUT = 2 # Time before the current buoy candidate is forgotten

class BuoyNewEntity(VisionEntity):

    def init(self):
        self.output = Container()
        self.trackers = []
        self.seen_buoy_count = 0  # Used in initial_search
        self.last_buoy = None
        self.last_buoy_time = None

    def process_frame(self, frame):
        buoy_locations = []

        # Create debug_frame
        if self.debug:
            debug_frame = cv.CloneImage(frame)
        else:
            debug_frame = False

        # Look for buoys if there aren't any trackers yet
        if not self.trackers:
            self.trackers = self.initial_search(frame, debug_frame)
            if self.trackers:

                buoy_locations = map(lambda x: adjust_location(x.object_center, frame.width, frame.height), self.trackers)
                if debug_frame:
                    svr.debug("Buoy", debug_frame)
                return

        # Tracking
        else:
            num_buoys_found, buoy_locations = self.buoy_track(frame, self.trackers, debug_frame)

            # Debug info
            if debug_frame:
                for tracker in self.trackers:
                    print "Drawing Circle!!!!", tracker.object_center
                    cv.Circle(debug_frame, (int(tracker.object_center[0]),int(tracker.object_center[1])), tracker.size[0], (0,0,255), 2)

        if debug_frame:
            svr.debug("Buoy", debug_frame)

        # Convert to output format
        self.output.buoys = []
        for location in buoy_locations:
            buoy = Container()
            buoy.theta = location[0]
            buoy.phi = location[1]
            buoy.id = 1
            self.output.buoys.append(buoy)

        if self.output.buoys:
            self.return_output()
        return self.output

    def initial_search(self, frame, debug_frame):
        '''Search for buoys, return trackers when at least 2 are found.'''

        middle_buoy, buoy_scale = self.detect_buoys(frame, debug_frame)

        if middle_buoy and (not self.last_buoy or sqrt((middle_buoy[0]-self.last_buoy[0])**2 + (middle_buoy[1]-self.last_buoy[1])**2) < MOVEMENT_THRESHOLD):
            self.seen_buoy_count += 1
            self.last_buoy = middle_buoy
            self.last_buoy_time = time()
            print "Seen Buoy", self.seen_buoy_count, ":", middle_buoy
        elif time() > self.last_buoy_time + CANDIDATE_TIMEOUT:
            self.seen_buoy_count = 0

        tracker = None
        if self.seen_buoy_count >= INIT_TRACKING_THRESHOLD:

            # Initialize Tracking
            print "Initializing Tracking"
            template_size = (100, 100)
            tracking_size = (300, 300)
            tracker = libvision.Tracker(
                frame,
                middle_buoy,
                template_size,
                tracking_size,
                min_z_score=TRACKING_MIN_Z_SCORE,
                alpha=TRACKING_ALPHA,
                #debug=True,
            )

        if tracker:
            return [tracker]
        else:
            return []

    def buoy_track(self, frame, trackers, debug_frame):
        '''Update trackers and return (num_buoys_found, buoy_locations).'''

        num_buoys_found = 0
        locations = []

        # Update trackers
        id_colors = ((0,255,0), (0,255,255), (255,255,0))
        for i, tracker in enumerate(trackers):
            location = tracker.locate_object(frame)

            if location:
                num_buoys_found += 1

                # Draw buoy on debug frame
                if debug_frame:
                    cv.Circle(debug_frame, location, 10, id_colors[i], 2)

                locations.append(adjust_location(location, frame.width, frame.height))

        return num_buoys_found, locations

    def detect_buoys(self, frame, debug_frame):

        # Get Channels
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        grey = libvision.misc.get_channel(hsv, 2)

        # load a haar classifier
        hc = cv.Load("/home/seawolf/software/seawolf5/vision/buoy_cascade_4.xml")

        #use classifier to detect buoys
        minsize = (10, 10)
        maxsize = (200, 200)
        buoys = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), min_neighbors=0, min_size=minsize, max_size=maxsize)

        if not buoys:
            return None, None

        # We'll probably only see one buoy at a time, so take the first one
        (x,y,w,h),n = buoys[0]
        return (x,y), w

def scale_in_place(image, new_size):
    '''Mutates image to have size of new_size.

    This function sets the ROI and copies a resized image into it.  Be aware
    that the image's ROI is set after returning from this function.

    '''
    copy = cv.CreateImage(cv.GetSize(image), 8, 3)
    cv.Copy(image, copy)
    cv.SetImageROI(image, (0, 0, new_size[0], new_size[1]))
    cv.Resize(copy, image, cv.CV_INTER_NN)

def adjust_location(location, width, height):
    '''
    Move origin to center and flip along horizontal axis.  Right
    and up will then be positive, which makes more sense for
    mission control.  Then scale from -1 to 1.
    '''
    return Point(
        (location[0] - width/2) / (width/2),
        (-1*location[1] + height/2) / (height/2),
    )

