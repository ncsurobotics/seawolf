
from __future__ import division
import math

import cv

from entities.base import VisionEntity
import libvision

BUOY_GREEN = 0
BUOY_RED = 1
BUOY_YELLOW = 2

def get_channel(frame, channel):
    '''
    Returns a single channel image containing the specified channel from frame.

    The channel given is 0-indexed.

    '''
    result = cv.CreateImage(cv.GetSize(frame), 8, 1)
    previous_coi = cv.GetImageCOI(frame)
    cv.SetImageCOI(frame, channel+1)  # COI is 1-indexed
    cv.Copy(frame, result)
    cv.SetImageCOI(frame, previous_coi)
    return result

class BuoysEntity(VisionEntity):

    name = "BuoysEntity"
    camera_name = "forward"

    def __init__(self, color_of_interest=BUOY_RED):
        self.color_of_interest = color_of_interest

        self.saturation_adaptive_thresh_blocksize = 51
        self.saturation_adaptive_thresh = 15
        self.red_adaptive_thresh_blocksize = 51
        self.red_adaptive_thresh = 15
        self.green_adaptive_thresh_blocksize = 51
        self.green_adaptive_thresh = 20
        self.blue_adaptive_thresh_blocksize = 51
        self.blue_adaptive_thresh = 20

        #XXX
        #self.canny_low = 70
        #self.canny_high = 190
        self.canny_low = 30
        self.canny_high = 40

    def initialize_non_pickleable(self, debug=True):

        if debug:
            self.create_trackbar("saturation_adaptive_thresh", 50)
            self.create_trackbar("saturation_adaptive_thresh_blocksize", 50)
            self.create_trackbar("red_adaptive_thresh", 50)
            self.create_trackbar("red_adaptive_thresh_blocksize", 50)
            self.create_trackbar("green_adaptive_thresh", 50)
            self.create_trackbar("green_adaptive_thresh_blocksize", 50)
            self.create_trackbar("blue_adaptive_thresh", 50)
            self.create_trackbar("blue_adaptive_thresh_blocksize", 50)

            #XXX
            self.create_trackbar("canny_low")
            self.create_trackbar("canny_high")

    def find(self, frame, debug=True):

        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)

        high_red_filter = get_channel(frame, 2)
        high_green_filter = get_channel(frame, 1)
        low_blue_filter = get_channel(frame, 0)
        low_sat_filter = get_channel(hsv, 1)

        cv.AdaptiveThreshold(high_red_filter, high_red_filter,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY,
            self.red_adaptive_thresh_blocksize - self.red_adaptive_thresh_blocksize%2 + 1,
            -1*self.red_adaptive_thresh,
        )
        cv.AdaptiveThreshold(high_green_filter, high_green_filter,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY,
            self.green_adaptive_thresh_blocksize - self.green_adaptive_thresh_blocksize%2 + 1,
            -1*self.green_adaptive_thresh,
        )
        cv.AdaptiveThreshold(low_blue_filter, low_blue_filter,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY,
            self.blue_adaptive_thresh_blocksize - self.blue_adaptive_thresh_blocksize%2 + 1,
            -1*self.blue_adaptive_thresh,
        )
        cv.AdaptiveThreshold(low_sat_filter, low_sat_filter,
            255,
            cv.CV_ADAPTIVE_THRESH_MEAN_C,
            cv.CV_THRESH_BINARY_INV,
            self.saturation_adaptive_thresh_blocksize - self.saturation_adaptive_thresh_blocksize%2 + 1,
            self.saturation_adaptive_thresh,
        )

        # Red:     red - High
        #        green - Neither
        #   saturation - Low
        # Low saturation but not high green.
        #
        # Green:   red - Low
        #        green - High
        #   saturation - Neither
        # High green but not high red.
        #
        # Yellow:  red - High
        #        green - High
        #   saturation - Low
        # Low saturation and high green but not high red.
        #
        # Filters needed:
        #  - Low saturation
        #  - High green
        #  - High red

        kernel = cv.CreateStructuringElementEx(9, 9, 4, 4, cv.CV_SHAPE_ELLIPSE)

        cv.Erode(high_red_filter, high_red_filter, kernel, 1)
        cv.Dilate(high_red_filter, high_red_filter, kernel, 1)

        cv.Erode(high_green_filter, high_green_filter, kernel, 1)
        cv.Dilate(high_green_filter, high_green_filter, kernel, 1)

        cv.Erode(low_blue_filter, low_blue_filter, kernel, 1)
        cv.Dilate(low_blue_filter, low_blue_filter, kernel, 1)

        cv.Erode(low_sat_filter, low_sat_filter, kernel, 1)
        cv.Dilate(low_sat_filter, low_sat_filter, kernel, 1)

        all_buoys_filter = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.Or(low_sat_filter, high_red_filter, all_buoys_filter)
        cv.Or(all_buoys_filter, low_blue_filter, all_buoys_filter)
        cv.Or(all_buoys_filter, high_green_filter, all_buoys_filter)

        red_buoy = cv.CreateImage(cv.GetSize(frame), 8, 1)
        green_buoy = cv.CreateImage(cv.GetSize(frame), 8, 1)
        yellow_buoy = cv.CreateImage(cv.GetSize(frame), 8, 1)

        not_high_green_filter = cv.CreateImage(cv.GetSize(frame), 8, 1)
        not_high_red_filter = cv.CreateImage(cv.GetSize(frame), 8, 1)

        cv.Not(high_green_filter, not_high_green_filter)
        cv.Not(high_red_filter, not_high_red_filter)

        cv.Erode(not_high_green_filter, not_high_green_filter, kernel, 1)
        cv.Erode(not_high_red_filter, not_high_red_filter, kernel, 1)

        cv.And(low_sat_filter, not_high_green_filter, red_buoy)
        cv.And(red_buoy, high_red_filter, red_buoy)

        cv.And(high_green_filter, not_high_red_filter, green_buoy)

        cv.And(low_sat_filter, high_red_filter, yellow_buoy)
        cv.And(yellow_buoy, high_green_filter, yellow_buoy)

        cv.Erode(red_buoy, red_buoy, kernel, 1)
        cv.Dilate(red_buoy, red_buoy, kernel, 1)

        cv.Erode(green_buoy, green_buoy, kernel, 1)
        cv.Dilate(green_buoy, green_buoy, kernel, 1)

        cv.Erode(yellow_buoy, yellow_buoy, kernel, 1)
        cv.Dilate(yellow_buoy, yellow_buoy, kernel, 1)

        if debug:

            #XXX
            edge_detect = get_channel(hsv, 0)
            cv.Canny(edge_detect, edge_detect, self.canny_low, self.canny_high)
            cv.NamedWindow("canny")
            cv.ShowImage("canny", edge_detect)

            cv.NamedWindow("high_red_filter")
            cv.NamedWindow("high_green_filter")
            cv.NamedWindow("low_blue_filter")
            cv.NamedWindow("low_sat_filter")

            cv.NamedWindow("red_buoy")
            cv.NamedWindow("green_buoy")
            cv.NamedWindow("yellow_buoy")

            cv.ShowImage("high_red_filter", high_red_filter)
            cv.ShowImage("high_green_filter", high_green_filter)
            cv.ShowImage("low_blue_filter", low_blue_filter)
            cv.ShowImage("low_sat_filter", low_sat_filter)

            cv.ShowImage("red_buoy", red_buoy)
            cv.ShowImage("green_buoy", green_buoy)
            cv.ShowImage("yellow_buoy", yellow_buoy)

            cv.CvtColor(all_buoys_filter, frame, cv.CV_GRAY2BGR)
            #cv.CvtColor(red_buoy, frame, cv.CV_GRAY2BGR)

    def __repr__(self):
        return "<BuoysEntity>"
