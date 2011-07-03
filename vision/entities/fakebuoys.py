

from __future__ import division
import math
import ctypes
from collections import namedtuple

import cv

from entities.base import VisionEntity
import libvision

Point = namedtuple("Point", ["x", "y"])

BUOY_GREEN = 0
BUOY_RED = 1
BUOY_YELLOW = 2

############################### Tuning Values ###############################
TRACKING_MIN_Z_SCORE = 15
TRACKING_ALPHA = 0.0
TRACKING_TEMPLATE_SIZE = (50, 50)
TRACKING_SEARCH_AREA = (200, 200)

class FakeBuoysEntity(VisionEntity):

    name = "FakeBuoysEntity"
    camera_name = "forward"

    def __init__(self, color_of_interest=BUOY_RED):
        self.color_of_interest = color_of_interest
        self.state = "searching"
        self.trackers = []
        self.buoy_locations = []

    def initialize_non_pickleable(self, debug=True):
        cv.SetMouseCallback("FakeBuoysEntity", self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            self.trackers.append(
                libvision.Tracker(self.frame, (x,y), TRACKING_TEMPLATE_SIZE, TRACKING_SEARCH_AREA)
            )

    def find(self, frame, debug=True):
        self.frame = frame

        # debug_frame will be copied to frame at the end if debug=True
        if debug:
            debug_frame = cv.CloneImage(frame)
        else:
            debug_frame = False

        # Searching State
        # Search for buoys, then move to tracking when they are found
        if self.state == "searching":

            # Trackers will be filled in with 
            if self.trackers:
                self.state = "tracking"

        # Tracking State
        num_buoys_found = 0
        if self.state == "tracking":
            num_buoys_found, locations = self.buoy_track(frame, self.trackers, debug_frame)
            if num_buoys_found > 0:
                self.buoy_locations = locations

        # Copy debug_frame
        if debug_frame:
            cv.Copy(debug_frame, frame)

        return num_buoys_found > 0

    def buoy_track(self, frame, trackers, debug_frame):
        '''Update trackers and return (num_buoys_found, buoy_locations).'''

        num_buoys_found = 0
        locations = []

        # Update trackers
        for tracker in trackers:
            location = tracker.locate_object(frame)

            if location:
                num_buoys_found += 1

                # Draw buoy on debug frame
                if debug_frame:
                    cv.Circle(debug_frame, location, 5, (0,255,0))

                # Move origin to center and flip along horizontal axis.  Right
                # and up will then be positive, which makes more sense for
                # mission control.
                adjusted_location = Point(
                    location[0] - frame.width/2,
                    -1*location[1] + frame.height/2
                )
                locations.append(adjusted_location)

            else:
                locations.append(False)

        return num_buoys_found, locations

    def extract_buoys_from_blobs(self, blobs, labeled_image):
        blobs = filter(self.blob_filter, blobs)
        if len(blobs) == 2:
            return blobs

    def blob_filter(self, blob):
        if blob.size < 50 or blob.size > 700:
            return False

        width = blob.roi[2]
        height = blob.roi[3]
        ratio = width / height
        if ratio < 1:
            ratio = 1 / ratio
        if ratio > 2:
            return False

        return True

    def find_blobs(self, frame, debug_image):
        '''Find blobs in an image.

        Hopefully this gets blobs that correspond with
        buoys, but any intelligent checking is done outside of this function.

        '''

        # Get Channels
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3);
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        saturation = libvision.misc.get_channel(hsv, 1)
        red = libvision.misc.get_channel(frame, 2)

        # Adaptive Threshold
        cv.AdaptiveThreshold(saturation, saturation,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY_INV,
            self.saturation_adaptive_thresh_blocksize - self.saturation_adaptive_thresh_blocksize%2 + 1,
            self.saturation_adaptive_thresh,
        )
        cv.AdaptiveThreshold(red, red,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY,
            self.red_adaptive_thresh_blocksize - self.red_adaptive_thresh_blocksize%2 + 1,
            -1*self.red_adaptive_thresh,
        )

        kernel = cv.CreateStructuringElementEx(9, 9, 4, 4, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(saturation, saturation, kernel, 1)
        cv.Dilate(saturation, saturation, kernel, 1)
        cv.Erode(red, red, kernel, 1)
        cv.Dilate(red, red, kernel, 1)

        buoys_filter = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.And(saturation, red, buoys_filter)

        if debug_image:
            cv.NamedWindow("Saturation")
            cv.ShowImage("Saturation", saturation)
            cv.NamedWindow("Red")
            cv.ShowImage("Red", red)
            cv.NamedWindow("AdaptiveThreshold")
            cv.ShowImage("AdaptiveThreshold", buoys_filter)

        # Get blobs
        labeled_image = cv.CreateImage(cv.GetSize(buoys_filter), 8, 1)
        blobs = libvision.blob.find_blobs(buoys_filter, labeled_image, MIN_BLOB_SIZE, 10)

        return blobs, labeled_image

    def __repr__(self):
        return "<BuoysEntity buoy_locations=%s>" % self.buoy_locations

def scale_in_place(image, new_size):
    '''Mutates image to have size of new_size.

    This function sets the ROI and copies a resized image into it.  Be aware
    that the image's ROI is set after returning from this function.

    '''
    copy = cv.CreateImage(cv.GetSize(image), 8, 3)
    cv.Copy(image, copy)
    cv.SetImageROI(image, (0, 0, new_size[0], new_size[1]))
    cv.Resize(copy, image, cv.CV_INTER_NN)
