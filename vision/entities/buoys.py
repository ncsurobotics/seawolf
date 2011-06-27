
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
#FILTER_TYPE = cv.CV_GAUSSIAN
FILTER_TYPE = cv.CV_GAUSSIAN
FILTER_SIZE = 11
# If we want to see buoys from far away, 50 is a good value for MIN_BLOB_SIZE.
# However, if we align with the path first, the buoys will be much closer, and
# this can be raised to 200.
MIN_BLOB_SIZE = 200
TRACKING_MIN_Z_SCORE = 15
TRACKING_ALPHA = 0.6
TRACKING_TEMPLATE_MULTIPLIER = 2
TRACKING_SEARCH_AREA_MULTIPLIER = 8

class BuoysEntity(VisionEntity):

    name = "BuoysEntity"
    camera_name = "forward"

    def __init__(self, color_of_interest=BUOY_RED):
        self.color_of_interest = color_of_interest
        self.state = "searching"
        self.trackers = []
        self.buoy_locations = []

    def initialize_non_pickleable(self, debug=True):
        pass

    def find(self, frame, debug=True):

        # Scale image to reduce processing
        scale_in_place(frame, (frame.width*0.7, frame.height*0.7))

        # debug_frame will be copied to frame at the end if debug=True
        if debug:
            debug_frame = cv.CloneImage(frame)
        else:
            debug_frame = False

        # Searching State
        # Search for buoys, then move to tracking when they are found
        if self.state == "searching":

            trackers = self.initial_search(frame, debug_frame)
            if trackers:
                self.trackers = trackers
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

    def initial_search(self, frame, debug_frame):
        '''Search for buoys, return trackers when at least 2 are found.  '''

        blobs, labeled_image = find_blobs(frame, debug_frame)
        #print map(lambda x: x.roi, blobs)
        buoy_blobs = extract_buoys_from_blobs(blobs, labeled_image)

        trackers = []
        if buoy_blobs:

            # Initialize Tracking
            for blob in buoy_blobs:
                tracker = libvision.Tracker(
                    frame,
                    blob.centroid,
                    (blob.roi[2]*TRACKING_TEMPLATE_MULTIPLIER,
                            blob.roi[3]*TRACKING_TEMPLATE_MULTIPLIER),
                    (blob.roi[2]*TRACKING_SEARCH_AREA_MULTIPLIER,
                            blob.roi[3]*TRACKING_SEARCH_AREA_MULTIPLIER),
                    min_z_score=TRACKING_MIN_Z_SCORE,
                    alpha=TRACKING_ALPHA,
                    #debug=True,
                )
                trackers.append(tracker)

        # Debug info
        if debug_frame and blobs:
            for blob in blobs:
                cv.Rectangle(debug_frame, (blob.roi[0], blob.roi[1]),
                         (blob.roi[0]+blob.roi[2], blob.roi[1]+blob.roi[3]), (0,255,0))

        return trackers

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

    def __repr__(self):
        return "<BuoysEntity buoy_locations=%s>" % self.buoy_locations


def rectangles_overlap_vertically(a, b):
    if a[1] <= b[1]+b[3] and a[1]+a[3] >= b[1]:
        return True
    else:
        return False

def list_union(*args):
    union = []
    for l in args:
        for item in l:
            if item not in union:
                union.append(item)
    return union

def extract_buoys_from_blobs(blobs, labeled_image):

    pairs = []
    for i, a in enumerate(blobs):
        for b in blobs[i+1:]:
            if rectangles_overlap_vertically(a.roi, b.roi):
                pairs.append([a,b])

    if len(pairs) == 1:
        return pairs[0]

    elif len(pairs) == 2:
        union = list_union(pairs[0], pairs[1])
        if len(union) == 3:
            return union
        else:
            return False

    elif len(pairs) == 3:
        union = list_union(pairs[0], pairs[1], pairs[2])
        if len(union) == 3:
            return union
        else:
            return False

    else:
        return False

def find_blobs(frame, debug_image):
    '''Find blobs in an image.

    Hopefully this gets blobs that correspond with
    buoys, but any intelligent checking is done outside of this function.

    How it works
    ------------
    This function sums the laplacian of gaussian of some of the channels that
    should distinguish the buoys best.  The total laplacian is then scaled from
    0-255 and an otsu threshold is performed.  A blob detection is then
    performed on the resulting binary image.

    '''

    # Filter
    # TODO: This can be sped up tremendously because the laplacian and gaussian
    #       can be combined into a single pass filter.  Better yet, separate
    #       the filter into 2 1D convolutions (isn't the difference of gaussian
    #       filter separatable?)
    filtered = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.Smooth(frame, filtered, FILTER_TYPE, FILTER_SIZE, FILTER_SIZE)

    # Grab hue, saturation, red and green channels
    #TODO: Possibly not all of these channels are needed
    filtered_hsv = cv.CreateImage(cv.GetSize(filtered), 8, 3)
    cv.CvtColor(filtered, filtered_hsv, cv.CV_BGR2HSV)
    channels = [libvision.misc.get_channel(filtered_hsv, i) for i in xrange(2)]+\
        [libvision.misc.get_channel(filtered, i) for i in xrange(1,3)]

    # Sum the laplacian from each channel
    total_laplace = cv.CreateImage((filtered.width,filtered.height), cv.IPL_DEPTH_32F, 1)
    cv.SetZero(total_laplace)
    for i, channel in enumerate(channels):
        channel_laplace = cv.CreateImage((channel.width,channel.height), cv.IPL_DEPTH_32F, 1)
        cv.Laplace(channel, channel_laplace, 19)
        cv.AbsDiffS(channel_laplace, channel_laplace, 0)
        cv.Add(channel_laplace, total_laplace, total_laplace)

    # Scale total_laplace 0-255 and store in result
    result = cv.CreateImage((channel.width,channel.height), 8, 1)
    cv.SetZero(result)
    max_value = cv.MinMaxLoc(total_laplace)[1]
    cv.ConvertScaleAbs(total_laplace, result, 255/max_value)

    cv.NamedWindow("Total Laplace") #XXX
    cv.ShowImage("Total Laplace", result) #XXX

    # Get otsu threshold of total_laplace
    hist = cv.CreateHist([256], cv.CV_HIST_ARRAY, [[0,255]], 1)
    cv.CalcHist([result], hist)
    threshold = libvision.filters.otsu_get_threshold(result)
    max_value = int(cv.GetMinMaxHistValue(hist)[1])

    # Show histogram
    if debug_image:
        hist_image = libvision.hist.histogram_image(hist, color=(0,255,0))
        cv.Line(hist_image, (threshold,0), (threshold,255), (255,255,255))
        cv.NamedWindow("Hist")
        cv.ShowImage("Hist", hist_image)

    # Threshold
    cv.Threshold(result, result, threshold, max_value, cv.CV_THRESH_BINARY)
    # There will be a giant spike on the very left of the histogram if we
    # see something, because max_value will be much greater than most
    # pixels.  If there isn't a large enough spike, ignore the image.
    # The reason for this becomes more clear if you study the histogram on
    # test footage.
    if cv.QueryHistValue_1D(hist, threshold)/max_value >= 0.02:
        return [], None

    # Get blobs
    labeled_image = cv.CreateImage(cv.GetSize(result), 8, 1)
    blobs = libvision.blob.find_blobs(result, labeled_image, MIN_BLOB_SIZE, 10)

    return blobs, labeled_image

def scale_in_place(image, new_size):
    '''Mutates image to have size of new_size.

    This function sets the ROI and copies a resized image into it.  Be aware
    that the image's ROI is set after returning from this function.

    '''
    copy = cv.CreateImage(cv.GetSize(image), 8, 3)
    cv.Copy(image, copy)
    cv.SetImageROI(image, (0, 0, new_size[0], new_size[1]))
    cv.Resize(copy, image, cv.CV_INTER_NN)
