# new_line_reducer.py
# Written as a replacement for the old one which stopped working.
# February 5, 2014


from __future__ import division
import cv2
import numpy as np
import math


def hough_line_reduce(lines, error_ratio=1 / 5, reject_ratio=1 / 3, tolerance=1 / 5):
    '''A dummy function to run LineReducer for the user.'''
    lr = LineReducer(lines, error_ratio, reject_ratio, tolerance)
    return lr.calculate_lines()


class LineReducer(object):

    '''A class that reduces a large set of line segments into a smaller set of
    fundamental line segments.
    '''

    def __init__(self, lines, error_ratio=1 / 5, reject_ratio=1 / 3, tolerance=1 / 5):
        '''Create a new instance of the LineReducer class.

        Keyword Arguments:
        lines -- tuple of lines.  If lines contains only one line, this class
            may throw a TypeError exception.
        error_ratio -- float representing maximum width to height ratio of a
            box fitting around all lines segments that describe the same real
            line.
        reject_ratio -- Defines how far at least one point on a line segment
            can be away from the line in a side-to-side sense and still be
            conidered to be tested to be part of that line, where the distance
            is the main line's length multiplied by this ratio.
        tolerance -- Defines what percentage further past the ends of the line
            a new segment can be and still be considered part of that line.
        '''
        assert error_ratio < 1, "Error ratio must be less than one."
        assert error_ratio > 0, "Error ratio must be greater than zero."

        self._error_ratio = error_ratio
        self._reject_ratio = reject_ratio
        self._tolerance = tolerance

        self._list_lines_count = len(lines[0])
        self._list_lines = list(lines[0])
        #print (self._list_lines)

        self._list_grouped = []
        self._groups = []
        self._final_lines = []

    def _line_length(self, line):
        '''Find the length of a line only given the tuple representing the
        endpoints of the line.

        Keyword Arguments:
        line -- tuple representing a line.
        '''
        square = (line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2
        return square ** (1 / 2)

    def _sort_list_lines(self, line_list):
        '''Sort all of the lines in line_list in order of longest to shortest.'''
        local_list = []
        for l in line_list:
            local_list.append([l, self._line_length(l)])

        sorted_list = sorted(local_list, key=lambda p: p[1], reverse=True)

        final_list = []
        for l in sorted_list:
            final_list.append(l[0])

        return final_list

    def _index_longest_available(self):
        '''Determine the index of the longest line segment that is not grouped.
        Returns -1 if no candidates are found.
        '''
        if self._list_lines_count == 0:
            return -1
        for x in xrange(self._list_lines_count):
            if not self._list_grouped[x]:
                return x
        return -1

    def _fit_rectangle(self, lines):
        '''Take a list of lines and find a rectangle that best matches them,
        such that all line segments are entirely within the rectangle.

        Note about format of rectangle:
        ((a, b), (c, d), e)
        a -- x-coordinate of center of rectangle.
        b -- y-coordinate of center of rectangle.
        c -- width of rectangle
        d -- height of rectangle
        e -- angle in degrees, zero when width is completely horizontal.

        Keyword Arguments:
        lines -- list of tuples representing lines.
        '''
        cloud = []
        #print (lines[0])
        for line in lines:
            cloud.append((line[0], line[1]))  # TODO MIGHT need Y before X, rather than X before Y
            cloud.append((line[2], line[3]))
        array = np.array([cloud], dtype=np.int32)
        return cv2.minAreaRect(array)

    def _test_fit(self, lines):
        '''Take a group of line segments and determine if they violate the
        error ratio.

        Keyword Arguments;
        lines -- list of tuples representing line segments.
        Returns True if the segments are acceptable.
        '''
        rectangle = self._fit_rectangle(lines)

        try:
            ratio = rectangle[1][0] / rectangle[1][1]
        except ZeroDivisionError:
            return True
        if ratio > 1:
            ratio = 1 / ratio

        if ratio > self._error_ratio:
            return False
        return True

    def _dist_points(self, point_a, point_b):
        '''Determine the distance between two points that are represented as
        tuples.
        '''
        square = (point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2
        return square ** (1 / 2)

    def _dot_prod(self, line_a, line_b):
        '''Find the dot product of two lines.

        Keyword Arguments:
        line_a -- numpy line segment representing a vector.
        line_b -- numpy line segment representing a vector.
        Returns number representing the dot product of the two vectors.
        '''

        a_delta_x = line_a[2] - line_a[0]
        b_delta_x = line_b[2] - line_b[0]
        a_delta_y = line_a[3] - line_a[1]
        b_delta_y = line_b[3] - line_b[1]
        return (a_delta_x * b_delta_x) + (a_delta_y * b_delta_y)

    def _rejection_line(self, point, line):
        '''Find the rejection vector of two lines and return the resulting line.
        The math used here is well explained at:
        http://en.wikipedia.org/wiki/Vector_projection#Vector_rejection

        Keyword Arguments:
        point -- tuple representing point
        line -- numpy array representing line
        '''
        a = [line[0], line[1], point[0], point[1]]
        scalar = self._dot_prod(a, line) / (self._line_length(line) ** 2)
        delta_x = line[2] - line[0]
        delta_y = line[3] - line[1]

        line_endpoint = np.array([line[0] + scalar * delta_x,
                                  line[1] + scalar * delta_y, point[0], point[1]])
        return line_endpoint

    def _min_dist_rejection(self, line_a, line_b):
        '''Determine if the minimum distance between two lines is less than or
        equal to a specified ratio, measured using a rejection line.

        Keyword Arguments:
        line_a -- index of first line, line that determines min acceptable dist.
        line_b -- index of second line
        Returns True if they are close enough
        '''
        l1 = self._list_lines[line_a]
        l2 = self._list_lines[line_b]

        rejection1 = self._rejection_line((l2[0], l2[1]), l1)
        rejection2 = self._rejection_line((l2[2], l2[3]), l1)

        length1 = self._line_length(rejection1)
        length2 = self._line_length(rejection2)

        comparison_length = self._line_length(self._list_lines[line_a])

        if length1 <= (comparison_length * self._reject_ratio)\
                or length2 <= (comparison_length * self._reject_ratio):
            return True
        return False

    def _min_dist_concentric(self, line_a, line_b):
        '''Determine if the minimum distance between two lines is less than or
        equal to a specified ratio, measured by making sure at least one point
        on the line is within 100(1 + tolerance)% away from both endpoints of
        the main line.

        Keyword Arguments:
        line_a -- index of first line, line that determines min acceptable dist.
        line_b -- index of second line
        Returns True if they are close enough.
        '''
        l1 = self._list_lines[line_a]
        l2 = self._list_lines[line_b]

        allowable_dist = self._line_length(l1) * (1 + self._tolerance)

        if self._dist_points((l1[0], l1[1]), (l2[0], l2[1])) > allowable_dist\
                and self._dist_points((l1[0], l1[1]), (l2[2], l2[3])) > allowable_dist:
            return False

        if self._dist_points((l1[2], l1[3]), (l2[0], l2[1])) > allowable_dist\
                and self._dist_points((l1[2], l1[3]), (l2[2], l2[3])) > allowable_dist:
            return False
        return True

    def _form_group(self):
        '''Forms a group starting with the longest available line and then adds
        it to the list self._group.

        Returns True if a group if formed.
        '''
        this_group = []

        start_line = self._index_longest_available()
        if start_line == -1:  # -1 means no groups available
            return False
        this_group.append(start_line)
        self._list_grouped[start_line] = True

        # Now we start adding lines.  Reasons that we might reject a line:
        #
        # 1. If the index is out of range.
        # 2. If it has already been added to another group.
        # 3. If it is more than half of the length of the first line away.
        # 4. If adding if makes the group of lines violate the error ratio.

        index = start_line
        while True:
            index += 1
            if index >= self._list_lines_count:
                break
            if self._list_grouped[index]\
                    or not self._min_dist_rejection(start_line, index)\
                    or not self._min_dist_concentric(start_line, index):
                continue

            test_group = []
            for l in this_group:
                test_group.append(self._list_lines[l])
            test_group.append(self._list_lines[index])

            if not self._test_fit(test_group):
                continue

            this_group.append(index)
            self._list_grouped[index] = True

        # Finish up:
        self._groups.append(this_group)
        return True

    def _group_to_line(self, group_index):
        '''Take the group at index 'group_index' and convert it into a best
        fitting line.

        Keyword Arguments:
        group_index -- index of group to process.
        Returns a tuple representing the line of best fit through the group.
        '''
        # First we define the rectangle, then we use the angle to find the ends
        # of the line, we create the line, then we return.
        lines = []
        for l in self._groups[group_index]:
            lines.append(self._list_lines[l])
        rectangle = self._fit_rectangle(lines)
        # Recall:
        # center_point = rectangle[0]
        # width = rectangle[1][0]
        # height = rectangle [1][1]
        # angle = rectangle[2]

        # First check if the rectangle accidentally mixed up width and height.
        if rectangle[1][0] > rectangle[1][1]:  # ... as it should be,
            length = rectangle[1][0]
            angle = rectangle[2]
        else:
            length = rectangle[1][1]
            angle = rectangle[2] + 90

        delta_x = length * math.cos(math.radians(angle)) / 2
        delta_y = length * math.sin(math.radians(angle)) / 2

        top_point = (rectangle[0][0] + delta_x, rectangle[0][1] + delta_y)
        bottom_point = (rectangle[0][0] - delta_x, rectangle[0][1] - delta_y)

        return np.array([top_point[0], top_point[1], bottom_point[0], bottom_point[1]])

    def _line_reduce(self):
        '''This is the actual function that executes the algorithm for the
        class.
        '''
        while True:
            if not self._form_group():
                break

        # self._DISCARD_USELESS_ONES()

        for g in xrange(len(self._groups)):
            self._final_lines.append(self._group_to_line(g))

    def calculate_lines(self):
        '''Returns a tuple containing all lines found.  Each lines is
        represented by a tuple describing the end points.  Each point is
        represented by a tuple with x and y cooredinates.

        The X and Y coordinates are FLOATS and may be POSITIVE or NEGATIVE.
        '''
        self._list_grouped = [False for x in xrange(self._list_lines_count)]
        self._list_lines = self._sort_list_lines(self._list_lines)
        self._line_reduce()
        return self._final_lines
