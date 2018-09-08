import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "pathBent"
obj = visObjects[visObj]
keys = obj([False, 0, 0, 0, 0, 0, 0]).keys

"""
Finds bent path in image where path is bends 45 degrees midway through.
"""
def ProcessFrame(frame):
  import time
  #time.sleep(.1)
  out = obj([False, 0, 0, 0, 0, 0, 0])
  frameOut = np.copy(frame)
  frame = norm(frame)
  m = cv2.mean(frame)
  red = dist(frame, [m[0],  m[1], 255])
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  ret, thresh = cv2.threshold(red, np.mean(red) - max(np.std(red), 10) * 2.65, 255, cv2.THRESH_BINARY_INV)
  debugFrame("threshOg", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  mean, std = cv2.meanStdDev(frame)
  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  r = cv2.GaussianBlur(r, (9, 9), 0)
  
  for i in range(len(contours)):
      epsilon = 0.045*cv2.arcLength(contours[i],True)
      approx = cv2.approxPolyDP(contours[i],epsilon,True)
      #check if shape triangle
      cv2.fillConvexPoly(frameOut, approx, (255,0,0))
      foundThreeOrFour = False
      """"if the approximated contour is a triangle"""
      if len(approx) == 3:
        #foundThreeOrFour = True
        
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
        
      elif len(approx) == 4:
        foundThreeOrFour = True
        """Figure out closest and furthest points"""
        pts = []
        for ptWrapper in approx:
            pts.append(ptWrapper[0])
        maxDist = 0
        end1 = 0
        end2 = 0
        for i in range(0,len(pts)):
            for j in range(i,len(pts)):
                ptdist = math.sqrt( (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2 )
                if(ptdist >= maxDist):
                    maxDist = ptdist
                    end1 = i
                    end2 = j
        p1, p2 = pts[end1], pts[end2]
        centerPts = []
        for i in range(len(pts)):
            if i != end1 and i != end2:
                centerPts.append(pts[i])
        center = ( (centerPts[0][0] + centerPts[1][0]) / 2, (centerPts[0][1] + centerPts[1][1]) / 2 )
        #out = obj([True, int(center[0]), int(center[1]), int(endPts[0][0]), int(endPts[0][1]), int(endPts[1][0]), int(endPts[1][1])])
        #frameOut = out.draw(frameOut)
      if foundThreeOrFour:
        v1 = [p1[0] - center[0], p1[1] - center[1]]
        v2 = [p2[0] - center[0], p2[1] - center[1]]
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        """Finding magnitude of 2 shorter sides and the angle opposite of the hypotenuse"""
        mag1 = math.sqrt( (v1[0]) ** 2 + (v1[1]) ** 2 )
        mag2 = math.sqrt( (v2[0]) ** 2 + (v2[1]) ** 2 )
        #may increment mags and arg inside acos to be not 0 or in acos domain
        if mag1 == 0:
            mag1 += .001
        if mag2 == 0:
            mag2 += .001
        angle = math.acos(.999 * dot/(mag1 * mag2)) * 180.0 / math.pi
        """
        checks that the biggest angle of the triangle is roughly 130 degrees and that the sides are similar sizes
        130 degrees corresponds to the 45 degree bend
        """
        MAX_ANG_DIF = 12
        MAX_LEN_DIF = 60
        MIN_LEN = 60
        TARGET_ANGLE = 130
        if mag1 > 100 or mag2 > 100:
            print "Angle, Mag1, Mag2: ", int(angle), int(mag1), int(mag2)
        #print angle
        if( abs(TARGET_ANGLE - abs(angle)) < MAX_ANG_DIF ) and abs(mag1 - mag2) < MAX_LEN_DIF and mag1 > MIN_LEN:
            out = obj([True, int(center[0]), int(center[1]), int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])])
            frameOut = out.draw(frameOut)

  debugFrame("out", frameOut)
  return out
def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
