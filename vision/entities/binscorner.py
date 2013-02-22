

from __future__ import division
import math
#import collections import Counter

import cv

import svr

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range





class Bin(object):
    bin_id = 0
    '''an imaged bin'''
    def __init__(self, corner_a,corner_b,corner_c, corner_d):
	rng = cv.RNG()
	self.midx = rect_midpointx(corner_a,corner_b,corner_c,corner_d)
	self.midy = rect_midpointy(corner_a,corner_b,corner_c,corner_d)
	self.corner1 = corner_a
	self.corner2 = corner_b
	self.corner3 = corner_c
	self.corner4 = corner_d
	if line_distance(corner_a,corner_c)< line_distance(corner_a, corner_b):
		self.angle = -angle_between_lines(line_slope(corner_a,corner_c), 0)
	else:
		self.angle = -angle_between_lines(line_slope(corner_a,corner_b), 0)
	self.ID = 0
	self.last_seen = 2
	self.seencount = 1
	r = int(cv.RandReal(rng)*255)
        g = int(cv.RandReal(rng)*255)
        b = int(cv.RandReal(rng)*255)
        self.debug_color = cv.RGB(r,g,b)


class Binscorner(object):
    def __init__(self,type,center,angle,area):
        #ID number used when tracking bins
        self.id = 0

        #decisive type of letter in the bin
        self.type = type

        #center of bin
        self.center = center

        #direction of the bin
        self.angle = angle

        #area of the bin
        self.area = area

        #tracks timeout for bin
        self.timeout = 10

        #tracks our type decisions
        self.type_counts = [0,0,0,0,0]


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
		return 0

def midpoint(corner_a, corner_b):
	midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
	midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
	#mid = (midpoint_x, midpoint_y)
	return [midpoint_x, midpoint_y]

def midpointx(corner_a, corner_b):
	midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
	#midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
	#mid = (midpoint_x, midpoint_y)
	return midpoint_x

def midpointy(corner_a, corner_b):
	#midpoint_x = (corner_b[0] - corner_a[0])/2+corner_a[0]
	midpoint_y = (corner_b[1] - corner_a[1])/2+corner_a[1]
	#mid = (midpoint_x, midpoint_y)
	return midpoint_y

def rect_midpointx(corner_a,corner_b,corner_c,corner_d):
	midpoint_x = (corner_a[0]+corner_b[0]+corner_c[0]+corner_d[0])/4
	return midpoint_x

def rect_midpointy(corner_a,corner_b,corner_c,corner_d):
	midpoint_y = (corner_a[1]+corner_b[1]+corner_c[1]+corner_d[1])/4
	return midpoint_y


		



class BinscornerEntity(VisionEntity):
    
   

    def init(self):

        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 21

        self.max_range = 100

	self.max_corners = 20
	self.quality_level = .7
	self.min_distance = 40
	self.good_features_blocksize = 24
	

	self.angle_min = math.pi/2-.15
	self.angle_max = math.pi/2+.15
	self.angle_min2 = math.pi/2-.15
	self.angle_max2 = math.pi/2+.15

	self.size_threshold = 40
	self.ratio_threshold = .5
	self.length_threshold = 200

	self.MaxTrans = 30
	self.MaxLostTrans = 50

	self.last_seen_thresh = 0
	self.min_seencount = 5
	self.lost_last_seen_thresh = 0

	self.perimeter_threshold = 0.08

	self.lost_clock =100

	self.corners = []
	self.candidates = []
        self.confirmed  = []
	self.new = []
	self.angles = []
	self.lost = []

	


    def process_frame(self, frame):
	self.debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
	cv.Copy(frame, self.debug_frame)


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
		cv.PutText(self.debug_frame, str(corner), (int(corner[0]),int(corner[1])), font, text_color)
		
	

#Find Candidates

	for corner1 in self.corners:
		for corner2 in self.corners:
			for corner3 in self.corners:
				for corner4 in self.corners:
					#Checks that corners are not the same and are in the proper orientation
					if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0] and corner4[1] != corner3[1] and corner4[1] != corner2[1] and corner4[1] != corner1[1] and corner3[1] != corner2[1] and corner3[1] != corner1[1] and corner2[1] != corner1[1] and corner2[0]>=corner3[0] and corner1[1]>=corner4[1] and corner2[0]>=corner1[0]:
						#Checks that the ratios are correct
						if math.fabs(line_distance(corner1,corner3) - line_distance(corner2,corner4)) < self.size_threshold and math.fabs(line_distance(corner1,corner2) - line_distance(corner3,corner4)) < self.size_threshold and math.fabs(line_distance(corner1,corner3)/line_distance(corner1,corner2)) < self.ratio_threshold or math.fabs(line_distance(corner1,corner2)/line_distance(corner1,corner3)) < self.ratio_threshold:
							#Checks that angles are roughly 90 degrees
							if math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4) ))> self.angle_min and math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4))) < self.angle_max:
								if math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4) ))> self.angle_min2 and math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4))) < self.angle_max2:
									found = 0
									new_bin = Bin(corner1,corner2,corner3,corner4)
									self.match_bins(new_bin)
	self.sort_bins()								
	svr.debug("Bins", self.debug_frame)
	#raw_input()
	        
	#Output bins
	self.output.bins = self.confirmed
        for bins in self.output.bins:
            bins.theta = (bins.midx - frame.width/2) * 37 / (frame.width/2);
            bins.phi = -1 * (bins.midy - frame.height/2) * 36 / (frame.height/2);
	    bins.orientation = bins.angle
        self.return_output()

    def match_bins(self, target):
		existing = 0
		#update if lost bin
		for lost in self.lost:
			if math.fabs(target.midx-lost.midx) < self.MaxTrans and math.fabs(target.midy-lost.midy) < self.MaxTrans and target.ID != lost.ID:
				lost.midx = target.midx
				lost.midy = target.midy
				lost.corner1 = target.corner1
				lost.corner2 = target.corner2
				lost.corner3 = target.corner3
				lost.corner4 = target.corner4
				lost.angle = target.angle
				lost.last_seen = 15
				lost.seencount +=1
				existing = 1
				self.confirmed.append(lost)
		#update if candidate
		for candidate in self.candidates:
			if math.fabs(target.midx-candidate.midx) < self.MaxTrans and math.fabs(target.midy-candidate.midy) < self.MaxTrans and target.ID != candidate.ID:
				candidate.midx = target.midx
				candidate.midy = target.midy
				candidate.corner1 = target.corner1
				candidate.corner2 = target.corner2
				candidate.corner3 = target.corner3
				candidate.corner4 = target.corner4
				candidate.angle = target.angle
				if candidate.last_seen < 30:
					candidate.last_seen +=3
				candidate.seencount +=1
				existing = 1
		#update if confirmed
		for confirmed in self.confirmed:
			for confirmed2 in self.confirmed:
				if confirmed.midx == confirmed2.midx and confirmed.midy == confirmed2.midy and confirmed.ID != confirmed2.ID:
					if confirmed.ID < confirmed2.ID:
						self.confirmed.remove(confirmed2)


			if math.fabs(target.midx-confirmed.midx) < self.MaxTrans and math.fabs(target.midy-confirmed.midy) < self.MaxTrans and target.ID != confirmed.ID:
				confirmed.midx = target.midx
				confirmed.midy = target.midy
				confirmed.corner1 = target.corner1
				confirmed.corner2 = target.corner2
				confirmed.corner3 = target.corner3
				confirmed.corner4 = target.corner4
				confirmed.angle = target.angle
				if confirmed.last_seen < 30:
					confirmed.last_seen +=3
				confirmed.seencount +=1
				existing = 1
		if existing == 0:
			print "found candidate"
			target.ID = Bin.bin_id
			Bin.bin_id += 1
			self.candidates.append(target)




    def sort_bins(self):
		for corner in self.corners:
			for candidate in self.candidates:
				if math.fabs((candidate.corner1[0] - corner[0])) < self.MaxTrans and math.fabs((candidate.corner1[1] - corner[1])) < self.MaxTrans or math.fabs((candidate.corner2[0] - corner[0])) < self.MaxTrans and math.fabs((candidate.corner2[1] - corner[1])) < self.MaxTrans or math.fabs((candidate.corner3[0] - corner[0])) < self.MaxTrans and math.fabs((candidate.corner3[1] - corner[1])) < self.MaxTrans or math.fabs((candidate.corner4[0] - corner[0])) < self.MaxTrans and math.fabs((candidate.corner4[1] - corner[1])) < self.MaxTrans :
					candidate.last_seen += 1
			
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
			if 0 < line_distance(confirmed.corner1,confirmed.corner3)*2 + line_distance(confirmed.corner1,confirmed.corner2)*2 < self.min_perimeter: 	
				self.min_perimeter = line_distance(confirmed.corner1,confirmed.corner3)*2 + line_distance(confirmed.corner1,confirmed.corner2)*2
			print confirmed.angle/math.pi*180			
			#self.angles.append((cv.Round(confirmed.angle/math.pi)*180/1)*1)
			self.angles.append(cv.Round(confirmed.angle/math.pi*180/10)*10)
		for confirmed in self.confirmed:
			data = []
			if math.fabs(line_distance(confirmed.corner1,confirmed.corner3)*2 + line_distance(confirmed.corner1,confirmed.corner2)*2 - self.min_perimeter)>self.min_perimeter*self.perimeter_threshold:
				print "perimeter error"	
				self.candidates.append(confirmed)
				self.confirmed.remove(confirmed)
				continue
#			from collections import Counter
#			data = Counter(self.angles)
#			print data.most_common(1)[0][0]
#			if cv.Round(confirmed.angle/math.pi*180/10)*10 != data.most_common(1)[0][0] and math.fabs(line_distance(confirmed.corner1,confirmed.corner3)*2 + line_distance(confirmed.corner1,confirmed.corner2)*2 - self.min_perimeter)>self.min_perimeter*0.05:
#				print "angle error"
#				continue
			
			confirmed.last_seen -= 1
			if confirmed.last_seen < self.last_seen_thresh:
				self.confirmed.remove(confirmed) 
				confirmed.last_seen = self.lost_clock
#				self.lost.append(confirmed)
				print "lost confirmed"
				continue
			#draw bins
			line_color = (confirmed.corner1[1]/2,confirmed.corner2[1]/2,confirmed.corner4[1]/2)
			cv.Circle(self.debug_frame, (int(confirmed.midx),int(confirmed.midy)), 15, line_color, 2,8,0)
			pt1 = (cv.Round(confirmed.corner1[0]), cv.Round(confirmed.corner1[1]))
			pt2 = (cv.Round(confirmed.corner2[0]), cv.Round(confirmed.corner2[1]))
			cv.Line(self.debug_frame, pt1, pt2, line_color, 1, cv.CV_AA, 0)
			pt2 = (cv.Round(confirmed.corner2[0]), cv.Round(confirmed.corner2[1]))
			pt4 = (cv.Round(confirmed.corner4[0]), cv.Round(confirmed.corner4[1]))
			pt3 = (cv.Round(confirmed.corner3[0]),cv.Round(confirmed.corner3[1]))
			cv.Line(self.debug_frame, pt2, pt4, line_color, 1, cv.CV_AA, 0)
			cv.Line(self.debug_frame, pt3,pt4, line_color, 1, cv.CV_AA, 0)
			cv.Line(self.debug_frame, pt1,pt3, line_color, 1, cv.CV_AA, 0)
			font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, .6, .6, 0, 1, 1)
			text_color = (0, 255, 0)
			cv.PutText(self.debug_frame, str(confirmed.ID), (int(confirmed.midx),int(confirmed.midy)), font, confirmed.debug_color)
#		for lost in self.lost:
#			lost.last_seen -= 1
#			if lost.last_seen < self.lost_last_seen_thresh:
#				self.lost.remove(lost)
#				print "lost lost"
	
	






	
	#libvision.misc.draw_lines(self.debug_frame, corner)
       # cv.CvtColor(color_filtered,self.debug_frame, cv.CV_GRAY2RGB)
	


