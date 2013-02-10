

from __future__ import division
import math

import cv

import svr

from base import VisionEntity
import libvision
from sw3.util import circular_average, circular_range

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

def line_group_accept_test(line_group, line, max_range):
    '''
    Returns True if the line should be let into the line group.

    First calculates what the range of rho values would be if the line were
    added.  If the range is greater than max_range the line is rejected and
    False is returned.
    '''

    theta = line[1]
    

#    if circular_range(

    

#    min_rho = line[0]
#    max_rho = line[0]
#    for l in line_group:
#        if l[0] > max_rho:
#            max_rho = l[0]
#        if l[0] < min_rho:
#            min_rho = l[0]
#    return max_rho - min_rho < max_range

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
		
	
	'''
	for corner1 in corners:
		for corner2 in corners:
#			if (math.sqrt(int(corner1[0])**2 + int(corner1[1]**2))-(math.sqrt(int(corner2[0])**2+int(corner2[1]**2)))) > self.min_line_size and (math.sqrt(int(corner1[0])**2 + int(corner1[1]**2))-(math.sqrt(int(corner2[0])**2+int(corner2[1]**2)))) < self.max_line_size:
			if math.sqrt((corner1[0]-corner2[0])**2 + (corner1[1]-corner2[1])**2) > self.min_line_size and math.sqrt((corner1[0]-corner2[0])**2 + (corner1[1]-corner2[1])**2) < self.max_line_size:
				pt1 = (cv.Round(corner1[0]), cv.Round(corner1[1]))
				pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
				cv.Line(debug_frame, pt1, pt2, corner_color, 1, cv.CV_AA, 0)
	'''

	'''
	for corner1 in corners:
		for corner2 in corners:
			for corner3 in corners:
				for corner4 in corners:
					if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0]:
						if math.fabs(line_slope(corner1, corner2) - line_slope(corner3,corner4)) < .05 and math.fabs(line_slope(corner1,corner3) - line_slope(corner2,corner4)) < .05 and angle_between_lines(line_slope(corner1, corner2),line_slope(corner3,corner4) )> -290 and angle_between_lines(line_slope(corner1, corner2),line_slope(corner3,corner4)) < 3600:
							pt1 = (cv.Round(corner1[0]), cv.Round(corner1[1]))
							pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
							cv.Line(debug_frame, pt1, pt2, corner_color, 1, cv.CV_AA, 0)
							pt3 = (cv.Round(corner3[0]), cv.Round(corner3[1]))
							pt4 = (cv.Round(corner4[0]), cv.Round(corner4[1]))
							cv.Line(debug_frame, pt3, pt4, corner_color, 1, cv.CV_AA, 0)
	
	'''

#Find Centers

	for corner1 in corners:
		for corner2 in corners:
			for corner3 in corners:
				for corner4 in corners:
					if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0] and corner4[1] != corner3[1] and corner4[1] != corner2[1] and corner4[1] != corner1[1] and corner3[1] != corner2[1] and corner3[1] != corner1[1] and corner2[1] != corner1[1] and corner2[0]>=corner3[0] and corner1[1]>=corner4[1] and corner2[0]>=corner1[0]:
						if math.fabs(line_distance(corner1,corner3) - line_distance(corner2,corner4)) < self.size_threshold and math.fabs(line_distance(corner1,corner2) - line_distance(corner3,corner4)) < self.size_threshold and math.fabs(line_distance(corner1,corner3)/line_distance(corner1,corner2)) < self.ratio_threshold or math.fabs(line_distance(corner1,corner2)/line_distance(corner1,corner3)) < self.ratio_threshold:
							if math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4) ))> self.angle_min and math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4))) < self.angle_max:
								if math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4) ))> self.angle_min2 and math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4))) < self.angle_max2:
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


	'''
	for corner1 in corners:
		for corner2 in corners:
			for corner3 in corners:
				for corner4 in corners:
					if (corner1!= corner2 and corner1!= corner4 and  corner1!= corner3) and (corner2!=  corner3 and corner2!= corner4) and corner3!=corner4 and angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4) ) != None and angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4)) != None and angle_between_lines(line_slope(corner2, corner4),line_slope(corner4,corner3)) != None:
						if math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4) ))> self.angle_min and math.fabs(angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4))) < self.angle_max and math.fabs(line_slope(corner1,corner2))-math.fabs(line_slope(corner2,corner4))> 1.5 and math.fabs(line_distance(corner1, corner2)-line_distance(corner4,corner3))<1 and math.fabs(line_distance(corner1, corner2)-line_distance(corner3,corner4))<1:
#							if math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4) ))> self.angle_min2 and math.fabs(angle_between_lines(line_slope(corner1, corner3),line_slope(corner3,corner4))) < self.angle_max2:
							print angle_between_lines(line_slope(corner1, corner2),line_slope(corner2,corner4) )
							line_color = (corner1[1]/2,corner2[1]/2,corner4[1]/2)
							pt1 = (cv.Round(corner1[0]), cv.Round(corner1[1]))
							pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
							cv.Line(debug_frame, pt1, pt2, line_color, 1, cv.CV_AA, 0)
							pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
							pt4 = (cv.Round(corner4[0]), cv.Round(corner4[1]))
							pt3 = (cv.Round(corner3[0]),cv.Round(corner3[1]))
							cv.Line(debug_frame, pt2, pt4, line_color, 1, cv.CV_AA, 0)
							cv.Line(debug_frame, pt3,pt4, line_color, 1, cv.CV_AA, 0)
							cv.Line(debug_frame, pt1,pt3, line_color, 1, cv.CV_AA, 0)
							cv.Circle(debug_frame, (int(midpointx(corner1,corner4)),int(midpointy(corner1,corner4))), 15, line_color, 2,8,0)
						
	'''

	

	
	'''
	for corner1 in corners:
		for corner2 in corners:
			for corner3 in corners:
				for corner4 in corners:
					if corner4[0] != corner3[0] and corner4[0] != corner2[0] and corner4[0] != corner1[0] and corner3[0] != corner2[0] and corner3[0] != corner1[0] and corner2[0] != corner1[0] and corner4[1] != corner3[1] and corner4[1] != corner2[1] and corner4[1] != corner1[1] and corner3[1] != corner2[1] and corner3[1] != corner1[1] and corner2[1] != corner1[1]:
						if midpoint(corner1,corner2) != None and midpoint(corner3,corner4) != None:
							if math.fabs(midpoint(corner1,corner2)[0]-midpoint(corner3,corner4)[0]) < 2 and math.fabs(midpoint(corner1,corner2)[1]-midpoint(corner3,corner4)[1]) < 2:
								center_color = (0,255,255)
                						cv.Circle(debug_frame, (int(midpoint(corner1,corner2)[0]),int(midpoint(corner1,corner2)[1])), 20, center_color, 2,8,0)
	
								#pt1 = (cv.Round(corner1[0]), cv.Round(corner1[1]))
								#pt2 = (cv.Round(corner2[0]), cv.Round(corner2[1]))
								#cv.Line(debug_frame, pt1, pt2, corner_color, 1, cv.CV_AA, 0)
								#pt3 = (cv.Round(corner3[0]), cv.Round(corner3[1]))
								#pt4 = (cv.Round(corner4[0]), cv.Round(corner4[1]))
								#cv.Line(debug_frame, pt3, pt4, corner_color, 1, cv.CV_AA, 0)
	
	'''
	'''
	for corner1 in corners:
		for corner2 in corners:
			for corner3 in corners:
				for corner4 in corners:
					for corner5 in corners:
						for corner6 in corners:
							for corner7 in corners:
								for corner8 in corners:
									if (corner1!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8) and (corner2!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8) and (corner3!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8) and (corner4!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8) and (corner5!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8) and (corner6!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8) and (corner7!= corner2 or corner3 or corner4 or corner5 or corner6 or corner7 or corner8):
										if midpoint(corner1,corner2) != None and midpoint(corner3,corner4) != None:
											if math.fabs(midpoint(corner1,corner2)[0]-midpoint(corner3,corner4)[0]) < 2 and math.fabs(midpoint(corner1,corner2)[1]-midpoint(corner3,corner4)[1]) < 2:
												center_color = (0,255,255)
                										cv.Circle(debug_frame, (int(midpoint(corner1,corner2)[0]),int(midpoint(corner1,corner2)[1])), 20, center_color, 2,8,0)
	



	'''












	
	#libvision.misc.draw_lines(debug_frame, corner)
       # cv.CvtColor(color_filtered,debug_frame, cv.CV_GRAY2RGB)
	svr.debug("Bins", debug_frame)

