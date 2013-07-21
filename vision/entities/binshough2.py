from __future__ import division
import math

import cv

import svr

import random

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range

class Bin(object):
    def __init__(self,corner1, corner2, corner3, corner4):
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4

        
        #ID number used when tracking bins
        self.id = 0

        #decisive type of letter in the bin
        self.type = type

        #center of bin
        self.center = (rect_midpointx(corner1,corner2,corner3,corner4), rect_midpointy(corner1,corner2, corner3, corner4))

        #direction of the bin
        self.angle = angle_between_lines(line_slope(corner1,corner2), 0)

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


        self.distance12 = line_distance(corner1,corner2)
        self.distance13 = line_distance(corner1,corner3)
        self.distance24 = line_distance(corner4,corner2)
        self.distance34 = line_distance(corner3,corner4)

        self.angle124 = angle_between_lines(line_slope(corner1,corner2),line_slope(corner2,corner4))
        self.angle134 = angle_between_lines(line_slope(corner1,corner3),line_slope(corner3,corner4))
        self.angle312 = angle_between_lines(line_slope(corner3,corner1),line_slope(corner1,corner2))
        self.angle243 = angle_between_lines(line_slope(corner2,corner4),line_slope(corner4,corner3))



def line_distance(corner_a, corner_b):
        distance = math.sqrt((corner_b[0]-corner_a[0])**2 + (corner_b[1]-corner_a[1])**2)
        return distance
def line_distance(corner_a, corner_b):
        distance = math.sqrt((corner_b[0]-corner_a[0])**2 + (corner_b[1]-corner_a[1])**2)
        return distance

def line_slope(corner_a, corner_b):
        if corner_a[0] != corner_b[0]:
                slope = (corner_b[1]-corner_a[1])/(corner_b[0]-corner_a[0])
                return slope

def angle_between_lines(slope_a, slope_b):
    if slope_a != None and slope_b != None and (1+slope_a*slope_b) != 0:
        angle = math.atan((slope_a - slope_b)/(1+slope_a*slope_b))
        return angle
    else: 
        angle = 0
        return angle

def midpoint(corner_a, corner_b):
        midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
        midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
        return [midpoint_x, midpoint_y]

def midpointx(corner_a, corner_b):
        midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
        return midpoint_x

def midpointy(corner_a, corner_b):
        midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
        return midpoint_y

def rect_midpointx(corner_a,corner_b,corner_c,corner_d):
        midpoint_x = (corner_a[0]+corner_b[0]+corner_c[0]+corner_d[0])/4
        return midpoint_x

def rect_midpointy(corner_a,corner_b,corner_c,corner_d):
        midpoint_y = (corner_a[1]+corner_b[1]+corner_c[1]+corner_d[1])/4
        return midpoint_y

def average_corners(corner_a,corner_b):
        average_corner = [0,0]
        average_corner[0] = (corner_a[0]+corner_b[0])/2
        average_corner[1] = (corner_a[1]+corner_b[1])/2
        return average_corner

def check_for_corner(line1,line2):
    corner_distance = 10
    angle_clarity_max = math.pi/2+.1
    angle_clarity_min = math.pi/2-.1

    if angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > angle_clarity_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < angle_clarity_max:
        if math.fabs(line1[0][0] - line2[0][0]) < corner_distance or math.fabs(line1[0][1] - line2[0][1]) < corner_distance or math.fabs(line1[1][0] - line2[1][0]) < corner_distance or math.fabs(line1[1][1] - line2[1][1]) < corner_distance:
            return True

    


class BinsHough2Entity(VisionEntity):

    def init(self):
	
#	self.vertical_threshold = 15*math.pi/180  # How close to vertical lines must be
#        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 20
        self.adaptive_thresh_blocksize = 27
        self.adaptive_thresh = 23

        self.max_range = 100

        self.Boxes = []
        self.groups = []

        self.corners = []
        self.hough_corners = []

        self.Bins = []

        #For Probalistic
        self.min_length = 40
        self.max_gap = 7 #40

        #grouping
        self.max_corner_range = 60  #15
        
        #for corner findings
        self.max_corner_range2 = 15

        #for updating
        self.max_corner_range3 = 40

        #for hough corners grouping
        self.max_corner_range4 = 15
        
        #For Rectangle Indentification Variables, look at function

        self.min_corner_distance = 40  #40

        #min and max angle in order to only accept rectangles
        self.angle_min = math.pi/2-.07
        self.angle_max = math.pi/2+.07
        self.angle_min2 = math.pi/2-.03
        self.angle_max2 = math.pi/2+.03

        
        #How close to the ideal 1:1 ratio the bin sides must be
        self.ratio_threshold =1.5

        self.center_thresh = 40

        self.lastseen_thresh = 40

        self.length_trans_thresh = 40
        self.angle_trans_thresh = 5

        self.center_trans = 15

        self.corner_sort_thresh = 60


        self.parallel_sides_length_thresh = 10


        #How close the perimeter of a bin must be when compared to the perimeter of other bins
        self.perimeter_threshold = 1


        self.corner_update_value = 3

        self.bin_id = 0
        

    def process_frame(self, frame):
	self.debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
        og_frame = cv.CreateImage(cv.GetSize(frame),8,3)
	cv.Copy(frame, self.debug_frame)
        cv.Copy(self.debug_frame, og_frame)


        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Set binary image to have saturation channel
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        binary = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        cv.SetImageCOI(hsv, 3)
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
   
        cv.CvtColor(binary,self.debug_frame, cv.CV_GRAY2RGB)
	

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        raw_lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_PROBABILISTIC,
            rho=1,
            theta=math.pi/180,
            threshold=self.hough_threshold,
            param1=self.min_length,
            param2=self.max_gap
        )

	
        lines = []
        

        for line in raw_lines:
            lines.append(line)
            
        #Grouping lines depending on endpoint simularities

        for line1 in lines[:]:
            for line2 in lines[:]:
                if line1 in lines and line2 in lines and line1 != line2:
                    if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range and math.fabs(line1[0][1] - line2[0][1]) < self.max_corner_range and math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range and math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1])> line_distance(line2[0], line2[1]):
                            lines.remove(line2)
                        else:
                            lines.remove(line1)
                    elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range and math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range and math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range and math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range:
                        if line_distance(line1[0], line1[1])> line_distance(line2[0], line2[1]):
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
                    if math.fabs(corner1[0]-corner2[0]) < self.max_corner_range4 and math.fabs(corner1[1]-corner2[1]) < self.max_corner_range4:
                        if corner1[0]>corner2[0]:
                            self.hough_corners.remove(corner2)
                        else:
                            self.hough_corners.remove(corner1)


        for line1 in lines:
            #cv.Line(self.debug_frame,line1[0],line1[1], (0,0,255), 10, cv.CV_AA, 0)
            for line2 in lines:
                if line1 is not line2:
                    self.find_corners(line1,line2)
                       
        for corner1 in self.corners:
            for corner2 in self.corners:
                if math.fabs(corner1[1][0] - corner2[1][0]) < self.max_corner_range2 and math.fabs(corner1[1][1] - corner2[1][1]) < self.max_corner_range2 and math.fabs(corner1[2][0] - corner2[2][0]) < self.max_corner_range2 and math.fabs(corner1[2][1] - corner2[2][1]) < self.max_corner_range2 and math.fabs(corner1[0][0] - corner2[0][0]) > self.max_corner_range2 and math.fabs(corner1[0][1] - corner2[0][1]) > self.max_corner_range2 :  
                    pt1 = (int(corner1[0][0]),int(corner1[0][1]))
                    pt4 = (int(corner2[0][0]),int(corner2[0][1]))
                    pt3 = (int(corner1[1][0]),int(corner1[1][1]))
                    pt2 = (int(corner1[2][0]),int(corner1[2][1]))
                    #line_color = (0,255,0)s
                    #cv.Line(self.debug_frame,pt1,pt2, line_color, 10, cv.CV_AA, 0)                  
                    #cv.Line(self.debug_frame,pt1,pt3, line_color, 10, cv.CV_AA, 0)
                    #cv.Line(self.debug_frame,pt4,pt2, line_color, 10, cv.CV_AA, 0)                  
                    #cv.Line(self.debug_frame,pt4,pt3, line_color, 10, cv.CV_AA, 0)
                    new_bin = Bin(pt1,pt2,pt3,pt4)
                    new_bin.id = self.bin_id
                    self.bin_id +=1
                    if math.fabs(line_distance(pt1,pt2) - line_distance(pt3,pt4)) < self.parallel_sides_length_thresh and math.fabs(line_distance(pt1,pt3) - line_distance(pt2,pt4)) < self.parallel_sides_length_thresh:
                        self.Bins.append(new_bin)
                        print "new_bin"

                elif math.fabs(corner1[1][0] - corner2[2][0]) < self.max_corner_range2 and math.fabs(corner1[1][1] - corner2[2][1]) < self.max_corner_range2 and math.fabs(corner1[2][0] - corner2[1][0]) < self.max_corner_range2 and math.fabs(corner1[2][1] - corner2[1][1]) < self.max_corner_range2 and math.fabs(corner1[0][0] - corner2[0][0]) > self.max_corner_range2 and math.fabs(corner1[0][1] - corner2[0][1]) > self.max_corner_range2 :
                    continue
            
            

                            

                    

        self.corners=[]
        self.final_corners = self.sort_corners() #Results are not used. Experimental corners which have been seen twice, should be only the corners we want, but there were problems
        self.sort_bins()
        self.update_bins()
        self.group_bins()
        self.draw_bins()
              

        for corner in self.hough_corners:
            line_color = [255,0,0]
            cv.Circle(self.debug_frame, corner, 15, (255,0,0), 2,8,0)

        for line in lines:
            line_color = [255,0,0]
            #cv.Line(self.debug_frame,line[0],line[1], line_color, 5, cv.CV_AA, 0)    
            #cv.Circle(self.debug_frame, line[0], 15, (255,0,0), 2,8,0)
            #cv.Circle(self.debug_frame, line[1], 15, (255,0,0), 2,8,0)


        self.output.pizza = self.Boxes
        anglesum = 0
        for Box in self.Boxes:
            Box.theta = (Box.center[0] - frame.width/2) * 37 / (frame.width/2)
            Box.phi = -1 * (Box.center[1] - frame.height/2) * 36 / (frame.height/2)
            anglesum += Box.angle
        if len(self.output.pizza) > 0:           
            self.output.orientation = anglesum/len(self.output.pizza)
        else:
            self.output.orientation = None
        self.return_output()

        svr.debug("Pizza", self.debug_frame)
        svr.debug("Original", og_frame)


    def find_corners(self,line1,line2):
        corner1=0
        corner2=0
        corner3=0
        corner4=0
        if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range2 and math.fabs(line1[0][1] - line2[0][1])<self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            corner1 = average_corners(line1[0],line2[0])
            corner2 = line1[1]
            corner3 = line2[1]
            self.corners.append([corner1,corner2,corner3])
        elif math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range2 and math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            corner1 = average_corners(line1[1],line2[1])
            corner2 = line1[0]
            corner3 = line2[0]
            self.corners.append([corner1,corner2,corner3])
        elif math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range2 and math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            corner1 = average_corners(line1[1],line2[0])
            corner2 = line1[0]
            corner3 = line2[1]
            self.corners.append([corner1,corner2,corner3])
        elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range2 and math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            corner1 = average_corners(line1[1],line2[0])
            corner2 = line1[1]
            corner3 = line2[0]
            self.corners.append([corner1,corner2,corner3])

    def check_corners(self,line1,line2):
        corner1=0
        corner2=0
        corner3=0
        corner4=0
        if math.fabs(line1[0][0] - line2[0][0]) < self.max_corner_range2 and math.fabs(line1[0][1] - line2[0][1])<self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            return true
        elif math.fabs(line1[1][0] - line2[1][0]) < self.max_corner_range2 and math.fabs(line1[1][1] - line2[1][1]) < self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            return true
        elif math.fabs(line1[1][0] - line2[0][0]) < self.max_corner_range2 and math.fabs(line1[1][1] - line2[0][1]) < self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            return true
        elif math.fabs(line1[0][0] - line2[1][0]) < self.max_corner_range2 and math.fabs(line1[0][1] - line2[1][1]) < self.max_corner_range2 and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) > self.angle_min and angle_between_lines(line_slope(line1[0],line1[1]),line_slope(line2[0],line2[1])) < self.angle_max:
            return true
        else:
            return false

    def draw_pizza(self):
        print "Number of boxes:", len(self.Boxes)
        for Box in self.Boxes:
            line_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv.Line(self.debug_frame,Box.corner1,Box.corner2, line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame,Box.corner1,Box.corner3, line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame,Box.corner3,Box.corner4, line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame,Box.corner2,Box.corner4, line_color, 10, cv.CV_AA, 0)
            font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, 1)
            cv.PutText(self.debug_frame, str("1"), (int(Box.corner1[0]),int(Box.corner1[1])), font, (0,0,255))
            cv.PutText(self.debug_frame, str("2"), (int(Box.corner2[0]),int(Box.corner2[1])), font, (0,0,255))
            cv.PutText(self.debug_frame, str("3"), (int(Box.corner3[0]),int(Box.corner3[1])), font, (0,0,255))
            cv.PutText(self.debug_frame, str("4"), (int(Box.corner4[0]),int(Box.corner4[1])), font, (0,0,255))
            center = (int(Box.center[0]), int(Box.center[1]))
            
            cv.Circle(self.debug_frame, center, 15, (0,255,0), 2,8,0)


    def sort_bins(self):
        for Bin1 in self.Bins[:]:
            for Bin2 in self.Bins[:]:
                print Bin1.center
                if Bin1 is not Bin2 and Bin1 in self.Bins and Bin2 in self.Bins:
                    if math.fabs(Bin1.center[0]-Bin2.center[0]) < self.max_corner_range2 and math.fabs(Bin1.center[0]-Bin2.center[0]) < self.max_corner_range2:
                        if Bin1.center[0] > Bin2.center[0]:
                            self.Bins.remove(Bin2)
                        else:
                            self.Bins.remove(Bin1)


    def update_bins(self):
        for Bin in self.Bins[:]:
            for corner in self.hough_corners:
                if math.fabs(corner[0]-Bin.corner1[0]) < self.max_corner_range3 and math.fabs(corner[1]-Bin.corner1[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh:
                        Bin.lastseen += 1
                    Bin.corner1 = corner
                    Bin.corner1_updated = self.corner_update_value
                elif math.fabs(corner[0]-Bin.corner2[0]) < self.max_corner_range3 and math.fabs(corner[1]-Bin.corner2[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh:
                        Bin.lastseen += 1
                    Bin.corner2 = corner
                    Bin.corner2_updated = self.corner_update_value
                elif math.fabs(corner[0]-Bin.corner3[0]) < self.max_corner_range3 and math.fabs(corner[1]-Bin.corner3[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh: 
                        Bin.lastseen += 1
                    Bin.corner3 = corner
                    Bin.corner3_updated = self.corner_update_value
                elif math.fabs(corner[0]-Bin.corner3[0]) < self.max_corner_range3 and math.fabs(corner[1]-Bin.corner3[1]) < self.max_corner_range3:
                    if Bin.lastseen < self.lastseen_thresh: 
                        Bin.lastseen += 1
                    Bin.corner4 = corner
                    Bin.corner4_updated = self.corner_update_value
            if Bin.corner1_updated==1 and Bin.corner2_updated==1 and Bin.corner3_updated==1 and Bin.corner4_updated==0:
                Bin.corner4 = (Bin.corner4_locx + Bin.corner1[0],Bin.corner4_locy + Bin.corner1[1])
            if Bin.corner1_updated == 1 and Bin.corner2_updated == 1 and Bin.corner3_updated == 0 and Bin.corner4_updated == 1:
                Bin.corner3 = (Bin.corner3_locx + Bin.corner1[0], Bin.corner3_locy + Bin.corner1[1])
            if Bin.corner1_updated == 1 and Bin.corner2_updated == 0 and Bin.corner3_updated == 1 and Bin.corner4_updated == 1:
                Bin.corner2 = (Bin.corner2_locx + Bin.corner1[0], Bin.corner2_locy + Bin.corner1[1])
            if Bin.corner1_updated == 0 and Bin.corner2_updated == 1 and Bin.corner3_updated == 1 and Bin.corner4_updated == 1:
                Bin.corner1 = (Bin.corner1_locx + Bin.corner2[0], Bin.corner1_locy + Bin.corner2[1])


            if line_distance(Bin.corner1,Bin.corner2) > Bin.distance12 + self.length_trans_thresh or line_distance(Bin.corner1,Bin.corner2) < Bin.distance12 - self.length_trans_thresh and Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"
            elif line_distance(Bin.corner1,Bin.corner3) > Bin.distance13 + self.length_trans_thresh or line_distance(Bin.corner1,Bin.corner3) < Bin.distance13 - self.length_trans_thresh and Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"
            elif line_distance(Bin.corner2,Bin.corner4) > Bin.distance24 + self.length_trans_thresh or line_distance(Bin.corner2,Bin.corner4) < Bin.distance24 - self.length_trans_thresh and Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"
            elif line_distance(Bin.corner3,Bin.corner4) > Bin.distance34 + self.length_trans_thresh or line_distance(Bin.corner3,Bin.corner4) < Bin.distance34 - self.length_trans_thresh and Bin in self.Bins:
                self.Bins.remove(Bin)
                print "length changed"


            elif math.fabs(Bin.angle124 - angle_between_lines(line_slope(Bin.corner1,Bin.corner2),line_slope(Bin.corner2,Bin.corner4))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"
            elif math.fabs(Bin.angle134 - angle_between_lines(line_slope(Bin.corner1,Bin.corner3),line_slope(Bin.corner3,Bin.corner4))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"
            elif math.fabs(Bin.angle312 - angle_between_lines(line_slope(Bin.corner3,Bin.corner1),line_slope(Bin.corner2,Bin.corner1))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"
            elif math.fabs(Bin.angle243 - angle_between_lines(line_slope(Bin.corner2,Bin.corner4),line_slope(Bin.corner3,Bin.corner4))) > self.angle_trans_thresh:
                self.Bins.remove(Bin)
                print "angle changed"



            Bin.lastseen -=2
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
                    if math.fabs(Bin1.center[0]-Bin2.center[0]) < self.center_trans and math.fabs(Bin1.center[1]-Bin2.center[1]) < self.center_trans:
                        if Bin1.id < Bin2.id:
                            Bin1.lastseen += Bin2.lastseen
                            self.Bins.remove(Bin2)
                        else:
                            Bin2.lastseen += Bin1.lastseen
                            self.Bins.remove(Bin1)


    def draw_bins(self):
        for Bin in self.Bins:
            side_a_distance = (line_distance(Bin.corner1,Bin.corner3)+line_distance(Bin.corner2,Bin.corner4))/2
            side_b_distance = (line_distance(Bin.corner1,Bin.corner2)+line_distance(Bin.corner3,Bin.corner4))/2
            side_a_unit_vector = [(Bin.corner3[0]-Bin.corner1[0])/side_a_distance, (Bin.corner3[1]-Bin.corner1[1])/side_a_distance]
            side_b_unit_vector = [(Bin.corner2[0]-Bin.corner1[0])/side_b_distance, (Bin.corner2[1]-Bin.corner1[1])/side_b_distance]

            pt1 = Bin.corner1
            pt2 = [pt1[0]+side_a_unit_vector[0]*side_a_distance, pt1[1]+side_a_unit_vector[1]*side_a_distance]
            pt3 = [pt1[0]+side_b_unit_vector[0]*side_b_distance, pt1[1]+side_b_unit_vector[1]*side_b_distance]
            pt4 = [pt3[0]+side_a_unit_vector[0]*side_a_distance, pt3[1]+side_a_unit_vector[1]*side_a_distance]

            #Bin.corner1 = pt1
            #Bin.corner2 = pt2
            #Bin.corner3 = pt3
            #Bin.corner4 = pt4


            line_color = (0,0,255) 
            print pt2
            cv.Line(self.debug_frame,pt1,(int(pt2[0]),int(pt2[1])), line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame,pt1,(int(pt3[0]),int(pt3[1])), line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame,(int(pt4[0]),int(pt4[1])),(int(pt2[0]),int(pt2[1])), line_color, 10, cv.CV_AA, 0)
            cv.Line(self.debug_frame,(int(pt4[0]),int(pt4[1])),(int(pt3[0]),int(pt3[1])), line_color, 10, cv.CV_AA, 0)




    def sort_corners(self):
        self.final_corners = []
        print len(self.hough_corners)
        
        for corner1 in self.hough_corners[:]:
            for corner2 in self.hough_corners[:]:
                if corner1 is not corner2 and corner1 in self.hough_corners and corner2 in self.hough_corners and corner1[0]-corner2[0] != 0 and corner1[1]-corner2[1] != 0:
                    if math.fabs(corner1[0]-corner2[0]) < self.corner_sort_thresh and math.fabs(corner1[1]-corner2[1]) < self.corner_sort_thresh:
                        self.final_corners.append(corner1)
                        #self.hough_corners.remove(corner2)
                        #self.hough_corners.remove(corner1)
                        print "appended"
                        break


        
        return self.final_corners


















