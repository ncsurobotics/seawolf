from __future__ import division
import math

import cv

import svr

from base import VisionEntity
import libvision


class Bin(object):
    def __init__(self, corner1, corner2, corner3, corner4):

        """
        Expected Bin setup:



         Corner1             Corner3
         _________________________
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |_________________________|
         Corner2            Corner4


        """

        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4

        if line_distance(self.corner1, self.corner2) < line_distance(self.corner1, self.corner3):
            tmp_corner = self.corner2
            self.corner2 = self.corner3
            self.corner3 = tmp_corner

        if line_distance(self.corner1, self.corner2) < line_distance(self.corner1, self.corner3):
            self.angle = -angle_between_lines(line_slope(self.corner1, self.corner2), 0)
        else:
            self.angle = -angle_between_lines(line_slope(self.corner1, self.corner3), 0)

        #ID number used when tracking bins
        self.id = 0

        #decisive type of letter in the bin
        self.icon = 0

        #center of bin
        self.center = rect_midpoint(self.corner1, self.corner2, self.corner3, self.corner4)

        self.lastseen = 2

        self.corner1_updated = 0
        self.corner2_updated = 0
        self.corner3_updated = 0
        self.corner4_updated = 0

        #locx and locy are relative locations of corners when compared to other corners of the same rectangle
        self.corner1_locx = self.corner1[0] - self.corner2[0]
        self.corner1_locy = self.corner1[1] - self.corner2[1]
        self.corner2_locx = self.corner2[0] - self.corner1[0]
        self.corner2_locy = self.corner2[1] - self.corner1[1]
        self.corner3_locx = self.corner3[0] - self.corner1[0]
        self.corner3_locy = self.corner3[1] - self.corner1[1]
        self.corner4_locx = self.corner4[0] - self.corner1[0]
        self.corner4_locy = self.corner4[1] - self.corner1[1]

        self.distance12 = line_distance(self.corner1, self.corner2)
        self.distance13 = line_distance(self.corner1, self.corner3)
        self.distance24 = line_distance(self.corner4, self.corner2)
        self.distance34 = line_distance(self.corner3, self.corner4)

        self.angle124 = angle_between_lines(line_slope(self.corner1, self.corner2),
                                            line_slope(self.corner2, self.corner4))
        self.angle134 = angle_between_lines(line_slope(self.corner1, self.corner3),
                                            line_slope(self.corner3, self.corner4))
        self.angle312 = angle_between_lines(line_slope(self.corner3, self.corner1),
                                            line_slope(self.corner1, self.corner2))
        self.angle243 = angle_between_lines(line_slope(self.corner2, self.corner4),
                                            line_slope(self.corner4, self.corner3))

        self.corner1_replace = []
        self.corner2_replace = []
        self.corner3_replace = []
        self.corner4_replace = []


def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0] - corner_a[0]) ** 2 +
                         (corner_b[1] - corner_a[1]) ** 2)
    return distance


def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1] - corner_a[1]) / (corner_b[0] - corner_a[0])
        return slope


def angle_between_lines(slope_a, slope_b):
    if slope_a is not None and slope_b is not None and (1 + slope_a * slope_b) != 0:
        angle = math.atan((slope_a - slope_b) / (1 + slope_a * slope_b))
        return angle
    else:
        angle = 0
        return angle


def midpoint(corner_a, corner_b):
    midpoint_x = (corner_b[0] - corner_a[0]) / 2 + corner_a[0]
    midpoint_y = (corner_b[1] - corner_a[1]) / 2 + corner_a[1]
    return [midpoint_x, midpoint_y]


def midpointx(corner_a, corner_b):
    midpoint_x = (corner_b[0] - corner_a[0]) / 2 + corner_a[0]
    return midpoint_x


def midpointy(corner_a, corner_b):
    midpoint_y = (corner_b[1] - corner_a[1]) / 2 + corner_a[1]
    return midpoint_y


def rect_midpoint(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0]) / 4
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1]) / 4
    return (midpoint_x, midpoint_y)


def rect_midpointx(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0]) / 4
    return midpoint_x


def rect_midpointy(corner_a, corner_b, corner_c, corner_d):
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1]) / 4
    return midpoint_y


def average_corners(corner_a, corner_b):
    average_corner = [0, 0]
    average_corner[0] = (corner_a[0] + corner_b[0]) / 2
    average_corner[1] = (corner_a[1] + corner_b[1]) / 2
    return average_corner


def check_for_corner(line1, line2):
    angle_clarity_max = math.pi / 2 + .1
    angle_clarity_min = math.pi / 2 - .1
    corner_distance = 10
    corner_angle = angle_between_lines(line_slope(line1[0], line1[1]),
                                       line_slope(line2[0], line2[1]))

    if angle_clarity_min < corner_angle < angle_clarity_max:
        if (math.fabs(line1[0][0] - line2[0][0]) < corner_distance or
            math.fabs(line1[0][1] - line2[0][1]) < corner_distance or
            math.fabs(line1[1][0] - line2[1][0]) < corner_distance or
            math.fabs(line1[1][1] - line2[1][1]) < corner_distance):
            return True


class BinsHough2Entity(VisionEntity):
    def init(self):

    #        self.vertical_threshold = 15*math.pi/180  # How close to vertical lines must be
    #        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 15  # 15 at comp
        self.adaptive_thresh_blocksize = 35  # 27 before competition
        self.adaptive_thresh = 7  # 23 before competition #9 at competition #11 after hough line changes

        self.max_range = 100

        self.Boxes = []
        self.groups = []

        self.corners = []
        self.hough_corners = []

        self.Bins = []

        #For Probalistic
        self.min_length = 15 #15 at comp
        self.max_gap = 10 #40 #5 at comp

        #grouping
        self.max_corner_range = 30  #15

        #for corner findings
        self.max_corner_range2 = 15

        #for updating
        self.max_corner_range3 = 30

        #for hough corners grouping
        self.max_corner_range4 = 35

        self.max_corner_range5 = 30

        #For Rectangle Indentification Variables, look at function

        self.min_corner_distance = 40  #40

        #min and max angle in order to only accept rectangles
        self.angle_min = math.pi / 2 - .07
        self.angle_max = math.pi / 2 + .07

        #How close to the ideal 1:1 ratio the bin sides must be
        self.ratio_threshold = 1.5 #1.5 before competition

        self.center_thresh = 40

        self.lastseen_thresh = 60

        self.length_trans_thresh = 40 #40 before  competition
        self.angle_trans_thresh = 5 #5 before competition

        self.center_trans = 15

        self.corner_sort_thresh = 15

        self.parallel_sides_length_thresh = 10

        #How close the perimeter of a bin must be when compared to the perimeter of other bins
        self.perimeter_threshold = 1

        self.corner_update_value = 5

        self.bin_id = 0


    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        og_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Copy(frame, self.debug_frame)
        cv.Copy(self.debug_frame, og_frame)

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1)  #3 before competition #2 at competition
        cv.Copy(hsv, binary)
        cv.SetImageCOI(hsv, 0)

        cv.AdaptiveThreshold(binary, binary,
                             255,
                             cv.CV_ADAPTIVE_THRESH_MEAN_C,
                             cv.CV_THRESH_BINARY_INV,
                             self.adaptive_thresh_blocksize,
                             self.adaptive_thresh,
        )

        # Morphology
        kernel = cv.CreateStructuringElementEx(5, 5, 3, 3, cv.CV_SHAPE_ELLIPSE)
        cv.Erode(binary, binary, kernel, 1)
        cv.Dilate(binary, binary, kernel, 1)

        # Get Edges
        #cv.Canny(binary, binary, 30, 40)

        cv.CvtColor(binary, self.debug_frame, cv.CV_GRAY2RGB)

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_PROBABILISTIC,
                                   rho=1,
                                   theta=math.pi / 180,
                                   threshold=self.hough_threshold,
                                   param1=self.min_length,
                                   param2=self.max_gap
        )

        lines = []

        for line in raw_lines:
            lines.append(line)

        #Grouping lines depending on endpoint similarities

        for line1 in lines[:]:
            for line2 in lines[:]:
                if line1 in lines and line2 in lines and line1 != line2:
                    if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range and \
                       math.fabs(line1[0][1] - line2[0][1]) < self.max_corner_range and \
                       math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range and \
                       math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1]) > line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)
                    elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range and \
                         math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range and \
                         math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range and \
                         math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1]) > line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)

        self.hough_corners = []
        for line in lines:
            self.hough_corners.append(line[0])
            self.hough_corners.append(line[1])

        for corner1 in self.hough_corners[:]:
            for corner2 in self.hough_corners[:]:
                if corner1 is not corner2 and corner1 in self.hough_corners and corner2 in self.hough_corners:
                    if math.fabs(corner1[0] - corner2[0]) < self.max_corner_range4 and \
                       math.fabs(corner1[1] - corner2[1]) < self.max_corner_range4:
                        corner1 = [(corner1[0] + corner2[0]) / 2, (corner1[1] + corner2[1]) / 2]
                        self.hough_corners.remove(corner2)

        for line1 in lines:
            #cv.Line(self.debug_frame,line1[0],line1[1], (0,0,255), 10, cv.CV_AA, 0)
            for line2 in lines:
                if line1 is not line2:
                    self.find_corners(line1, line2)

        for corner1 in self.corners:
            for corner2 in self.corners:
                if math.fabs(corner1[1][0] - corner2[1][0]) < self.max_corner_range2 and \
                   math.fabs(corner1[1][1] - corner2[1][1]) < self.max_corner_range2 and \
                   math.fabs(corner1[2][0] - corner2[2][0]) < self.max_corner_range2 and \
                   math.fabs(corner1[2][1] - corner2[2][1]) < self.max_corner_range2 and \
                   math.fabs(corner1[0][0] - corner2[0][0]) > self.max_corner_range2 and \
                   math.fabs(corner1[0][1] - corner2[0][1]) > self.max_corner_range2:
                    pt1 = (int(corner1[0][0]), int(corner1[0][1]))
                    pt4 = (int(corner2[0][0]), int(corner2[0][1]))
                    pt3 = (int(corner1[1][0]), int(corner1[1][1]))
                    pt2 = (int(corner1[2][0]), int(corner1[2][1]))
                    #line_color = (0,255,0)s
                    #cv.Line(self.debug_frame,pt1,pt2, line_color, 10, cv.CV_AA, 0)                  
                    #cv.Line(self.debug_frame,pt1,pt3, line_color, 10, cv.CV_AA, 0)
                    #cv.Line(self.debug_frame,pt4,pt2, line_color, 10, cv.CV_AA, 0)                  
                    #cv.Line(self.debug_frame,pt4,pt3, line_color, 10, cv.CV_AA, 0)
                    new_bin = Bin(pt1, pt2, pt3, pt4)
                    new_bin.id = self.bin_id
                    self.bin_id += 1
                    if math.fabs(line_distance(pt1, pt2) - line_distance(pt3, pt4)) < self.parallel_sides_length_thresh and \
                       math.fabs(line_distance(pt1, pt3) - line_distance(pt2, pt4)) < self.parallel_sides_length_thresh:
                        self.Bins.append(new_bin)
                        print "new_bin"

                elif (math.fabs(corner1[1][0] - corner2[2][0]) < self.max_corner_range2 and
                      math.fabs(corner1[1][1] - corner2[2][1]) < self.max_corner_range2 and
                      math.fabs(corner1[2][0] - corner2[1][0]) < self.max_corner_range2 and
                      math.fabs(corner1[2][1] - corner2[1][1]) < self.max_corner_range2 and
                      math.fabs(corner1[0][0] - corner2[0][0]) > self.max_corner_range2 and
                      math.fabs(corner1[0][1] - corner2[0][1]) > self.max_corner_range2):
                    continue

        self.corners = []
        self.final_corners = self.sort_corners() #Results are not used. Experimental corners which have been seen twice, should be only the corners we want, but there were problems
        self.sort_bins()
        self.update_bins()
        self.group_bins()
        self.draw_bins()

        for corner in self.hough_corners:
            line_color = [255, 0, 0]
            cv.Circle(self.debug_frame, corner, 15, (255, 0, 0), 2, 8, 0)

        for line in lines:
            line_color = [255, 0, 0]
            cv.Line(self.debug_frame, line[0], line[1], line_color, 5, cv.CV_AA, 0)
            #cv.Circle(self.debug_frame, line[0], 15, (255,0,0), 2,8,0)
            #cv.Circle(self.debug_frame, line[1], 15, (255,0,0), 2,8,0)

        #Output bins
        self.output.bins = self.Bins
        anglesum = 0
        for bins in self.output.bins:
            bins.theta = (bins.center[0] - frame.width / 2) * 37 / (frame.width / 2)
            bins.phi = -1 * (bins.center[1] - frame.height / 2) * 36 / (frame.height / 2)
            anglesum += bins.angle
            # bins.orientation = bins.angle
        if len(self.output.bins) > 0:
            self.output.orientation = anglesum / len(self.output.bins)
        else:
            self.output.orientation = None
        self.return_output()

        svr.debug("Bins", self.debug_frame)
        svr.debug("Original", og_frame)

        #BEGIN SHAPE PROCESSING

        #constants
        img_width = 128
        img_height = 256

        number_x = 23
        number_y = 111
        number_w = 82
        number_h = 90

        bin_thresh_blocksize = 11
        bin_thresh = 1.9

        red_significance_threshold = 0.4

        #load templates - run once, accessible to number processor

        number_templates = [
            (10, cv.LoadImage("number_templates/10.png")),
            (16, cv.LoadImage("number_templates/16.png")),
            (37, cv.LoadImage("number_templates/37.png")),
            (98, cv.LoadImage("number_templates/98.png")),
        ]

        #Begin Bin Contents Processing

        for bin in self.Bins:
            #Take the bin's corners, and get an image containing an img_width x img_height rectangle of it
            transf = cv.CreateMat(3, 3, cv.CV_32FC1)
            cv.GetPerspectiveTransform(
                [bin.corner1, bin.corner2, bin.corner3, bin.corner4],
                [(0, 0), (0, img_height), (img_width, 0), (img_width, img_height)],
                transf
            )
            bin_image = cv.CreateImage([img_width, img_height], 8, 3)
            cv.WarpPerspective(frame, bin_image, transf)

            #AdaptaveThreshold to get black and white image highlighting the number (still works better than my yellow-vs-red threshold attempt
            hsv = cv.CreateImage(cv.GetSize(bin_image), 8, 3)
            bin_thresh_image = cv.CreateImage(cv.GetSize(bin_image), 8, 1)
            cv.CvtColor(bin_image, hsv, cv.CV_BGR2HSV)
            cv.SetImageCOI(hsv, 3)
            cv.Copy(hsv, bin_thresh_image)
            cv.SetImageCOI(hsv, 0)
            cv.AdaptiveThreshold(bin_thresh_image, bin_thresh_image,
                                 255,
                                 cv.CV_ADAPTIVE_THRESH_MEAN_C,
                                 cv.CV_THRESH_BINARY_INV,
                                 bin_thresh_blocksize,
                                 bin_thresh,
            )
            kernel = cv.CreateStructuringElementEx(5, 5, 3, 3, cv.CV_SHAPE_ELLIPSE)
            cv.Erode(bin_thresh_image, bin_thresh_image, kernel, 1)
            cv.Dilate(bin_thresh_image, bin_thresh_image, kernel, 1)

            #Here, we loop through all four different templates, and figure out which one we think is most likely.
            #The comparison function counts corresponding pixels that are non-zero in each image, and then corresponding pixels that are different in each image. The ratio of diff_count/both_count is our "unconfidence" ratio. The lower it is, the more confident we are.
            #There are two nearly identical pieces of code within this loop. One checks the bin right-side-up, and the other one checks it flipped 180.
            last_thought_number = -1
            last_unconfidence_ratio = number_w * number_h + 2
            for i in range(0, len(number_templates)):
                both_count = 0
                diff_count = 0
                this_number_image = number_templates[i][1]
                for y in range(0, number_h):
                    for x in range(0, number_w):
                        if (bin_thresh_image[y + number_y, x + number_x] != 0) and (this_number_image[y, x][0] != 0):
                            both_count += 1
                        elif (bin_thresh_image[y + number_y, x + number_x] != 0) or (this_number_image[y, x][0] != 0):
                            diff_count += 1
                if both_count == 0:
                    unconfidence_ratio = number_w * number_h + 1  # max unconfidence
                else:
                    unconfidence_ratio = 1.0 * diff_count / both_count
                if unconfidence_ratio < last_unconfidence_ratio:
                    last_thought_number = number_templates[i][0]
                    last_unconfidence_ratio = unconfidence_ratio
                both_count = 0
                diff_count = 0
                for y in range(0, number_h):
                    for x in range(0, number_w):
                        if (bin_thresh_image[img_height - number_y - 1 - y, img_width - number_x - 1 - x] != 0) and (
                                this_number_image[y, x][0] != 0):
                            both_count += 1
                        elif (bin_thresh_image[img_height - number_y - 1 - y, img_width - number_x - 1 - x] != 0) or (
                                this_number_image[y, x][0] != 0):
                            diff_count += 1
                if both_count == 0:
                    unconfidence_ratio = number_w * number_h + 1  # max unconfidence
                else:
                    unconfidence_ratio = 1.0 * diff_count / both_count
                if unconfidence_ratio < last_unconfidence_ratio:
                    last_thought_number = number_templates[i][0]
                    last_unconfidence_ratio = unconfidence_ratio

            print str(last_thought_number) + " | " + str(last_unconfidence_ratio)

            try: #check if it's defined
                bin.number_unconfidence_ratio
            except:
                bin.number_unconfidence_ratio = last_unconfidence_ratio
                bin.number = last_thought_number
                print "Set Speed Limit Number"
            else:
                if last_unconfidence_ratio < bin.number_unconfidence_ratio:
                    bin.number_unconfidence_ratio = last_unconfidence_ratio
                    if bin.number == last_thought_number:
                        print "More Confident on Same Number: Updated"
                    else:
                        print "More Confident on Different Number: Updated"
                        bin.icon = last_thought_number


    #END SHAPE PROCESSING

    def find_corners(self, line1, line2):
        corner1 = 0
        corner2 = 0
        corner3 = 0
        corner4 = 0
        corner_angle = angle_between_lines(line_slope(line1[0], line1[1]),
                                           line_slope(line2[0], line2[1]))

        if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range2 and \
           math.fabs(line1[0][1] - line2[0][1]) < self.max_corner_range2 and \
           self.angle_min < corner_angle < self.angle_max:
            corner1 = average_corners(line1[0], line2[0])
            corner2 = line1[1]
            corner3 = line2[1]
            self.corners.append([corner1, corner2, corner3])
        elif math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range2 and \
           math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range2 and \
           self.angle_min < corner_angle < self.angle_max:
            corner1 = average_corners(line1[1], line2[1])
            corner2 = line1[0]
            corner3 = line2[0]
            self.corners.append([corner1, corner2, corner3])
        elif math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range2 and \
             math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range2 and \
             self.angle_min < corner_angle < self.angle_max:
            corner1 = average_corners(line1[1], line2[0])
            corner2 = line1[0]
            corner3 = line2[1]
            self.corners.append([corner1, corner2, corner3])
        elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range2 and \
             math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range2 and \
             self.angle_min < corner_angle < self.angle_max:
            corner1 = average_corners(line1[1], line2[0])
            corner2 = line1[1]
            corner3 = line2[0]
            self.corners.append([corner1, corner2, corner3])


    def check_corners(self, line1, line2):
        corner1 = 0
        corner2 = 0
        corner3 = 0
        corner4 = 0
        corner_angle = angle_between_lines(line_slope(line1[0], line1[1]),
                                           line_slope(line2[0], line2[1]))

        if self.angle_min < corner_angle < self.angle_max:
            if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range2 and \
               math.fabs(line1[0][1] - line2[0][1]) < self.max_corner_range2:
                return True
            elif math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range2 and \
                 math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range2:
                return True
            elif math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range2 and \
                 math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range2:
                return True
            elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range2 and \
                 math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range2:
                return True
            else:
                return False

    def sort_bins(self):
        for Bin1 in self.Bins[:]:
            for Bin2 in self.Bins[:]:
                if Bin1 is not Bin2 and Bin1 in self.Bins and Bin2 in self.Bins:
                    if math.fabs(Bin1.center[0] - Bin2.center[0]) < self.max_corner_range5:
                        if Bin1.id < Bin2.id:
                            self.Bins.remove(Bin2)
                        else:
                            self.Bins.remove(Bin1)

    def update_bins(self):
        for Bin in self.Bins[:]:
            Bin.corner1_replace = []
            Bin.corner2_replace = []
            Bin.corner3_replace = []
            Bin.corner4_replace = []
            for corner in self.hough_corners:
                if math.fabs(corner[0] - Bin.corner1[0]) < self.max_corner_range3 and \
                   math.fabs(corner[1] - Bin.corner1[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh:
                        Bin.lastseen += self.corner_update_value
                        #Bin.corner1 = corner
                    Bin.corner1_replace.append(corner)
                    Bin.corner1_updated = 1
                elif math.fabs(corner[0] - Bin.corner2[0]) < self.max_corner_range3 and \
                     math.fabs(corner[1] - Bin.corner2[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh:
                        Bin.lastseen += self.corner_update_value
                        #Bin.corner2 = corner
                    Bin.corner2_replace.append(corner)
                    Bin.corner2_updated = 1
                elif math.fabs(corner[0] - Bin.corner3[0]) < self.max_corner_range3 and \
                     math.fabs(corner[1] - Bin.corner3[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh:
                        Bin.lastseen += self.corner_update_value
                        #Bin.corner3 = corner
                    Bin.corner3_replace.append(corner)
                    Bin.corner3_updated = 1
                elif math.fabs(corner[0] - Bin.corner3[0]) < self.max_corner_range3 and \
                     math.fabs(corner[1] - Bin.corner3[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh:
                        Bin.lastseen += self.corner_update_value
                        #Bin.corner4 = corner
                    Bin.corner4_replace.append(corner)
                    Bin.corner4_updated = 1

            min_corner = 1000000
            potential_replacement = 0
            for replacement in Bin.corner1_replace:
                new_min = (Bin.corner1[0] - replacement[0]) ^ 2 + (Bin.corner1[1] - replacement[1]) ^ 2
                if new_min < min_corner:
                    min_corner = new_min
                    potential_replacement = replacement
            if min_corner < 1000000:
                Bin.corner1 = potential_replacement

            min_corner = 1000000
            potential_replacement = 0
            for replacement in Bin.corner2_replace:
                new_min = (Bin.corner2[0] - replacement[0]) ^ 2 + (Bin.corner2[1] - replacement[1]) ^ 2
                if new_min < min_corner:
                    min_corner = new_min
                    potential_replacement = replacement
            if min_corner < 1000000:
                Bin.corner2 = potential_replacement

            min_corner = 1000000
            potential_replacement = 0
            for replacement in Bin.corner3_replace:
                new_min = (Bin.corner3[0] - replacement[0]) ^ 2 + (Bin.corner3[1] - replacement[1]) ^ 2
                if new_min < min_corner:
                    min_corner = new_min
                    potential_replacement = replacement
            if min_corner < 1000000:
                Bin.corner3 = potential_replacement

            min_corner = 1000000
            potential_replacement = 0
            for replacement in Bin.corner4_replace:
                new_min = (Bin.corner4[0] - replacement[0]) ^ 2 + (Bin.corner4[1] - replacement[1]) ^ 2
                if new_min < min_corner:
                    min_corner = new_min
                    potential_replacement = replacement
            if min_corner < 1000000:
                Bin.corner4 = potential_replacement

            if Bin.corner1_updated == 1 and Bin.corner2_updated == 1 and Bin.corner3_updated == 1 and Bin.corner4_updated == 0:
                Bin.corner4 = (Bin.corner4_locx + Bin.corner1[0], Bin.corner4_locy + Bin.corner1[1])
            if Bin.corner1_updated == 1 and Bin.corner2_updated == 1 and Bin.corner3_updated == 0 and Bin.corner4_updated == 1:
                Bin.corner3 = (Bin.corner3_locx + Bin.corner1[0], Bin.corner3_locy + Bin.corner1[1])
            if Bin.corner1_updated == 1 and Bin.corner2_updated == 0 and Bin.corner3_updated == 1 and Bin.corner4_updated == 1:
                Bin.corner2 = (Bin.corner2_locx + Bin.corner1[0], Bin.corner2_locy + Bin.corner1[1])
            if Bin.corner1_updated == 0 and Bin.corner2_updated == 1 and Bin.corner3_updated == 1 and Bin.corner4_updated == 1:
                Bin.corner1 = (Bin.corner1_locx + Bin.corner2[0], Bin.corner1_locy + Bin.corner2[1])

            if line_distance(Bin.corner1, Bin.corner2) > Bin.distance12 + self.length_trans_thresh or \
               line_distance(Bin.corner1, Bin.corner2) < Bin.distance12 - self.length_trans_thresh and \
               Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"
            elif line_distance(Bin.corner1, Bin.corner3) > Bin.distance13 + self.length_trans_thresh or \
                 line_distance(Bin.corner1, Bin.corner3) < Bin.distance13 - self.length_trans_thresh and \
                 Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"
            elif line_distance(Bin.corner2, Bin.corner4) > Bin.distance24 + self.length_trans_thresh or \
                 line_distance(Bin.corner2, Bin.corner4) < Bin.distance24 - self.length_trans_thresh and \
                 Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"
            elif line_distance(Bin.corner3, Bin.corner4) > Bin.distance34 + self.length_trans_thresh or \
                 line_distance(Bin.corner3, Bin.corner4) < Bin.distance34 - self.length_trans_thresh and \
                 Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"

            elif math.fabs(Bin.angle124 - angle_between_lines(line_slope(Bin.corner1, Bin.corner2), line_slope(Bin.corner2, Bin.corner4))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"
            elif math.fabs(Bin.angle134 - angle_between_lines(line_slope(Bin.corner1, Bin.corner3), line_slope(Bin.corner3, Bin.corner4))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"
            elif math.fabs(Bin.angle312 - angle_between_lines(line_slope(Bin.corner3, Bin.corner1), line_slope(Bin.corner2, Bin.corner1))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"
            elif math.fabs(Bin.angle243 - angle_between_lines(line_slope(Bin.corner2, Bin.corner4), line_slope(Bin.corner3, Bin.corner4))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"

            Bin.center = rect_midpoint(Bin.corner1, Bin.corner2, Bin.corner3, Bin.corner4)

            if line_distance(Bin.corner1, Bin.corner2) < line_distance(Bin.corner1, Bin.corner3):
                Bin.angle = -angle_between_lines(line_slope(Bin.corner1, Bin.corner2), 0)
            else:
                Bin.angle = -angle_between_lines(line_slope(Bin.corner1, Bin.corner3), 0)

            print (Bin.angle / math.pi) * 180

            Bin.lastseen -= 2
            if Bin.lastseen < 0 and Bin in self.Bins:
                self.Bins.remove(Bin)
                print "Bin Lost"

            Bin.corner1_updated = 0
            Bin.corner2_updated = 0
            Bin.corner3_updated = 0
            Bin.corner4_updated = 0
        print "There are", len(self.Bins), "Bins"


    def group_bins(self):
        for Bin1 in self.Bins[:]:
            for Bin2 in self.Bins[:]:
                if Bin1 in self.Bins and Bin2 in self.Bins and Bin1 is not Bin2:
                    if math.fabs(Bin1.center[0] - Bin2.center[0]) < self.center_trans and \
                       math.fabs(Bin1.center[1] - Bin2.center[1]) < self.center_trans:
                        if Bin1.id < Bin2.id:
                            Bin1.lastseen += Bin2.lastseen
                            self.Bins.remove(Bin2)
                        else:
                            Bin2.lastseen += Bin1.lastseen
                            self.Bins.remove(Bin1)


    def draw_bins(self):
        for Bin in self.Bins:
            print Bin.id
            side_a_distance = (line_distance(Bin.corner1, Bin.corner3) + line_distance(Bin.corner2, Bin.corner4)) / 2
            side_b_distance = (line_distance(Bin.corner1, Bin.corner2) + line_distance(Bin.corner3, Bin.corner4)) / 2
            side_a_unit_vector = [(Bin.corner3[0] - Bin.corner1[0]) / side_a_distance,
                                  (Bin.corner3[1] - Bin.corner1[1]) / side_a_distance]
            side_b_unit_vector = [(Bin.corner2[0] - Bin.corner1[0]) / side_b_distance,
                                  (Bin.corner2[1] - Bin.corner1[1]) / side_b_distance]

            pt1 = Bin.corner1
            pt2 = [pt1[0] + side_a_unit_vector[0] * side_a_distance,
                   pt1[1] + side_a_unit_vector[1] * side_a_distance]
            pt3 = [pt1[0] + side_b_unit_vector[0] * side_b_distance,
                   pt1[1] + side_b_unit_vector[1] * side_b_distance]
            pt4 = [pt3[0] + side_a_unit_vector[0] * side_a_distance,
                   pt3[1] + side_a_unit_vector[1] * side_a_distance]

            #Bin.corner1 = pt1
            #Bin.corner2 = pt2
            #Bin.corner3 = pt3
            #Bin.corner4 = pt4

            line_color = (0, 0, 255)
            cv.Line(self.debug_frame, pt1, (int(pt2[0]), int(pt2[1])), line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame, pt1, (int(pt3[0]), int(pt3[1])), line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame, (int(pt4[0]), int(pt4[1])), (int(pt2[0]), int(pt2[1])), line_color, 10, cv.CV_AA,
                    0)
            cv.Line(self.debug_frame, (int(pt4[0]), int(pt4[1])), (int(pt3[0]), int(pt3[1])), line_color, 10, cv.CV_AA,
                    0)

            cv.Circle(self.debug_frame, (int(Bin.center[0]), int(Bin.center[1])), 15, (0, 255, 0), 2, 8, 0)

            font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, .6, .6, 0, 1, 1)
            text_color = (0, 255, 0)
            #print id and last_seen by each bin
            cv.PutText(self.debug_frame, str(Bin.icon),
                       (int(Bin.center[0]), int(Bin.center[1])),
                       font, text_color)


    def sort_corners(self):
        self.final_corners = []

        for corner1 in self.hough_corners[:]:
            for corner2 in self.hough_corners[:]:
                if corner1 is not corner2 and corner1 in self.hough_corners and corner2 in self.hough_corners and \
                   corner1[0] - corner2[0] != 0 and corner1[1] - corner2[1] != 0:
                    if math.fabs(corner1[0] - corner2[0]) < self.corner_sort_thresh and \
                                    math.fabs(corner1[1] - corner2[1]) < self.corner_sort_thresh:
                        self.final_corners.append(corner1)
                        #self.hough_corners.remove(corner2)
                        #self.hough_corners.remove(corner1)
                        break
        return self.final_corners


