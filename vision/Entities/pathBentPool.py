import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "pathBent"
obj = visObjects[visObj]
keys = obj([False, 0, 0, 0, 0, 0, 0]).keys
SCREEN_AREA = 200000

"""
Finds bent path in image where path is bends 45 degrees midway through.
"""
def ProcessFrame(frame):
  import time
  #time.sleep(.1)
  out = obj([False, 0, 0, 0, 0, 0, 0])
  
  #frame = norm(frame)
  frameOut = np.copy(frame)
  m = cv2.mean(frame)
  red = dist(frame, [m[0],  m[1], 150])
  red = blur = cv2.blur(red,(5,5))
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  # multiplier of                                     std dev init was   2.65
  ret, thresh = cv2.threshold(red, 145, 255, cv2.THRESH_BINARY_INV)
  debugFrame("threshOg", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contour_img = np.copy(frame)
  real_contours = []
  for cnt in contours:
      area = cv2.contourArea(cnt)
      # this is the area of the screen
      # often, the whole sceen is detected as a contour :/
      # here, we remove it
      if area < SCREEN_AREA:
        cv2.drawContours(contour_img, [cnt], 0, (0,255,0), 3)
        real_contours.append(cnt)
  debugFrame("contours", contour_img)
  contours = real_contours

  mean, std = cv2.meanStdDev(frame)
  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  r = cv2.GaussianBlur(r, (9, 9), 0)
  
  
  for i in range(len(contours)):
      epsilon = 0.075*cv2.arcLength(contours[i],True)
      approx = cv2.approxPolyDP(contours[i],epsilon,True)
      #check if shape triangle
      cv2.fillConvexPoly(frameOut, approx, (255,0,0))
      """"if the approximated contour is a triangle"""
      if len(approx) == 3:
        
        """Finding the point opposite of the hypotenuse"""
        pts = []
        for ptWrapper in approx:
            pts.append(ptWrapper[0])
        #find hypotenuse
        maxLen = 0
        maxIdx = 0
        for j in range(3):
            #print j
            p1 = pts[j]
            #print (j+1) %3
            p2 = pts[(j + 1)%3]
            sideLen = math.sqrt( (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 )
            if sideLen > maxLen:
                maxLen = sideLen
                maxIdx = j
        p1 = pts[maxIdx]
        p2 = pts[(maxIdx + 1) % 3]
        center = pts[(maxIdx + 2) % 3]
        #cv2.circle(frameOut,(center[0], center[1]) , 5, color = (0,0,0), thickness = -1)
        v1 = [p1[0] - center[0], p1[1] - center[1]]
        v2 = [p2[0] - center[0], p2[1] - center[1]]
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        """Finding magnitude of 2 shorter sides and the angle opposite of the hypotenuse"""
        mag1 = math.sqrt( (v1[0]) ** 2 + (v1[1]) ** 2 )
        mag2 = math.sqrt( (v2[0]) ** 2 + (v2[1]) ** 2 )
        angle = math.acos(dot/(mag1 * mag2)) * 180.0 / math.pi
        #print "ANGLE: ", angle
        #print "MAGNITUDES: ", mag1, " ", mag2
        """
        checks that the biggest angle of the triangle is roughly 130 degrees and that the sides are similar sizes
        130 degrees corresponds to the 45 degree bend
        """
        MAX_LEN_DIF = 20
        MIN_LEN = 60
        TARGET_ANGLE = 130

        angle_accurate = abs(TARGET_ANGLE - abs(angle)) < 15 
        similar_lengths =  abs(mag1 - mag2) < MAX_LEN_DIF
        min_length = mag1 > MIN_LEN
        print "angle_accurate", angle_accurate, abs(TARGET_ANGLE - abs(angle))
        print "similar_lengths", similar_lengths
        print "min_length", min_length
        
        if angle_accurate and similar_lengths and min_length:
            out = obj([True, int(center[0]), int(center[1]), int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])])
            frameOut = out.draw(frameOut)

  debugFrame("out", frameOut)
  return out
def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
