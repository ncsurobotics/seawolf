# pylint: disable=E1101
from __future__ import division
from collections import namedtuple
from itertools import combinations

import cv

import svr

from base import VisionEntity, Container
import libvision

Point = namedtuple("Point", ["x", "y"])

BUOY_GREEN = 0
BUOY_YELLOW = 2

############################### Tuning Values ###############################
INIT_SEARCH_LOST_TIMEOUT = 5  # Frames we stop looking for features after we don't see any features
INIT_TRACKING_THRESHOLD = 3  # Frames to see buoys before tracking

TRACKING_MIN_Z_SCORE = 10
TRACKING_ALPHA = 0.6
TRACKING_TEMPLATE_MULTIPLIER = 0.25
TRACKING_SEARCH_AREA_MULTIPLIER = 0.6

MAX_Y_SEPARATION = 20
CENTER_ERROR_PERCENT = 0.2


class BuoyEntity(VisionEntity):

    def init(self):
        self.output = Container()
        self.trackers = []
        self.seen_buoy_count = 0  # Used in initial_search

    def process_frame(self, frame):
        buoy_locations = []

        # Scale image to reduce processing
        '''
        scale = 0.7
        frame_scaled = cv.CreateImage((int(frame.width*scale), int(frame.height*scale)), 8, 3)
        cv.Resize(frame, frame_scaled)
        cv.SetImageROI(frame, (0, 0, int(frame.width*scale), int(frame.height*scale)))
        '''

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

        features = self.find_features(frame, debug_frame)
        middle_buoy, buoy_dist = self.extract_buoys_from_features(features)

        if middle_buoy:
            self.seen_buoy_count += 1
        else:
            self.seen_buoy_count = 0

        tracker = None
        if self.seen_buoy_count >= INIT_TRACKING_THRESHOLD:

            # Initialize Tracking
            print "Initializing Tracking"
            tracker = libvision.Tracker(
                frame,
                middle_buoy,
                (buoy_dist * TRACKING_TEMPLATE_MULTIPLIER,
                 buoy_dist * TRACKING_TEMPLATE_MULTIPLIER),
                (buoy_dist * TRACKING_SEARCH_AREA_MULTIPLIER,
                 buoy_dist * TRACKING_SEARCH_AREA_MULTIPLIER),
                min_z_score=TRACKING_MIN_Z_SCORE,
                alpha=TRACKING_ALPHA,
                # debug=True,
            )

        # Debug info
        if debug_frame and middle_buoy:
            cv.Circle(debug_frame, (int(middle_buoy[0]), int(middle_buoy[1])), int(buoy_dist * TRACKING_TEMPLATE_MULTIPLIER / 2), (0, 255, 0), 2)

        if tracker:
            return [tracker]
        else:
            return []

    def buoy_track(self, frame, trackers, debug_frame):
        '''Update trackers and return (num_buoys_found, buoy_locations).'''

        num_buoys_found = 0
        locations = []

        # Update trackers
        id_colors = ((0, 255, 0), (0, 255, 255), (255, 255, 0))
        for i, tracker in enumerate(trackers):
            location = tracker.locate_object(frame)

            if location:
                num_buoys_found += 1

                # Draw buoy on debug frame
                if debug_frame:
                    cv.Circle(debug_frame, location, 10, id_colors[i], 2)

                locations.append(adjust_location(location, frame.width, frame.height))

        return num_buoys_found, locations

    def extract_buoys_from_features(self, features):

        if len(features) < 3:
            return None, None

        for tripplet in combinations(features, 3):

            # Sort features by x value
            feature1, feature2, feature3 = sorted(tripplet, key=lambda x: x[0])

            # Test that center feature is in middle of outside features
            center = (feature1[0] + feature3[0]) / 2
            if abs(center - feature2[0]) > CENTER_ERROR_PERCENT * (feature3[0] - feature1[0]):
                continue

            # Go through every pair
            tripplet_is_valid = True
            for a, b in combinations((feature1, feature2, feature3), 2):

                # Ignore tripplets with pairs with large y separations
                if abs(a[1] - b[1]) > MAX_Y_SEPARATION:
                    tripplet_is_valid = False
                    break
            if not tripplet_is_valid:
                continue

            return feature2, feature3[0] - feature1[0]

        return None, None

    def find_features(self, frame, debug_image):
        '''Find features in an image.'''

        # Get Channels
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        grey = libvision.misc.get_channel(hsv, 2)

        # Feature Detection
        eigimage = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 1)
        tmpimage = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 1)
        cornercount = 4
        qualitylevel = .2
        mindistance = 40
        blockSize = 7
        corners = cv.GoodFeaturesToTrack(grey, eigimage, tmpimage, cornercount, qualitylevel, mindistance, None, blockSize, 0, 0.4)

        # determine if three corners are in a reasonable orientation
        if debug_image:

            for corner in corners:
                corner_color = (0, 0, 255)
                cv.Circle(debug_image, (int(corner[0]), int(corner[1])), 15, corner_color, 2, 8, 0)

        return corners


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
        (location[0] - width / 2) / (width / 2),
        (-1 * location[1] + height / 2) / (height / 2),
    )
