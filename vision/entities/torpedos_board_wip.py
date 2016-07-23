"""
Vision code for doing the torpedos task at robosub 2016"""

from __future__ import division
import math
import random
import time
import logging
import itertools
import math

import cv, cv2
import numpy as np

import svr
from base import VisionEntity
import libvision
from entity_types.bin import Bin
#import Image

DEBUG_BIN_IDENTIFICATION = False
DEBUG_LINE_GROUPS = False
DEBUG_SHOW_RED_LINES = False

class Board(object):
    def __init__(self):
        pass

class Line(object):
    def __init__(self, line):
        self.rho = line[0]
        self.theta = line[1]
        self.groupID = None

        self.x = self.rho*np.cos(self.theta)
        self.y = self.rho*np.sin(self.theta)

        self.b, self.m = self.get_pointslope()

    def get_pointslope(self):
        m = -self.x / self.y
        b = self.y - m*self.x
        return (b,m)
        
    @staticmethod
    def find_intersection(line1, line2):
        top = line1.y - line2.y*line1.m/line2.m - line1.x*line1.m
        bottom = 1 - line1.m/line2.m

        y_intersect = top/bottom
        x_intersect = (y_intersect - line1.y)/line1.m + line1.x
        return (x_intersect,y_intersect)

    @staticmethod
    def find_all_intersections(lines, max_x, max_y):
        points = []
        print "checking for intersections"
        for line1,line2 in itertools.combinations(lines,2):
            print "comparing {} and {}".format(line1, line2)
            found_point = Line.find_intersection(line1,line2)
            print found_point

            # if invalid
            if (math.isnan(found_point[0])) or  (math.isnan(found_point[1])):
                continue

            if (math.isinf(found_point[0])) or  (math.isinf(found_point[1])):
                continue

            found_x = found_point[0]
            found_y = found_point[1]
            if (not (0 <= found_x < max_x)) or (not (0 <= found_y < max_y)):
                continue

            # find matches
            no_match = True
            for point in points:
                if np.isclose(point[0],found_point[0], atol=10) \
                  and  np.isclose(point[1],found_point[1], atol=10):
                    no_match = False

            #print found_point
            if no_match:
                #print found_point
                x = int(round(found_point[0]))
                y = int(round(found_point[1]))
                xy = (x,y)
                points.append(xy)

        #print points
        return points
        

    def __repr__(self):
        return repr( (self.rho, self.theta) )

    def __getitem__(self, i):
        return (self.rho, self.theta)[i]

    """
    def __str__(self):
        return "{}, {}".format(self.rho, self.theta)
    """

def line_group_accept_test(line_group, line, max_range_r, max_range_t):
    '''
    Returns True if the line should be let into the line group.

    First calculates what the range of rho values would be if the line were
    added.  If the range is greater than max_range the line is rejected and
    False is returned.

    ARGS:
      line_group--a list of lines
      line--line to be tested
      ...
    '''
    #print "linegrp"
    #print line_group
    # unwrap rho, theta stuff
    rho, theta = get_unwrapped_line(line)
    max_rho = rho
    min_rho = rho

    for l in line_group:
        l = get_unwrapped_line(l)
        if l[0] > max_rho:
            max_rho = l[0]
        if l[0] < min_rho:
            min_rho = l[0]

    max_theta = theta
    min_theta = theta

    for l in line_group:
        l = get_unwrapped_line(l)
        if l[1] > max_theta:
            max_theta = l[1]
        if l[1] < min_theta:
            min_theta = l[1]
    
    in_range_rho = (max_rho - min_rho < max_range_r)
    in_range_theta = (max_theta - min_theta < max_range_t)
    if in_range_rho and in_range_theta:
        return True
    else:
        #print "fail logic: rho={}, theta={}".format(in_range_rho, in_range_theta)
        if not in_range_rho:
            #print "line_group rho={}".format(line_group[0])
            #print "min_rho={}".format(min_rho)
            #print "max_rho={}".format(max_rho)
            pass

def get_unwrapped_line(line):
    # if input is a Line object
    if isinstance(line, Line):
        flipped = line.rho < 0
        if flipped:
            return Line( (-line.rho, line.theta-np.pi) )
        else:
            return line

    # if input is just a line tuple
    else:
        flipped = line[0] < 0
        if flipped:
            return (-line[0], line[1]-np.pi)
        else:
            return line


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class TorpedosEntity(VisionEntity):
    name = "Torpedos"

    def init(self):
        #self.adaptive_thresh_blocksize = 25  # without canny, 15
        #self.adaptive_thresh = 12  # without canny, 8
        #self.mid_sep = 50
        #self.min_area = 4500
        #self.max_area = 14000
        #self.recent_id = 1
        #self.trans_thresh = 25

        #self.candidates = []
        #self.confirmed = []

        #self.lastseen_thresh = 1
        #self.seencount_thresh = 2
        #self.lastseen_max = 5
        self.C = 20
        self.blk_size = 50
        
        pass
        # frame parameters
        self.frame_width = None
        self.frame_height = None

        # debug parameters
        self.step = 0

        # bin tracking parameters
        self.candidates = []
        self.confirmed = []
        self.recent_id = 0
        self.seencount_thresh = 15
        self.lastseen_thresh = 1
        self.trans_thresh = 10
        self.lastseen_max = 100

        # line grouping parameters
        self.line_group = []
        self.avg_line_group = []

        # create test parameters
        cv.NamedWindow("Torpedos")
        self.create_trackbar("C", 200) #250
        self.create_trackbar("blk_size", 50) #125
        #self.create_trackbar("param3", 255) #0

    def process_frame(self, frame):
        # This is equivalent to the old routine, but it isn't actually necessary
        #height, width, depth = libvision.cv_to_cv2(frame).shape
        #self.debug_frame = np.zeros((height, width, 3), np.uint8)


        # init
        self.step = 0

        # other init
        time.sleep(0.1)
        print ""

        # print debug data
        """
        print("param1={}, param2={}, param3={}".format(
            self.param1,
            self.param2,
            self.param3,
        ))"""
        
        # attain initial frames
        raw_frame   = libvision.cv_to_cv2(frame)
        self.frame_height,self.frame_width = raw_frame.shape[0:2]

        # run processing algorithms
        #self.bin_algorithm1(raw_frame, debug=True)
        self.backplane_algorithm2(raw_frame, debug=True)
        #import pdb; pdb.set_trace()

    

    def backplane_algorithm1(self, frame, debug=False):
        debug_frame = frame
        # thresholding: note, channel 0 (blue) is especially good
        # for discerning the board from the water.
        blur = 3
        smooth_frame = cv2.medianBlur(frame, blur, blur)

        channel_frame = self.get_channel(smooth_frame, 0, True)
        

        # Get Edges
        edge_frame = cv2.Canny(channel_frame, 30, 40)
        self.print_frame("edges", edge_frame)

        # get lines
        thresh = clamp(self.param1,1, 2000)
        lines = cv2.HoughLines(edge_frame,
                                rho=self.param2+1,
                                theta=np.pi/float(self.param3+1),
                                threshold=thresh)

        try:
            self.lines_to_consider = 6
            lines = lines[0][:self.lines_to_consider]
        except TypeError:
            lines = []


        #import pdb; pdb.set_trace()

        if len(lines) > 1:
            cv_lines = libvision.misc.cv2_to_cv(debug_frame)
            libvision.misc.draw_lines(cv_lines, lines)
            cv_lines = libvision.misc.cv_to_cv2(cv_lines)
            pass
        else: 
            cv_lines = debug_frame

        self.print_frame("lines", cv_lines)

    def select_board_contour(self, contours):
        return #contours[0]

    def backplane_algorithm2(self, frame, debug=False):
        debug_frame = frame
        # thresholding: note, channel 0 (blue) is especially good
        # for discerning the board from the water.
        blur = 3
        smooth_frame = cv2.medianBlur(frame, blur, blur)
        channel_frame = self.get_channel(frame, 0, True)

        # threshold should be enough to make the target standout from other objects in the environment
        blk = self.blk_size*2 + 3
        threshold_frame = cv2.adaptiveThreshold(channel_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blk, self.C)
        self.print_frame("thresholding", threshold_frame)
        threshold_frame = self.morphology(threshold_frame, [-14,14])
        self.print_frame("thresholding", threshold_frame)
        
        # Find contours of every shape present after threshold
        contours, hierarchy = cv2.findContours(threshold_frame,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        
        #TODO: select contour with largest area
        self.select_board_contour(contours)

        #
        contour_frame = frame*0
        #cv2.drawContours(debug_frame, contours, -1, (255, 100, 255), -1)
        cv2.drawContours(contour_frame, contours, -1, (255, 100, 255), -1)

        # #########
        # part 2: get edges
        ##############
        # Get Edges
        edge_frame = cv2.Canny(contour_frame, 30, 40)
        self.print_frame("edges", edge_frame)

        # get lines
        #thresh = clamp(self.param1,1, 2000)
        lines = cv2.HoughLines(edge_frame,
                                rho=1,
                                theta=np.pi/180.0,
                                threshold=40)

        try:
            lines = lines[0][:]
        except TypeError:
            lines = []


        #import pdb; pdb.set_trace()
        if DEBUG_SHOW_RED_LINES:
            if len(lines) > 1:
                cv_lines = libvision.misc.cv2_to_cv(debug_frame)
                libvision.misc.draw_lines(cv_lines, lines)
                cv_lines = libvision.misc.cv_to_cv2(cv_lines)
                pass
            else: 
                cv_lines = debug_frame
            self.print_frame("lines", cv_lines)

        # ######
        # part 3: eliminate duplicates
        # ######

        # convert lines to objects
        lines = self.objectify_cv_lines(lines)

        self.clear_line_groups()
        for n,line in enumerate(lines):
            if DEBUG_LINE_GROUPS:
                print "analyzing line{}: {}".format(n,line)
            self.match_line_group(line)

        # print debug messages
        if DEBUG_LINE_GROUPS:
            print "---"
            print "printing line groups:"
            for i,group in enumerate(self.line_group):
                print "group{}".format(i)
                for line in group:
                    print line


        # convert groups to averages
        if DEBUG_LINE_GROUPS:
            print "---"
        self.avg_line_group = []
        for group in self.line_group:
            line = self.avg_group(group)
            self.avg_line_group.append(line)

            if DEBUG_LINE_GROUPS:
                print line

        lines = self.avg_line_group
        if len(lines) > 1:
            cv_lines = libvision.misc.cv2_to_cv(debug_frame)
            libvision.misc.draw_linesC(cv_lines, lines[:4], (255,100,255))
            cv_lines = libvision.misc.cv_to_cv2(cv_lines)
            pass
        else: 
            cv_lines = debug_frame

        self.print_frame("lines", debug_frame)
        
        # #######
        # part 4: asses for board object
        # #######
        if len(lines) > 1:
            points = Line.find_all_intersections(lines, self.frame_width, self.frame_height)
            print points

            for point in points:
                cv2.circle(debug_frame, point, 2, (255,255,255), 2)

        self.print_frame("points", debug_frame)
        """
        if len(self.avg_line_group) == 4:
            corners = p1,p2,p3,p4
            if self.board = None:
                self.board = Board(corners)
            else:
                self.board.updateCorners(corners)

        """
        """
        # if there are enough contours for at least one bin
        if len(contours) > 1:
            cv2.drawContours(debug_frame, contours, -1, (255, 100, 255), 1)

            for n, cnt in enumerate(contours):
                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

        # Get Edges
        edge_frame = cv2.Canny(channel_frame, 30, 40)
        self.print_frame("edges", edge_frame)

        # get lines
        thresh = clamp(self.param1,1, 2000)
        lines = cv2.HoughLines(edge_frame,
                                rho=self.param2+1,
                                theta=np.pi/float(self.param3+1),
                                threshold=thresh)

        try:
            self.lines_to_consider = 6
            lines = lines[0][:self.lines_to_consider]
        except TypeError:
            lines = []


        #import pdb; pdb.set_trace()

        if len(lines) > 1:
            cv_lines = libvision.misc.cv2_to_cv(debug_frame)
            libvision.misc.draw_lines(cv_lines, lines)
            cv_lines = libvision.misc.cv_to_cv2(cv_lines)
            pass
        else: 
            cv_lines = debug_frame

        self.print_frame("lines", cv_lines)
        """

    def avg_group(self, lines):
        rho_sum = 0
        theta_sum = 0


        # accumulate rho and theta values
        for line in lines:
            # check if line if flipped around
            flipped = (line.rho < 0)

            if not flipped:
                rho_sum += line.rho
                theta_sum += line.theta
            else:
                rho_sum += -line.rho
                theta_sum += line.theta - np.pi

        # average the values
        avg_rho = rho_sum / float(len(lines))
        avg_theta = theta_sum / float(len(lines))

        # if line is in the nether region theta-wise, flip it.
        if avg_theta < 0:
            avg_rho = -avg_rho
            avg_theta += np.pi

        return Line( (avg_rho, avg_theta) )
        
    def objectify_cv_lines(self, lines):
        line_list = []
        for line in lines:
            line_list.append( Line(line) )

        return line_list
    
    def clear_line_groups(self):
        self.line_group = []

    def match_line_group(self, line):
        if len(self.line_group) == 0:
            self.line_group.append([line])
            return
        
        match_found = False
        for i,group in enumerate(self.line_group):
            # check each line_group to see if there's a match
            if line_group_accept_test(group, line, 20, np.pi/10.0):
                self.line_group[i].append(line)
                match_found = True

                if DEBUG_LINE_GROUPS:
                    print "line{} accepted into group{}".format(line,i)
                
                break
        
        # if no match was found, create a new line group
        if not match_found:
            self.line_group.append( [line] )

            if DEBUG_LINE_GROUPS:
                print "line{} is a new line. creating group{}.".format(line,i+1)
            
            pass

        

    def get_channel(self, in_frame, channel, debug=False):
        if channel >= 3:
            out_frame = cv2.cvtColor(in_frame, cv2.COLOR_BGR2HSV) 
            channel -= 3
        else:
            out_frame = in_frame

        # isolate channel
        out_frame = out_frame[:,:,channel]

        if debug:
            self.print_frame('channel_frame'+str(channel), out_frame)

        return out_frame
    
    def bin_algorithm1(self, frame, debug=False):
        debug_frame = frame

        # thresholding
        adaptive_frame = self.adaptive_threshold(frame, channel=1, 
                                                 blk_size=13, 
                                                 thresh=18)

        self.print_frame("adaptive", adaptive_frame)

        despeckled_frame = self.morphology(adaptive_frame, [-3,3])

        #print contours
        self.raw_bins = []

        self.raw_bins = self.find_bins(despeckled_frame,
                                       min_area=self.param1,
                                       max_area=self.param2,
                                       debug_frame=debug_frame)


        self.print_frame("debug",debug_frame)
        if DEBUG_BIN_IDENTIFICATION:
            print "candidates={}, confirmed={}".format(len(self.candidates), len(self.confirmed))
        
        # match, sort, and draw
        for bin in self.raw_bins:
            self.match_bins(bin)

        print "candidates={}, confirmed={}".format(len(self.candidates), len(self.confirmed))
        
        self.sort_bins()
        self.draw_bins(debug_frame)

        self.print_frame("debug", debug_frame)


        
    def adaptive_threshold(self, in_frame, channel, blk_size, thresh, blur=0):
        if channel >= 3:
            in_frame = cv2.cvtColor(in_frame, cv2.COLOR_BGR2HSV) 
            channel -= 3

        # isolate channel
        frame = in_frame[:,:,channel]
        self.print_frame('channel_frame', frame)

        # Thresholding
        frame = cv2.adaptiveThreshold(frame, 255,
                        cv2.ADAPTIVE_THRESH_MEAN_C,
                        cv2.THRESH_BINARY_INV,
                        blk_size,
                        thresh)
                                                 
        # return
        return frame

    def morphology(self, frame, sequence):

        for val in sequence:
            # perform transformation
            if val > 0:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (val, val))
                frame = cv2.dilate(frame, kernel)
            elif val < 0:
                val = -val
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (val, val))
                frame = cv2.erode(frame, kernel)
            else:
                pass #do nothing

        return frame

    def find_bins(self, frame, min_area, max_area, debug_frame):
        # empty variables
        discovered_bins = []

        # Find contours of every shape present after threshold
        contours, hierarchy = cv2.findContours(frame,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

        # if there are enough contours for at least one bin
        if len(contours) > 1:
            cv2.drawContours(debug_frame, contours, -1, (255, 100, 255), 1)

            for n, cnt in enumerate(contours):
                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

                # test aspect ratio & area, create bin if matches
                (x, y), (w, h), theta = rect
                if w > 0 and h > 0:
                    area = h * w
                    if DEBUG_BIN_IDENTIFICATION:
                        print "for bin{}: area={}".format(n,area)

                    if min_area < area < max_area:
                        #approximate raw contour points to a simpler polygon with less points
                        approx = cv2.approxPolyDP(
                            cnt, 0.01 * cv2.arcLength(cnt, True), True)

                        aspect_ratio = float(h) / w
                        # Depending on the orientation of the bin, "width" may be flipped with height, thus needs 2 conditions for each case

                        if DEBUG_BIN_IDENTIFICATION:
                            print "for bin{}: len={}".format(n,len(approx))

                        if 2 <= len(approx) < 12 and (0.8 < aspect_ratio < 1.2):
                            p1,p2,p3,p4 = (tuple(box[0]), tuple(box[1]), tuple(box[2]), tuple(box[3]))

                            # instantiate a new bin
                            new_bin = Bin(p1,p2,p3,p4)
                            new_bin.id = self.recent_id
                            new_bin.area = area

                            # print "new bin created with slope: ", new_bin.line_slope

                            #print -theta
                            # if theta != 0:
                            #    new_bin.theta = np.pi*(-theta)/180
                            # else:
                            #    new_bin.theta = 0
                            self.recent_id += 1
                            discovered_bins.append(new_bin)

        print "found {} contours. {} are bins.".format(len(contours), len(discovered_bins))
        return discovered_bins
    
    def match_bins(self, target):
        found = 0


        for confirmed_bin in self.confirmed:

            if math.fabs(confirmed_bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(confirmed_bin.midy - target.midy) < self.trans_thresh:

                # raise the found flag
                found = 1

                # update the confirmed bin to match the target bin
                confirmed_bin.midx = target.midx
                confirmed_bin.midy = target.midy
                confirmed_bin.corner1 = target.corner1
                confirmed_bin.corner2 = target.corner2
                confirmed_bin.corner3 = target.corner3
                confirmed_bin.corner4 = target.corner4
                confirmed_bin.theta = target.theta
                confirmed_bin.seencount += 3

                # increment last seen counter until it reaches the cap
                if confirmed_bin.lastseen < self.lastseen_max:
                    confirmed_bin.lastseen += 6

        for candidate_bin in self.candidates:

            if math.fabs(candidate_bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(candidate_bin.midy - target.midy) < self.trans_thresh:
                
                # raise the found flag
                found = 1

                # update the candidate bin to match the target bin
                candidate_bin.midx = target.midx
                candidate_bin.midy = target.midy
                candidate_bin.corner1 = target.corner1
                candidate_bin.corner2 = target.corner2
                candidate_bin.corner3 = target.corner3
                candidate_bin.corner4 = target.corner4
                candidate_bin.theta = target.theta
                candidate_bin.seencount += 3

                # increment last seen counter until it reaches the cap
                if candidate_bin.lastseen < self.lastseen_max:
                    candidate_bin.lastseen += 6

        # if target bin didn't match anything, make it a candidate
        if found == 0:
            self.add_candidate(target)
            target.lastseen += 3


    def add_candidate(self, bin):
        self.candidates.append(bin)
        print "candidate appended"

    def remove_candidate(self, bin):
        self.candidates.remove(bin)
        print "candidate removed"
    
    def sort_bins(self):

        for candidate_bin in self.candidates[:]:
            # auto decrement
            candidate_bin.lastseen -= 2

            # if candidate bin has been seen enough times...
            if candidate_bin.seencount >= self.seencount_thresh:

                self.confirmed.append(candidate_bin)
                self.candidates.remove(candidate_bin)
                print "confirmed appended"

            # else, check if candidate bin has disappeared
            elif candidate_bin.lastseen < self.lastseen_thresh:
                self.remove_candidate(candidate_bin)

        for confirmed_bin in self.confirmed[:]:
            # auto decrement
            confirmed_bin.lastseen -= 1

            # if confirmed bin has disappeared
            if confirmed_bin.lastseen < self.lastseen_thresh:

                self.confirmed.remove(confirmed_bin)
                print "confirmed removed"

    def draw_bins(self, test_frame):
        self.ind_bins = []
        clr = (0, 0, 255)
        for bin in self.confirmed:
            font = cv2.FONT_HERSHEY_SIMPLEX

            bin.patch = self.subimage2(test_frame, (int(bin.midx), int(bin.midy)),
                                       bin.theta, bin.width, bin.height)
            # cv.SaveImage('patch.jpg',patch)

            cv2.circle(test_frame, bin.corner1, 5, clr, -1)
            cv2.circle(test_frame, bin.corner2, 5, clr, -1)
            cv2.circle(test_frame, bin.corner3, 5, clr, -1)
            cv2.circle(test_frame, bin.corner4, 5, clr, -1)
            cv2.circle(test_frame, (int(bin.midx), int(bin.midy)), 5, clr, -1)

            #cv2.rectangle(test_frame, bin.corner1, bin.corner3, clr, 5)
            pts = np.array([bin.corner1, bin.corner2, bin.corner3, bin.corner4], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(test_frame, [pts], True, (255, 0, 0), 4)

            # print bin ID
            """
            cv2.putText(img=test_frame, 
                        text="id=" + str(bin.id), 
                        org=(int(bin.midx) - 50, int(bin.midy) + 40), 
                        fontFace=font, 
                        fontScale=.3, 
                        color=clr, 
                        thickness=1, 
                        lineType=cv2.CV_AA)
            """
            cv2.putText(img=test_frame, 
                        text="corner1", 
                        org=(int(bin.corner1[0]), int(bin.corner1[1])), 
                        fontFace=font, 
                        fontScale=.3, 
                        color=clr, 
                        thickness=1, 
                        lineType=cv2.CV_AA)

            # draw angle line
            m = math.tan(bin.theta)
            pt1 = (int(bin.midx), int(bin.midy))
            pt2 = (int(bin.midx + 10), int((10) * m + bin.midy))
            cv2.line(test_frame, pt1, pt2, clr, 4, 8, 0)

    def subimage(self, image, center, theta, width, height):
        print "theta is:", theta
        theta = theta
        image = libvision.cv2_to_cv(image)
        output_image = cv.CreateImage((int(width), int(height)), image.depth, image.nChannels)
        mapping = np.array([[np.cos(theta), -np.sin(theta), center[0]],
                            [np.sin(theta), np.cos(theta), center[1]]])
        map_matrix_cv = cv.fromarray(mapping)
        print mapping
        cv.GetQuadrangleSubPix(image, output_image, map_matrix_cv)
        return output_image

    def subimage2(self, image, center, theta, width, height):
        #print "theta is:", theta
        M = cv2.getRotationMatrix2D(center, theta / np.pi * 180, 1.0)
        rotated = cv2.warpAffine(image, M, (image.shape[0], image.shape[1]))

        pts = [(center[0] - width / 2, center[1]), (center[0] + width / 2, center[1]), (center[0], center[1] - height / 2), (center[0], center[1] + height / 2)]

        cropped = rotated[int(center[1] - height / 2):int(center[1] + height / 2), int(center[0] - width / 2):int(center[0] + width / 2)]
        #print cropped.shape
        cropped = cropped.copy()
        cv2.circle(rotated, center, 3, (255, 255, 255))
        for pt in pts:
            cv2.circle(rotated, (int(pt[0]), int(pt[1])), 4, (255, 0, 255))
        name = "Patches/" + str(int(theta * 1000)) + ".jpg"
        #print name
        #cv2.imwrite(name, cropped)
        return cropped
    
    def print_frame(self, name, frame, on_svr=False):
        """prints out the given frame locally, or offers to
        stream the image via svr."""

        name = "print{}: {}".format(self.step, name)

        # print using svr
        if on_svr:
            svr.debug(name, frame)

        # print using openCV
        else:   
            self.debug_stream(name, frame)

        # increment step counter
        self.step += 1


"""
        # CV2 Transforms: denoise and convert to hsv
        self.numpy_frame = self.debug_frame.copy()
        self.numpy_frame = cv2.medianBlur(self.numpy_frame, 5)
        self.numpy_frame = cv2.cvtColor(self.numpy_frame, cv2.COLOR_BGR2HSV)

        # Separate the channels convenience later
        (self.frame1, self.frame2, self.frame3) = cv2.split(self.numpy_frame)

        # Change the frame number to determine what channel to focus on
        self.numpy_frame = self.frame3

        # Thresholding
        self.numpy_frame = cv2.adaptiveThreshold(self.numpy_frame,
                                                 255,
                                                 cv2.ADAPTIVE_THRESH_MEAN_C,
                                                 cv2.THRESH_BINARY_INV,
                                                 self.adaptive_thresh_blocksize,
                                                 self.adaptive_thresh)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel = np.ones((2,2), np.uint8)
        self.numpy_frame = cv2.erode(self.numpy_frame, kernel)
        self.numpy_frame = cv2.dilate(self.numpy_frame, kernel)

        # capture frames representing the effect of the adaptive threshold
        self.adaptive_frame = self.numpy_frame.copy()

        # Find contours of every shape present after threshold
        contours, hierarchy = cv2.findContours(self.numpy_frame,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

        self.raw_bins = []
        
        # if there are enough contours for at least one bin
        if len(contours) > 1:
            cv2.drawContours(self.numpy_frame, contours, -1, (255, 255, 255), 3)

            for h, cnt in enumerate(contours):
                #hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)

                # test aspect ratio & area, create bin if matches
                (x, y), (w, h), theta = rect
                if w > 0 and h > 0:
                    area = h * w
                    if self.min_area < area < self.max_area:
                        #approximate raw contour points to a simpler polygon with less points
                        approx = cv2.approxPolyDP(
                            cnt, 0.01 * cv2.arcLength(cnt, True), True)

                        aspect_ratio = float(h) / w
                        # Depending on the orientation of the bin, "width" may be flipped with height, thus needs 2 conditions for each case
                        if 2 <= len(approx) < 12 and (.4 < aspect_ratio < .6 or 1.8 < aspect_ratio < 2.2):
                            new_bin = Bin(tuple(box[0]), tuple(
                                box[1]), tuple(box[2]), tuple(box[3]))
                            new_bin.id = self.recent_id
                            new_bin.area = area

                            # print "new bin created with slope: ", new_bin.line_slope

                            #print -theta
                            # if theta != 0:
                            #    new_bin.theta = np.pi*(-theta)/180
                            # else:
                            #    new_bin.theta = 0
                            self.recent_id += 1
                            self.raw_bins.append(new_bin)

        for bin in self.raw_bins:
            self.match_bins(bin)

        self.sort_bins()
        self.draw_bins()

        self.return_output()
        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(self.adaptive_frame)

        # svr.debug("processed", self.numpy_to_cv)
        # svr.debug("adaptive", self.adaptive_to_cv)
        # svr.debug("debug", self.debug_to_cv)
        self.debug_stream("debug", self.debug_frame)
        self.debug_stream("processed", self.numpy_frame)
        self.debug_stream("adaptive", self.adaptive_frame)
        for bin in self.confirmed:

            print type(bin.patch)
            if (bin.patch.shape[1] != 0) and (bin.patch.shape[0] != 0):
                self.debug_stream("Patch" + str(bin.id), bin.patch)
            # svr.debug("Patch"+str(bin.id),libvision.cv2_to_cv(bin.patch))
            print bin.id

            #svr.debug("Patch" + str(bin.id), bin.patch)

        # TODO, CLEAN THIS UP SOME
    def match_bins(self, target):
        found = 0
        for bin in self.confirmed:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(bin.midy - target.midy) < self.trans_thresh:
                bin.midx = target.midx
                bin.midy = target.midy
                bin.corner1 = target.corner1
                bin.corner2 = target.corner2
                bin.corner3 = target.corner3
                bin.corner4 = target.corner4
                bin.theta = target.theta
                bin.seencount += 3
                if bin.lastseen < self.lastseen_max:
                    bin.lastseen += 6
                found = 1

        for bin in self.candidates:
            if math.fabs(bin.midx - target.midx) < self.trans_thresh and \
               math.fabs(bin.midy - target.midy) < self.trans_thresh:
                bin.midx = target.midx
                bin.midy = target.midy
                bin.corner1 = target.corner1
                bin.corner2 = target.corner2
                bin.corner3 = target.corner3
                bin.corner4 = target.corner4
                bin.theta = target.theta
                bin.seencount += 3
                if bin.lastseen < self.lastseen_max:
                    bin.lastseen += 6
                found = 1
        if found == 0:
            self.candidates.append(target)
            target.lastseen += 3

        # TODO, CLEAN THIS UP SOME
    def sort_bins(self):
        for bin in self.candidates[:]:
            bin.lastseen -= 2
            if bin.seencount >= self.seencount_thresh:
                self.confirmed.append(bin)
                self.candidates.remove(bin)
                print "confirmed appended"
            if bin.lastseen < self.lastseen_thresh:
                self.candidates.remove(bin)
        for bin in self.confirmed[:]:
            bin.lastseen -= 1
            if bin.lastseen < self.lastseen_thresh:
                self.confirmed.remove(bin)
                print "confirmed removed"

    def subimage(self, image, center, theta, width, height):
        print "theta is:", theta
        theta = theta
        image = libvision.cv2_to_cv(image)
        output_image = cv.CreateImage((int(width), int(height)), image.depth, image.nChannels)
        mapping = np.array([[np.cos(theta), -np.sin(theta), center[0]],
                            [np.sin(theta), np.cos(theta), center[1]]])
        map_matrix_cv = cv.fromarray(mapping)
        print mapping
        cv.GetQuadrangleSubPix(image, output_image, map_matrix_cv)
        return output_image

    def subimage2(self, image, center, theta, width, height):
        print "theta is:", theta
        M = cv2.getRotationMatrix2D(center, theta / np.pi * 180, 1.0)
        rotated = cv2.warpAffine(image, M, (image.shape[0], image.shape[1]))

        pts = [(center[0] - width / 2, center[1]), (center[0] + width / 2, center[1]), (center[0], center[1] - height / 2), (center[0], center[1] + height / 2)]

        cropped = rotated[int(center[1] - height / 2):int(center[1] + height / 2), int(center[0] - width / 2):int(center[0] + width / 2)]
        print cropped.shape
        cropped = cropped.copy()
        cv2.circle(rotated, center, 3, (255, 255, 255))
        for pt in pts:
            cv2.circle(rotated, (int(pt[0]), int(pt[1])), 4, (255, 0, 255))
        name = "Patches/" + str(int(theta * 1000)) + ".jpg"
        print name
        #cv2.imwrite(name, cropped)
        return cropped

    def draw_bins(self):
        self.ind_bins = []
        clr = (0, 0, 255)
        for bin in self.confirmed:

            bin.patch = self.subimage2(self.debug_frame, (int(bin.midx), int(bin.midy)),
                                       bin.theta, bin.width, bin.height)
            # cv.SaveImage('patch.jpg',patch)

            cv2.circle(self.debug_frame,
                       bin.corner1, 5, clr, -1)
            cv2.circle(self.debug_frame,
                       bin.corner2, 5, clr, -1)
            cv2.circle(self.debug_frame,
                       bin.corner3, 5, clr, -1)
            cv2.circle(self.debug_frame,
                       bin.corner4, 5, clr, -1)
            cv2.circle(self.debug_frame, (
                int(bin.midx), int(bin.midy)), 5, clr, -1)

            #cv2.rectangle(self.debug_frame, bin.corner1, bin.corner3, clr, 5)
            pts = np.array([bin.corner1, bin.corner2, bin.corner3, bin.corner4], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(self.debug_frame, [pts], True, (255, 0, 0), 4)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.debug_frame, "id=" + str(bin.id), (int(bin.midx) - 50, int(bin.midy) + 40), font, .8, clr, 1, cv2.CV_AA)

            cv2.putText(self.debug_frame, "corner1", (int(bin.corner1[0]), int(bin.corner1[1])), font, .8, clr, 1, cv2.CV_AA)

            # draw angle line
            m = math.tan(bin.theta)
            pt1 = (int(bin.midx), int(bin.midy))
            pt2 = (int(bin.midx + 10), int((10) * m + bin.midy))
            cv2.line(self.debug_frame, pt1, pt2, clr, 4, 8, 0)

"""