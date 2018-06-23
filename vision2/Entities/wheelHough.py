import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from Utilities import bcluster
from VisObj import visObjects
import reader
import time
import random

visObj = "buoys"
obj = visObjects[visObj]
keys = obj().out.keys()
""" For seeing straight lines that the image processes. """
seeLines = True
seeCircles = False
seeClusters = True

"""Distance between 2 2d points."""
def distance(x1,y1,x2,y2):
  return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )

"""
Get twin angle of given angle, offset by 180 degrees. If given 20, return 200.
"""
def twin(rad):
  nrad = rad - math.pi
  return adjust(nrad)
def adjust(rad):
  while rad < 0:
    rad += math.pi * 2
  while rad > math.pi * 2:
    rad -= math.pi * 2
  return rad
"""
Target thetas in degrees, ie: [30, 75, ...]. Lines in houghLines format errorMaxAngle in degrees.
Return angleLines in format [[x1,y1,x2,y2], [x3,y3,x4,y4], ...]
"""
def angleLines(lines, targetThetas=[30,75], errorMaxAngle = 1):
  intersections = []
  angleLines = []
  lineCount = len(lines[0])
  if lineCount > 1:
    
    #biggest difference in angles to be a match
    maxAngleError = errorMaxAngle * math.pi / 180
    targetThetas = [30, 75]
    targetThetas = [theta * math.pi/180 for theta in targetThetas ]
    for i in range(lineCount):
      x1, y1, x2, y2 = lines[0][i]
      aTheta1 = math.atan2(y2 - y1, x2 - x1)
      aTheta2 = twin(aTheta1)
      for j in range(i + 1, lineCount):
        x3, y3, x4, y4 = lines[0][j]
        bTheta1 = math.atan2(y4 - y3, x4 - x3)
        bTheta2 = twin(aTheta1)
        #angle differences
        differences = [ aTheta1 - bTheta1, aTheta1 - bTheta2, aTheta2 - bTheta1, aTheta2 - bTheta2, bTheta1 - aTheta1, bTheta1 - aTheta2, bTheta2 - aTheta1, bTheta2 - aTheta2 ]
        #in radians
        differences = [adjust(theta) for theta in differences]
        for targetTheta in targetThetas:
          for difference in differences:
            targetDifference = abs(difference - targetTheta)
            if targetDifference <= maxAngleError:
              #lines are the right angle from each other
              #now, do they intesect?
              """ Denominator in formula to calculate line intersection """
              denominator = (x1 - x2)*(y3 - y4) - (y1 - y2) * (x3 - x4)
              if denominator != 0:
                """ Lines are not parallel """
                xnum = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
                ynum = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)

                """ Coordinates of where two lines would intersect """
                xintersect = xnum / denominator
                yintersect = ynum / denominator

                """ Checks that the intersection occurs on the line segment """
                if x1 <= x2:
                  xrange1 = [x1,x2]
                else:
                  xrange1 = [x2,x1]
                if x3 <= x4:
                  xrange2 = [x3,x4]
                else:
                  xrange2 = [x4,x3]
                if xrange1[0] <= xintersect and xintersect <= xrange1[1] and xrange2[0] <= xintersect and xintersect <= xrange2[1]:
                  #yes, they do intersect
                  intersections.append([xintersect, yintersect])
                  angleLines.append(lines[0][i])
                  angleLines.append(lines[0][j])
    return angleLines, intersections

def getIntersections(lines):
  intersections = []
  lineCount = len(lines)
  for i in range(lineCount):
    x1, y1, x2, y2 = lines[i]
    for j in range(i + 1, lineCount):
      x3, y3, x4, y4 = lines[i]
      
      """ Denominator in formula to calculate line intersection """
      denominator = (x1 - x2)*(y3 - y4) - (y1 - y2) * (x3 - x4)
      if denominator != 0:
        """ Lines are not parallel """
        xnum = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
        ynum = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)

        """ Coordinates of where two lines would intersect """
        xintersect = xnum / denominator
        yintersect = ynum / denominator

        """ Checks that the intersection occurs on the line segment """
        if x1 <= x2:
          xrange1 = [x1,x2]
        else:
          xrange1 = [x2,x1]
        if x3 <= x4:
          xrange2 = [x3,x4]
        else:
          xrange2 = [x4,x3]
        if xrange1[0] <= xintersect and xintersect <= xrange1[1] and xrange2[0] <= xintersect and xintersect <= xrange2[1]:
          #yes, they do intersect
          intersections.append([int(xintersect), int(yintersect)])


  return intersections
def getAvgPt(pts):
  total = []
  dim = len(pts[0])
  count = 0
  for i in range(dim):
    total.append(0)
  for pt in pts:
    for i in range(dim):
      total[i] += pt[i]
    count += 1
  return [int(tot / count) for tot in total ]


"""
Process Overview:
Finds circles in image
Finds lines (may need to only select lines near circles).
Find intersections of lines and get average intersection: this is near the circle center
Choose the circle with center closest to this average point
"""

def ProcessFrame(frame):
  out = obj()
  frameOut = frame.copy()
  frame = norm(frame)
  mean, std = cv2.meanStdDev(frame)
  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  print "m: %d, std %d" % (mean, std)
  #r = frame[:, :, 2]
  r = cv2.GaussianBlur(r, (9, 9), 0)
  debugFrame("ChannelOfInterest", r)
  edges = cv2.Canny(r, std * 2.5,  1.2* std)
  debugFrame("edges", edges)
  height, width = frame.shape[:2]
  outImg = np.zeros((height,width,3), np.uint8)
  #frameOut = outImg
  """
  Below is the param info for HoughCircles
    image is the imaged being looked at by the function
    method cv2.CV_HOUGH_GRADIENT is the only method available
    dp the size of accumulator inverse relative to input image, dp = 2 means accumulator is half dim of input image
    minDist minimum distance between detected circles, too small and mult neighbor circ founds, big and neighbor circ counted as same
    param1 bigger value input into canny, unsure why it is useful therefore not using
    param2 vote threshold
    minRadius  min Radius of circle to look for
    maxRadius  max Radius of circle to look for
  """

  """ Find and make list of circles in the image """
  
  drawAvg = False
  circleList = []

  minDeg = 80.0
  s = .8
  d = 3.7  
  """
  maxrad = 250
  minrad = 75
  step = 50
  delay = 0
  try:
    d, s, minDeg, minrad, maxrad, step, delay = reader.readVars('/home/ben/seawolf/vision2/info.txt')
  except Exception as e:
    print "Fail+++++++++++++++++++++++++ ++++++++++++++++++++++++++++++++++++               ++++++++="
    print e
  time.sleep(delay)
  """
  maxrad = 300
  minrad = 50
  step = 50
  for radius in range(minrad + step, maxrad + 1, step):
    circles =  cv2.HoughCircles(image = r, method = cv2.cv.CV_HOUGH_GRADIENT, dp = 3.4, minDist =  radius * 2, param2 = int((2 * radius * math.pi)/6.5), minRadius = radius - step, maxRadius = radius)
    msg = "minRadius: %d, maxRadius %d" % (radius - step, radius)
    if type(circles) != type(None):
      print msg + " found: %d" % (len(circles))
      for circ in circles[0,:]:
        #rint "circ: ", circ
        circleList.append(circ)
        if seeCircles:
          cv2.circle(frameOut, (circ[0], circ[1]), circ[2], (0,0,0), 2, 8, 0 )
    else:
      print msg + " no circ found"
  if len(circleList) > 0:
    """ Finds lines in image, hopefully the lines of the slices in the wheel. May have to adjust the Min line length for further away wheels """
    minLineLen = 61
    maxGap = 62
    linePts = 128
    """
    try:
      d, s, minLineLen, maxGap, linePts, step, delay = reader.readVars('/home/ben/seawolf/vision2/info.txt')
    except Exception as e:
      print "Fail+++++++++++++++++++++++++ ++++++++++++++++++++++++++++++++++++               ++++++++="
      print e
    time.sleep(delay)
    """


    lines = cv2.HoughLinesP(edges, 4, math.pi/180, linePts, minLineLength = minLineLen, maxLineGap = linePts)
    
    """ Max number of lines in the image to process through """
    maxLines = 20
    if type(lines) == type(None):
      lineCount = 0
    else:
      lineCount = len(lines[0])
      if lineCount < maxLines:
        try:
          lines, intersections = angleLines(lines, errorMaxAngle = 1)
          lineCount = len(lines)
        except Exception:
          lineCount = 0

    foundCenter = False

    if 0 < lineCount and lineCount < maxLines:
      #intersections = getIntersections(lines)
      intersectionCount = len(intersections)
      #print "Intersection count--------00000000000000000000000000000000000000", intersectionCount
      """ Find average of intersection points """
      if intersectionCount > 0:
        if seeLines:
          for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(frameOut, (x1, y1), (x2, y2), (255, 0,0), 2 )

        ptTotal = [0,0,0]
        clusters = bcluster.findClusters(intersections, 35)
        for cluster in clusters:
          color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
          for pt in cluster:
            x, y = pt
            if seeClusters:
              cv2.circle(frameOut, (int(x), int(y)), 7, color, 2, 8, 0 )
            ptTotal[0] += pt[0]
            ptTotal[1] += pt[1]
            ptTotal[2] += 1
          if seeLines:
            cv2.circle(frameOut, (pt[0], pt[1]), 7, (255,255,255), -2, 8, 0 )
        #biggest custer at front of cluster list
        intersections = clusters[0]
        ptTotal = [0,0,0]
        if seeLines:
          for pt in intersections:
            cv2.circle(frameOut, (pt[0], pt[1]), 7, (255,255,255), -2, 8, 0 )
        xIntAvg, yIntAvg = getAvgPt(intersections)
        """Find the furthest point on a line from the center"""
        maxDist = 0
        for line in lines:
          x1,y1,x2,y2 = line
          dist1 = distance(xIntAvg, yIntAvg, x1, y1)
          dist2 = distance(xIntAvg, yIntAvg, x2, y2)
          if dist1 > maxDist or dist1 > maxDist:
            maxDist = max(dist1, dist2)
        out.append([xIntAvg, yIntAvg, int(maxDist)])
    """        
    else:
      if len(circleList) > 1:
        maxCirc = circleList[0]
        for circ in circleList:
          if circ[2] > maxCirc[2]:
            maxCirc = circ
        out.append(maxCirc)
    """
  
  
  frameOut = out.draw(frameOut)
  out.draw(frameOut)

  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
