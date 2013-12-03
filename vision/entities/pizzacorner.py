from __future__ import division
import math
import cv
#import cv2
import numpy as np
import svr
from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range
#import msvcrt
import random


class Bin(object):
    bin_id = 0
    '''an imaged pizza'''
    def __init__(self, corner_a, corner_b, corner_c, corner_d):
        rng = cv.RNG()
        self.midx = rect_midpointx(corner_a, corner_b, corner_c, corner_d)
        self.midy = rect_midpointy(corner_a, corner_b, corner_c, corner_d)
        self.corner1 = corner_a
        self.corner2 = corner_b
        self.corner3 = corner_c
        self.corner4 = corner_d
        #locx and locy are relative locations of corners when compared to other corners of the same rectangle
        self.corner1_locx = self.corner1[0] - self.corner2[0]
        self.corner1_locy = self.corner1[1] - self.corner2[1]
        self.corner2_locx = self.corner2[0] - self.corner1[0]
        self.corner2_locy = self.corner2[1] - self.corner1[1]
        self.corner3_locx = self.corner3[0] - self.corner1[0]
        self.corner3_locy = self.corner3[1] - self.corner1[1]        
        self.corner4_locx = self.corner4[0] - self.corner1[0]
        self.corner4_locy = self.corner4[1] - self.corner1[1]
        #angle is found according to short side
        if line_distance(corner_a, corner_c) < line_distance(corner_a, corner_b):
            self.angle = -angle_between_lines(line_slope(corner_a, corner_c), 0)
        else:
            self.angle = -angle_between_lines(line_slope(corner_a, corner_b), 0)
        self.id = 0   #id identifies which pizza your looking at
        self.last_seen = 2 #how recently you have seen this pizza
        self.seencount = 1 #how many times you have seen this pizza (if you see it enough it becomes confirmed)
        r = int(cv.RandReal(rng)*255)
        g = int(cv.RandReal(rng)*255)
        b = int(cv.RandReal(rng)*255)
        self.debug_color = cv.RGB(r, g, b)
        self.object = random.choice(["A", "B", "C", "D"])

def line_distance(corner_a, corner_b):
    distance = math.sqrt((corner_b[0] - corner_a[0])**2 + 
                         (corner_b[1] - corner_a[1])**2)
    return distance

def line_slope(corner_a, corner_b):
    if corner_a[0] != corner_b[0]:
        slope = (corner_b[1] - corner_a[1]) / (corner_b[0] - corner_a[0])
        return slope

def angle_between_lines(slope_a, slope_b):
    if slope_a is not None and slope_b is not None and (1+slope_a*slope_b) != 0:
        angle = math.atan((slope_a - slope_b) / (1+slope_a*slope_b))
        return angle
    else: 
        angle = 0
        return angle

def midpoint(corner_a, corner_b):
    midpoint_x = (corner_b[0] - corner_a[0])/2 + corner_a[0]
    midpoint_y = (corner_b[1] - corner_a[1])/2 + corner_a[1]
    return (midpoint_x, midpoint_y)

def midpointx(corner_a, corner_b):
    midpoint_x = (corner_b[0] - corner_a[0])/2 + corner_a[0]
    return midpoint_x

def midpointy(corner_a, corner_b):
    midpoint_y = (corner_b[1] - corner_a[1])/2 + corner_a[1]
    return midpoint_y

def rect_midpoint(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0])/4
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1])/4
    return [midpoint_x, midpoint_y]

def rect_midpointx(corner_a, corner_b, corner_c, corner_d):
    midpoint_x = (corner_a[0] + corner_b[0] + corner_c[0] + corner_d[0])/4
    return midpoint_x

def rect_midpointy(corner_a, corner_b, corner_c, corner_d):
    midpoint_y = (corner_a[1] + corner_b[1] + corner_c[1] + corner_d[1])/4
    return midpoint_y


class PizzaCornerEntity(VisionEntity):
    
    def init(self):

        #Adaptive threshold parameters
        self.adaptive_thresh_blocksize = 35
        self.adaptive_thresh = 6 #12

        #Good features parameters

        self.max_corners = 18
        self.quality_level = .6

        self.min_distance = 10
        self.good_features_blocksize = 24
        
        #min and max angle in order to only accept rectangles
        self.angle_min = math.pi/2-.1
        self.angle_max = math.pi/2+.1
        self.angle_min2 = math.pi/2-.1
        self.angle_max2 = math.pi/2+.1

        #how close the sizes of parallel lines of a bin must be to eachother
        self.size_threshold = 30
        #How close to the ideal 2:1 ratio the bin sides must be
        self.ratio_threshold = 1.5
        
        #How far a bin may move and still be considered the same bin
        self.MaxTrans = 40

        #Minimum number the seencount can be before the bin is lost
        self.last_seen_thresh = 0
        #How many times a bin must be seen to be accepted as a confirmed bin
        self.min_seencount = 5
 
        #How close the perimeter of a bin must be when compared to the perimeter of other bins
        self.perimeter_threshold = 0.08

        self.corners = []
        self.candidates = []
        self.confirmed  = []
        self.new = []
        self.angles = []


    def process_frame(self, frame):
        self.debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
        self.test_frame = cv.CreateImage(cv.GetSize(frame),8,3)

        cv.Copy(frame, self.debug_frame)
        cv.Copy(frame, self.test_frame)

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 1)
        cv.Copy(hsv, binary)
        cv.SetImageCOI(hsv, 0)
   
        #Adaptive Threshold
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
        
   
        cv.CvtColor(binary, self.debug_frame, cv.CV_GRAY2RGB)
        
        #Find Corners
        temp1 = cv.CreateImage(cv.GetSize(frame), 8, 1)
        temp2 = cv.CreateImage(cv.GetSize(frame), 8, 1)
        self.corners = cv.GoodFeaturesToTrack(binary, temp1, temp2, self.max_corners, self.quality_level, self.min_distance, None, self.good_features_blocksize, 0, 0.4) 
        
        #Display Corners
        for corner in self.corners:
            corner_color = (0,0,255)
            text_color = (0, 255, 0)
            font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, .6, .6, 0, 1, 1)
            cv.Circle(self.debug_frame, (int(corner[0]),int(corner[1])), 15, corner_color, 2,8,0)
                
        #Find Candidates

        for corner1 in self.corners:
            for corner2 in self.corners:
                for corner3 in self.corners:
                    for corner4 in self.corners:
                        #Checks that corners are not the same and are in the proper orientation
                        if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and \
                           corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0] and \
                           corner4[1] != corner3[1] and corner4[1] != corner2[1] and corner4[1] != corner1[1] and \
                           corner3[1] != corner2[1] and corner3[1] != corner1[1] and corner2[1] != corner1[1] and \
                           corner2[0] >= corner3[0] and corner1[1] >= corner4[1] and corner2[0] >= corner1[0] and \
                           math.fabs(corner1[0] - corner4[0]) > self.min_corner_distance and \
                           math.fabs(corner1[1] - corner4[1]) > self.min_corner_distance and \
                           math.fabs(corner2[0] - corner3[0]) > self.min_corner_distance and \
                           math.fabs(corner2[1] - corner3[1]) > self.min_corner_distance:
                            #Checks that the side ratios are correct
                            if math.fabs(line_distance(corner1, corner3) - line_distance(corner2, corner4)) < self.size_threshold and \
                               math.fabs(line_distance(corner1, corner2) - line_distance(corner3, corner4)) < self.size_threshold and \
                               math.fabs(line_distance(corner1, corner3) / line_distance(corner1, corner2)) < .5 * self.ratio_threshold:
                                #Checks that angles are roughly 90 degreesmath.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4)))
                                angle_cnr_2 = math.fabs(angle_between_lines(line_slope(corner1, corner2), line_slope(corner2, corner4)))
                                if self.angle_min < angle_cnr_2 < self.angle_max:
                                    angle_cnr_3 = math.fabs(angle_between_lines(line_slope(corner1, corner3), line_slope(corner3, corner4)))
                                    if self.angle_min2 < angle_cnr_3 < self.angle_max2:
                                        new_bin = Bin(corner1, corner2, corner3, corner4)
                                        self.match_bins(new_bin)
        self.sort_bins()
        
        '''                 
    #START SHAPE PROCESSING
    
    #TODO load these ONCE somewhere
    samples = np.loadtxt('generalsamples.data',np.float32)
    responses = np.loadtxt('generalresponses.data',np.float32)
    responses = responses.reshape((responses.size,1))
    model = cv2.KNearest()
    model.train(samples,responses)
    
        for bin in self.confirmed:
            try:
                bin.speedlimit
            except:
                continue
            transf = cv.CreateMat(3, 3, cv.CV_32FC1)
        corner_orders = [
            [bin.corner1, bin.corner2, bin.corner3, bin.corner4], #0 degrees
            [bin.corner4, bin.corner3, bin.corner2, bin.corner1], #180 degrees
            [bin.corner2, bin.corner4, bin.corner1, bin.corner3], #90 degrees
            [bin.corner3, bin.corner1, bin.corner4, bin.corner2], #270 degrees
            [bin.corner3, bin.corner4, bin.corner1, bin.corner2], #0 degrees and flipped X
            [bin.corner2, bin.corner1, bin.corner4, bin.corner3], #180 degrees and flipped X
            [bin.corner1, bin.corner3, bin.corner2, bin.corner4], #90 degrees and flipped X
            [bin.corner4, bin.corner2, bin.corner3, bin.corner1]] #270 degrees andf flipped X
            for i in range(0, 8):
            cv.GetPerspectiveTransform(
                corner_orders[i],
                [(0, 0), (0, 256), (128, 0), (128, 256)],
                transf
            )
                shape = cv.CreateImage([128, 256], 8, 3)
                cv.WarpPerspective(frame, shape, transf)
                
            shape_thresh = np.zeros((256-104,128,1), np.uint8)
            j = 104
            while j<256:
                i = 0
                while i<128:
                    pixel = cv.Get2D(shape, j, i)
                if int(pixel[2]) > (int(pixel[1]) + int(pixel[0])) * 0.7:
                    shape_thresh[j-104,i] = 255
                else:
                    shape_thresh[j-104,i] = 0
                i = i+1
                j = j+1
            cv2.imshow("Bin " + str(i), shape_thresh)
            contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                    if cv2.contourArea(cnt)>50:
                        [x,y,w,h] = cv2.boundingRect(cnt)
                        if  h>54 and w>36:
                                roi = thresh[y:y+h,x:x+w]
                                roismall = cv2.resize(roi,(10,10))
                                roismall = roismall.reshape((1,100))
                                roismall = np.float32(roismall)
                                retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
                                digit_tuples.append( (x, int((results[0][0]))) )
                    
                    if len(digit_tuples) == 2:
                        digit_tuples_sorted = sorted(digit_tuples, key=lambda digit_tuple: digit_tuple[0])
                speedlimit = 0
                for i in range(0, len(digit_tuples_sorted)):
                        speedlimit = speedlimit * 10 + digit_tuples_sorted[i][1]
                    bin.speedlimit = speedlimit
                    print "Found speed limit: " + str(speedlimit)
                    break
                else:
                    print "Unable to determine speed limit"

        #... TODO more
        #END SHAPE PROCESSING
    '''
        
        
        svr.debug("Pizza", self.debug_frame)
        svr.debug("Pizza2", self.test_frame)

        self.output.pizza = self.confirmed
        anglesum = 0
        for Box in self.output.pizza:
            Box.theta = (Box.midx - frame.width/2) * 37 / (frame.width/2)
            Box.phi = -1 * (Box.midy - frame.height/2) * 36 / (frame.height/2)
            anglesum += Box.angle
        if len(self.output.pizza) > 0:           
            self.output.orientation = anglesum/len(self.output.pizza)
        else:
            self.output.orientation = None
        self.return_output()


    def match_bins(self, target):
        existing = 0
        #update if candidate
        for candidate in self.candidates:
            if math.fabs(target.midx-candidate.midx) < self.MaxTrans and \
               math.fabs(target.midy-candidate.midy) < self.MaxTrans and \
               target.id != candidate.id:
                candidate.midx = target.midx
                candidate.midy = target.midy
                candidate.corner1 = target.corner1
                candidate.corner2 = target.corner2
                candidate.corner3 = target.corner3
                candidate.corner4 = target.corner4
                candidate.angle = target.angle
                candidate.corner1_locx = candidate.corner1[0] - candidate.corner2[0]
                candidate.corner1_locy = candidate.corner1[1] - candidate.corner2[1]
                candidate.corner2_locx = candidate.corner2[0] - candidate.corner1[0]
                candidate.corner2_locy = candidate.corner2[1] - candidate.corner1[1]
                candidate.corner3_locx = candidate.corner3[0] - candidate.corner1[0]
                candidate.corner3_locy = candidate.corner3[1] - candidate.corner1[1]        
                candidate.corner4_locx = candidate.corner4[0] - candidate.corner1[0]
                candidate.corner4_locy = candidate.corner4[1] - candidate.corner1[1]
                if candidate.last_seen < 20:
                    candidate.last_seen += 3
                candidate.seencount += 1
                existing = 1
        #update if confirmed
        for confirmed in self.confirmed:
            for confirmed2 in self.confirmed:
                if confirmed.midx == confirmed2.midx and \
                   confirmed.midy == confirmed2.midy and \
                   confirmed.id != confirmed2.id:
                    if confirmed.id < confirmed2.id:
                        self.confirmed.remove(confirmed2)

            if math.fabs(target.midx-confirmed.midx) < self.MaxTrans and \
               math.fabs(target.midy-confirmed.midy) < self.MaxTrans and \
               target.id != confirmed.id:
                confirmed.midx = target.midx
                confirmed.midy = target.midy
                confirmed.corner1 = target.corner1
                confirmed.corner2 = target.corner2
                confirmed.corner3 = target.corner3
                confirmed.corner4 = target.corner4
                confirmed.angle = target.angle
                if confirmed.last_seen < 20:
                    confirmed.last_seen += 3
                confirmed.seencount += 1
                existing = 1
        if existing == 0:
            print "found candidate"
            target.id = Bin.bin_id
            Bin.bin_id += 1
            self.candidates.append(target)


    def sort_bins(self):
        #promote candidate to confirmed if seen enough times, if it hasn't been seen, delete the bin
        for candidate in self.candidates:

            candidate.last_seen -= 1
            if candidate.last_seen < self.last_seen_thresh:
                self.candidates.remove(candidate) 
                print "lost"
                continue
            if candidate.seencount > self.min_seencount:
                self.confirmed.append(candidate)
                self.candidates.remove(candidate)
                print "confirmed"
                continue

        self.min_perimeter = 500000        
        self.angles = []
        for confirmed in self.confirmed:
            if 0 < line_distance(confirmed.corner1, confirmed.corner3)*2 + line_distance(confirmed.corner1, confirmed.corner2)*2 < self.min_perimeter:
                self.min_perimeter = line_distance(confirmed.corner1, confirmed.corner3)*2 + line_distance(confirmed.corner1, confirmed.corner2)*2
            #print confirmed.angle/math.pi*180
            self.angles.append(cv.Round(confirmed.angle/math.pi*180/10)*10)

        #compare perimeter of existing bins. If a bin is too much bigger than the others, it is deleted. This is done to get rid of bins found based of 3 bins
        for confirmed in self.confirmed:
            if math.fabs(line_distance(confirmed.corner1, confirmed.corner3)*2 + math.fabs(line_distance(confirmed.corner1, confirmed.corner2)*2) - self.min_perimeter) > self.min_perimeter*self.perimeter_threshold and line_distance(confirmed.corner1, confirmed.corner3)*2 + line_distance(confirmed.corner1, confirmed.corner2)*2 > self.min_perimeter:
                print "perimeter error (this is a good thing)"
                print math.fabs(line_distance(confirmed.corner1, confirmed.corner3)*2 + math.fabs(line_distance(confirmed.corner1, confirmed.corner2)*2) - self.min_perimeter), "is greater than", self.min_perimeter*self.perimeter_threshold
                print "yay?"

                confirmed.last_seen -= 5

                continue

            
            confirmed.last_seen -= 1
            if confirmed.last_seen < self.last_seen_thresh:
                self.confirmed.remove(confirmed) 
                print "lost confirmed"
                continue
            #draw bins
            line_color = (confirmed.corner1[1]/2, confirmed.corner2[1]/2, confirmed.corner4[1]/2)
            cv.Circle(self.debug_frame, (int(confirmed.midx), int(confirmed.midy)), 15, line_color, 2, 8, 0)
            pt1 = (cv.Round(confirmed.corner1[0]), cv.Round(confirmed.corner1[1]))
            pt2 = (cv.Round(confirmed.corner2[0]), cv.Round(confirmed.corner2[1]))
            cv.Line(self.debug_frame, pt1, pt2, line_color, 1, cv.CV_AA, 0)
            pt2 = (cv.Round(confirmed.corner2[0]), cv.Round(confirmed.corner2[1]))
            pt4 = (cv.Round(confirmed.corner4[0]), cv.Round(confirmed.corner4[1]))
            pt3 = (cv.Round(confirmed.corner3[0]),cv.Round(confirmed.corner3[1]))
            cv.Line(self.debug_frame, pt2, pt4, line_color, 1, cv.CV_AA, 0)
            cv.Line(self.debug_frame, pt3, pt4, line_color, 1, cv.CV_AA, 0)
            cv.Line(self.debug_frame, pt1, pt3, line_color, 1, cv.CV_AA, 0)
            font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, .6, .6, 0, 1, 1)
            text_color = (0, 255, 0)
            #print id and last_seen by each bin
            cv.PutText(self.debug_frame, str(confirmed.id), (int(confirmed.midx), int(confirmed.midy)), font, confirmed.debug_color)
            cv.PutText(self.debug_frame, str(confirmed.last_seen), (int(confirmed.midx-20), int(confirmed.midy-20)), font, confirmed.debug_color)


#TODO Lower how much it gets from seeing corners to reduce things. Add variable for max last_seen instead of stating in code. Delete lost[] code or archive useful parts. fix perimeter error. get rid of bbb's. Fix integration of flux capacitors. Reduce interference from time lords. Prevent the rise of skynet. Speed up the processes so they can make the kessler run in under 12 parsecs. Go plaid in ludicrous speed. (NOTE: It's a Unix System, I know this). 



#Ideas: lower maxtrans, fix numerous bins sharing the same spot.
