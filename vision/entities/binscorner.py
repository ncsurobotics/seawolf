

from __future__ import division
import math

import cv

import svr

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range


MAX_X_TRANS = 30
MAX_Y_TRANS = 30
#how many consequtive frames a candidate is allowed to go missing
CANDIDATE_BIN_TIMEOUT = 3
#required seen threshold to accept a buoy
CANDIDATE_SEEN_THRESH = 2

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




class Bin(object):
    '''an imaged bin'''
    def __init__(self):

        #Identification Number
        self.id = 0

        self.midx = None
        self.midy = None

        self.small = None

        self.large = None

	self.color = None

        #Frames since last sighting
        self.last_seen = 0

        #Keeps track of how often we have seen this buoy
        self.seen_count = 0

        #Color used in debug windows
        self.debug_color = None


class BinscornerEntity(VisionEntity):
    def new_bins(self,corner1,corner2,corner3,corner4):
       	'''intialize a new bin'''
	new_bins = Bin()
	new_bins.midx = rect_midpointx(corner1,corner2, corner3, corner4)
	new_bins.midy = rect_midpointy(corner1,corner2, corner3, corner4)
	new_bins.corner1 = corner1
	new_bins.corner2 = corner2
	new_bins.corner3 = corner3
	new_bins.corner4 = corner4
	if math.fabs(line_distance(corner1, corner3))<math.fabs(line_distance(corner1,corner2)):
		new_bins.angle = -angle_between_lines(line_slope(corner1,corner3), 0)
		new_bins.small = math.fabs(line_distance(corner1, corner3))
		new_bins.large = math.fabs(line_distance(corner1, corner2))
	else:
		new_bins.angle = angle_between_lines(line_slope(corner1,corner2), 0)
		new_bins.small = math.fabs(line_distance(corner1, corner2))
		new_bins.large = math.fabs(line_distance(corner1, corner3))
	        new_bins.last_seen = 0
	        new_bins.seen_count = 0
        return new_bins



    def init(self):
	
	
#	self.vertical_threshold = 15*math.pi/180  # How close to vertical lines must be
#        self.horizontal_threshold = 0.2  # How close to horizontal lines must be
        self.hough_threshold = 180
        self.adaptive_thresh_blocksize = 19
        self.adaptive_thresh = 21

        self.max_range = 100

	self.max_corners = 20
	self.quality_level = .7
	self.min_distance = 40
	self.good_features_blocksize = 24
	
        self.min_line_size = 120
	self.max_line_size = 200

	self.angle_min = math.pi/2-.1
	self.angle_max = math.pi/2+.1

	self.angle_min2 = math.pi/2-.1
	self.angle_max2 = math.pi/2+.1

	self.size_threshold = 40
	self.ratio_threshold = .5
	self.length_threshold = 200


	self.candidates = []
	self.confirmed = []




    def process_frame(self, frame):
	debug_frame = cv.CreateImage(cv.GetSize(frame),8,3)
	cv.Copy(frame, debug_frame)


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
   
        cv.CvtColor(binary,debug_frame, cv.CV_GRAY2RGB)
	
	temp1 = cv.CreateImage(cv.GetSize(frame), 8, 1)
	temp2 = cv.CreateImage(cv.GetSize(frame), 8, 1)
	
	corners = cv.GoodFeaturesToTrack(binary, temp1, temp2, self.max_corners, self.quality_level, self.min_distance, None, self.good_features_blocksize, 0, 0.4) 

        for corner in corners:
                corner_color = (0,0,255)
		text_color = (0, 255, 0)
		font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, .6, .6, 0, 1, 1)
		cv.Circle(debug_frame, (int(corner[0]),int(corner[1])), 15, corner_color, 2,8,0)
		cv.PutText(debug_frame, str(corner), (int(corner[0]),int(corner[1])), font, text_color)
		#print corner
#		cv.PutText(debug_frame, corner, (int(corner[0]),int(corner[1]), CV_FONT_HERSHEY_SIMPLEX, (0,0,255))
		


#Find Centers

	for corner1 in corners:
		for corner2 in corners:
			for corner3 in corners:
				for corner4 in corners:
					if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0] and corner4[1] != corner3[1] and corner4[1] != corner2[1] and corner4[1] != corner1[1] and corner3[1] != corner2[1] and corner3[1] != corner1[1] and corner2[1] != corner1[1] and corner2[0]>=corner3[0] and corner1[1]>=corner4[1] and corner2[0]>=corner1[0]:
						if math.fabs(line_distance(corner1,corner3) - line_distance(corner2,corner4)) < self.size_threshold and math.fabs(line_distance(corner1,corner2) - line_distance(corner3,corner4)) < self.size_threshold and math.fabs(line_distance(corner1,corner3)/line_distance(corner1,corner2)) < self.ratio_threshold or math.fabs(line_distance(corner1,corner2)/line_distance(corner1,corner3)) < self.ratio_threshold:
							if math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4) ))> self.angle_min and math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4))) < self.angle_max:
								if math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4) ))> self.angle_min2 and math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4))) < self.angle_max2:
									existing = 0
									for bins in self.candidates:
										if bins.midx == rect_midpointx(corner1,corner2, corner3, corner4) and bins.midy == rect_midpointy(corner1,corner2, corner3, corner4) :
											existing = 1
									if existing == 0:
										bins_found = self.new_bins(corner1,corner2,corner3,corner4)
										self.candidates.append(bins_found)
										self.sort_bins()
										

										line_color = (corner1[1]/2,corner2[1]/2,corner4[1]/2)
										cv.Circle(debug_frame, (int(rect_midpointx(corner1,corner2, corner3, corner4)),int(rect_midpointy(corner1,corner2, corner3, corner4))), 15, line_color, 2,8,0)
										
										pt1 = (cv.Round(corner1[0]), cv.Round(corner1[1]))
										pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
										cv.Line(debug_frame, pt1, pt2, line_color, 1, cv.CV_AA, 0)
										pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
										pt4 = (cv.Round(corner4[0]), cv.Round(corner4[1]))
										pt3 = (cv.Round(corner3[0]),cv.Round(corner3[1]))
										cv.Line(debug_frame, pt2, pt4, line_color, 1, cv.CV_AA, 0)
										cv.Line(debug_frame, pt3,pt4, line_color, 1, cv.CV_AA, 0)	
										cv.Line(debug_frame, pt1,pt3, line_color, 1, cv.CV_AA, 0)
										if math.fabs(line_distance(corner1, corner3))<math.fabs(line_distance(corner1,corner2)):
											angle = -angle_between_lines(line_slope(corner1,corner3), 0)
											print int((angle/math.pi)*180)
											cv.PutText(debug_frame, str(int((angle/math.pi)*180)), (int(rect_midpointx(corner1,corner2, corner3, corner4)),int(rect_midpointy(corner1,corner2, corner3, corner4))), font, text_color)

											print "found"
	svr.debug("Bins", debug_frame)

    def sort_bins(self):
        
        	#perform upkeep on confirmed buoys
       		for confirmed in self.confirmed:

        	    #increment how long ago we saw this buoy.  If it gets
        	    # matched, this number will be reset
        	    confirmed.last_seen += 1
        	    confirmed.seen_count -= 1

        	    #check if this buoy can be matched to a new buoy
        	    self.match_bins(confirmed)
	
        	    #if this buoy hasn't been seen recently, mark it as lost
        	    if confirmed.last_seen > CONFIRMED_BIN_TIMEOUT:
        	        self.lost.append(confirmed)
        	        self.confirmed.remove(confirmed)
	
        	#perform upkeep on candidates
        	for candidate in self.candidates:
	
        	    #increment how long ago we saw this buoy.  If it gets
        	    # matched, this number will be reset
        	    candidate.last_seen += 1
        	    candidate.seen_count -= 1
	
        	    #check if this buoy can be matched to a new buoy
        	    self.match_bins(candidate)
	
        	    #if this buoy hasn't been seen recently, stop tracking
        	    if candidate.last_seen > CANDIDATE_BIN_TIMEOUT:
        	        self.candidates.remove(candidate)
	
        	    #if seen count has grown large enough, accept this buoy
        	    if candidate.seen_count >= CANDIDATE_SEEN_THRESH:
        	        if self.debug:
        	            #assign this buoy a debug color
        	            r = int(cv.RandReal(self.rng)*255)
        	            g = int(cv.RandReal(self.rng)*255)
        	            b = int(cv.RandReal(self.rng)*255)
        	            candidate.debug_color = cv.RGB(r,g,b)
        	        candidate.id = self.bin_count
        	        self.bin_count += 1
        	        self.confirmed.append(candidate)
        	        self.candidates.remove(candidate)
	
        	#perform upkeep on lost buoys
        	#TODO use lost buoys for anything, likely will depend on color
	
        	

    def match_bins(self, target):
        	'''matches buoys in the self.new list to a target buoy'''
        
	        #check if any of the new buoys match this confirmed buoy
        	for Bin in self.confirmed:
        	    if abs(Bin.midx - target.midx) < MAX_X_TRANS:
        	        continue
        	    if abs(Bin.midy - target.midy) < MAX_Y_TRANS:
        	        continue
        	    
	
        	    #this is a match, update confirmed buoy
        	    Bin.color = target.color
        	    Bin.midx = target.midx
        	    Bin.midy = target.midy
        	    
        	    Bin.last_seen = 0
        	    Bin.seen_count += 2 #effectually increase by 1 if seen, -1 if not seen
        	    #TODO handle color
	
        	    #remove this new buoy that has been matched
		    self.confirmed.remove(target)
		
        	    break		






	
	#libvision.misc.draw_lines(debug_frame, corner)
       # cv.CvtColor(color_filtered,debug_frame, cv.CV_GRAY2RGB)
    

