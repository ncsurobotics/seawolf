from __future__ import division
from time import time

import cv

import libvision

DEFAULT_MATCH_METHOD = cv.CV_TM_CCORR
MIN = 2  # Indexes into cv.minmaxloc outputs.
MAX = 3
# Depending on the matching method, a match will be at either min or max.  This
# dict maps methods to min or max accordingly.
MATCH_METHOD_MIN_OR_MAX = {
    cv.CV_TM_SQDIFF: MIN,
    cv.CV_TM_SQDIFF_NORMED: MIN,
    cv.CV_TM_CCORR: MAX,
    cv.CV_TM_CCORR_NORMED: MAX,
    cv.CV_TM_CCOEFF: MAX,
    cv.CV_TM_CCOEFF_NORMED: MAX,
}


class Tracker(object):

    '''Tracks an object between a sequence of frames.

    On initialization, a frame is given with the location and size of the
    object to track.  Tracker.locate_object() is then called for each frame to
    track the object.

    A template is created based on the frame given during initialization.  For
    each frame after that, a template matching is done around the previous
    object location to find the object in the new frame.  The size of this
    search area is determined by the search_size argument to __init__().

    '''

    def __init__(self, frame, center, size, search_size, alpha=0.2,
                 min_z_score=5.0, match_method=DEFAULT_MATCH_METHOD, debug=False):
        '''
        Arguments:

            frame - Frame which the template is extracted from.

            center - The center of the object to track in the given frame.
            Must be a tuple (x,y).

            size - The width and height of the object found.  Used to determine
                the size of the template that is created for the object.  Must
                be a tuple (width, height).

            search_size - The width and height of the area that will be
                searched each frame, with the previous object location at the
                center.  Must be a tuple (width, height).

            alpha - Each frame the object template is updated.  alpha is a
                floating point value from 0-1 specifying how much of the new
                image is mixed in with the current template each frame.  Giving
                a value of 1 will replace the template entirely with the match
                that was just found.  A value of 0 will keep the initial
                template.

            min_z_score - The number of standard deviations from the average
                the template matching max/min must be for it to be considered a
                valid match.

            match_method - The distance calculation that is used for template
                matching.  Must be one of the OpenCV method constants defined
                for OpenCV's MatchTemplate function (cv.CV_TM_*).

            debug - If this evaluates to True, various debugging windows will
                be displayed.

        '''

        self.object_center = center
        self.size = size
        self.match_method = match_method
        self.alpha = alpha
        self.min_z_score = min_z_score
        self.search_size = search_size
        self.debug = debug

        template_rect = clip_rectangle((
            center[0] - size[0] / 2,
            center[1] - size[1] / 2,
            size[0],
            size[1],
        ), frame.width, frame.height)
        self._template = self._preprocess(crop(frame, template_rect))

        if self.debug:
            cv.NamedWindow("match")
            cv.NamedWindow("template")
            cv.NamedWindow("search region")
            cv.NamedWindow("Histogram")

    def _preprocess(self, frame):
        '''
        Formats a raw rgb image into a processed image which template matching
        is performed on.

        In this case, the laplacian of the image and template is calculated,
        and the matching is done on those preprocessed frames.  In the future,
        this function should implement multiple preprocessing methods that can
        be selected between on init.

        '''

        dst = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, frame.channels)
        cv.Laplace(frame, dst, 19)
        return dst

    def _update_template(self, search_image, coordinates):
        '''Updates the object template after a match for the object is found.

        search_image is the region which locate_object looked for the object
        in.  coordinates is a tuple (x,y) of the position within search_image
        that the object was found.  The search_image should already be
        preprocessed.  The current template and search image are mixed together
        as such:
            self.template = self.template*(1-self.alpha) + match*self.alpha

        '''
        match_rectangle = (
            int(coordinates[0] - self._template.width / 2),
            int(coordinates[1] - self._template.height / 2),
            int(self._template.width),
            int(self._template.height)
        )
        cv.SetImageROI(search_image, match_rectangle)

        cv.ConvertScale(self._template, self._template, 1 - self.alpha)
        cv.ScaleAdd(search_image, self.alpha, self._template, self._template)

        cv.ResetImageROI(search_image)

    def locate_object(self, frame):
        '''
        Finds the object in the given frame based on information from previous
        frames.

        The object location as a tuple (x,y) within the given image is
        returned.  If the object is not found, False is returned.
        Tracker.object_center will always contain the last known object
        location.
        '''

        if not self._template:
            raise RuntimeError("The Tracker class can not be used after it is "
                               "unpickled.")

        search_rect = clip_rectangle((
            self.object_center[0] - self.search_size[0] / 2,  # x
            self.object_center[1] - self.search_size[1] / 2,  # y
            self.search_size[0],  # width
            self.search_size[1],  # height
        ), frame.width, frame.height)
        search_image = self._preprocess(crop(frame, search_rect))
        result = cv.CreateImage(
            (
                search_image.width - self._template.width + 1,
                search_image.height - self._template.height + 1
            ),
            cv.IPL_DEPTH_32F, 1)
        cv.MatchTemplate(search_image, self._template, result, self.match_method)
        min_or_max = MATCH_METHOD_MIN_OR_MAX[self.match_method]
        minmaxloc = cv.MinMaxLoc(result)
        if abs(minmaxloc[1] - minmaxloc[0]) < 0.001:
            return False
        match_in_result = minmaxloc[min_or_max]

        # Change from result image coordinates to search region coordinates to
        # image coordinates
        match_in_search_region = (
            match_in_result[0] + self._template.width / 2,
            match_in_result[1] + self._template.height / 2,
        )
        object_center = (
            match_in_search_region[0] + search_rect[0],
            match_in_search_region[1] + search_rect[1],
        )
        object_center = (
            int(in_range(0, object_center[0], frame.width - 1)),
            int(in_range(0, object_center[1], frame.height - 1)),
        )

        # Determine if the max/min is significant.
        hist = cv.CreateHist([256], cv.CV_HIST_ARRAY, [[0, 255]], 1)
        cv.CalcHist([scale_32f_image(result)], hist)
        # XXX stddevs from mean should be calculated from either 0 or 255
        #    depending on min or max
        distance = abs(libvision.hist.num_stddev_from_mean(hist, 255))
        if distance < self.min_z_score:
            object_found = False
        else:
            object_found = True
            self._update_template(search_image, match_in_search_region)
            self.object_center = object_center

        if self.debug:

            result_8bit = scale_32f_image(result)
            if object_found:
                cv.Circle(result_8bit, match_in_result, 5, (0, 255, 0))
                cv.Circle(search_image, match_in_search_region, 5, (0, 255, 0))
            hist_image = libvision.hist.histogram_image(hist)

            cv.ShowImage("match", result_8bit)
            cv.ShowImage("template", scale_32f_image(self._template))
            cv.ShowImage("search region", scale_32f_image(search_image))
            cv.ShowImage("Histogram", hist_image)

        # Update Template
        if object_found:
            return self.object_center
        else:
            return False

    def __getstate__(self):
        '''Makes this object safe for pickling.

        OpenCV object cannot be pickled.  Something very weird happens if you
        try.  This function is called while pickling.  The dictionary returned
        by this function is what is actually pickled, which excludes the
        IplImage which won't pickle correctly.

        Note that for this reason, this class does not work correctly after pickled.

        '''
        pickleable_copy = self.__dict__.copy()
        pickleable_copy['_template'] = None
        return pickleable_copy


def scale_32f_image(image):
    '''
    Scales the given cv.IPL_DEPTH_32F type image to an 8 bit image so that the
    smallest value maps to 0 and the largest maps to 255.  Used for displaying
    debugging images.

    Processes each channel separately, which can produce some useful, but
    esoteric results.

    '''
    if image.depth != cv.IPL_DEPTH_32F:
        return image
    result = cv.CreateImage(cv.GetSize(image), 8, image.channels)
    channel_image = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_32F, 1)
    channel_scaled = cv.CreateImage(cv.GetSize(image), 8, 1)
    for channel_num in xrange(1, image.channels + 1):

        cv.SetImageCOI(image, channel_num)
        cv.Copy(image, channel_image)
        minmaxloc = cv.MinMaxLoc(channel_image)
        minimum = minmaxloc[0]
        maximum = minmaxloc[1]
        if maximum - minimum > 0:
            cv.ConvertScale(channel_image, channel_scaled, 255 / (maximum - minimum), -255 / (maximum - minimum) * minimum)
        else:
            cv.ConvertScale(channel_image, channel_scaled, 0, -255 / minimum)

        cv.SetImageCOI(result, channel_num)
        cv.Copy(channel_scaled, result)

    cv.SetImageCOI(image, 0)
    cv.SetImageCOI(result, 0)
    return result


def crop(frame, rect):
    '''Crops the image to a given CvRect.

    Rect must be within the image.  Rectangles can be clipped with
    clip_rectangle().

    '''
    cv.SetImageROI(frame, rect)
    cropped = cv.CreateImage(cv.GetSize(frame), frame.depth, frame.channels)
    cv.Copy(frame, cropped)
    cv.ResetImageROI(frame)
    return cropped


def clip_rectangle(rect, width, height):
    '''
    Returns the clipped CvRect that will fit inside a width x height image.

    '''
    x = in_range(0, rect[0], width - 1)
    y = in_range(0, rect[1], height - 1)
    return (
        int(x),
        int(y),
        int(rect[2] - abs(x - rect[0])),
        int(rect[3] - abs(y - rect[1])),
    )


def in_range(min, x, max):
    '''Returns x clipped to the range of min and max.'''
    if x > max:
        return max
    elif x < min:
        return min
    else:
        return x
