import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects

visObj = "buoys"
obj = visObjects[visObj]
keys = obj().out.keys()
""" For seeing straight lines that the image processes. """
seeLines = True

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

  maxrad = 300
  minrad = 75
  step = 50
  drawAvg = False
  circleList = []
  for radius in range(minrad + step, maxrad + 1, step):
    circles =  cv2.HoughCircles(image = r, method = cv2.cv.CV_HOUGH_GRADIENT, dp = 3.7, minDist =  radius * 2, param2 = int((2 * radius * math.pi)/12), minRadius = radius - step, maxRadius = radius)
    msg = "minRadius: %d, maxRadius %d" % (radius - step, radius)
    if type(circles) != type(None):
      print msg + " found: %d" % (len(circles))
      for circ in circles[0,:]:
        print "circ: ", circ
        circleList.append(circ)
        #cv2.circle(frameOut, (circ[0], circ[1]), 7, (0,0,0), 2, 8, 0 )
    else:
      print msg + " no circ found"

  """ Finds lines in image, hopefully the lines of the slices in the wheel. May have to adjust the Min line length for further away wheels """
  lines = cv2.HoughLinesP(edges, 4, math.pi/180, 200, minLineLength = 40, maxLineGap = 50)
  
  """ Max number of lines in the image to process through """
  maxLines = 20
  if type(lines) == type(None):
    lineCount = 0
  else:
    lineCount = len(lines[0])

  foundCenter = False

  if 0 < lineCount and lineCount < maxLines:
    intersections = []
    intersectionCount = 0
    """ Loop through all combinations of lines O(lineCount ^ 2) """
    
    for i in range(0, lineCount):
      """ Line 1 """
      x1,y1,x2,y2 = lines[0][i]
      
      for j in range(i + 1, lineCount):
        """ Line 2 """
        x3,y3,x4,y4 = lines[0][j]

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
            intersections.append([xintersect, yintersect])
            intersectionCount += 1
      if seeLines:
        cv2.line(frameOut, (x1, y1), (x2, y2), (255, 0,0), 2 )
    
    """ Find average of intersection points """
    if intersectionCount > 0:
      ptTotal = [0,0,0]
      for pt in intersections:
        ptTotal[0] += pt[0]
        ptTotal[1] += pt[1]
        ptTotal[2] += 1
      
      xIntAvg = ptTotal[0] / ptTotal[2]
      yIntAvg = ptTotal[1] / ptTotal[2]
      #cv2.circle(frameOut, (xIntAvg, yIntAvg), 7, (0,0,255), 2, 8, 0 )
      """ Find the average amount each point drifts from the average """
      error = [0,0]

      for pt in intersections:
        error[0] += math.sqrt( (xIntAvg - pt[0]) ** 2 + (yIntAvg - pt[1]) ** 2 )
        error[1] += 1
      errorAvg = error[0] / error[1]
      """
      radiusTotal = 0
      for line in lines[0]:
        radiusTotal += math.sqrt( (line[0] - xIntAvg) ** 2 + (line[1] - yIntAvg) ** 2 )
        radiusTotal += math.sqrt( (line[2] - xIntAvg) ** 2 + (line[3] - yIntAvg) ** 2 )
      radius = int(radiusTotal / lineCount)
      """

      """ Check that there isn't a huge gap between the intersecting points """
      errorThreshold = 30
      if errorAvg < errorThreshold:

        """ Find radius of circle closest to average intersection """
        if len(circleList) > 1:
          closestCirc = circleList[0]
          for circ in circleList:
            if math.sqrt( (xIntAvg - circ[0]) ** 2 + (yIntAvg - circ[1]) ** 2 ) < math.sqrt( (xIntAvg - closestCirc[0]) ** 2 + (yIntAvg - closestCirc[1]) ** 2 ):
              closestCirc = circ
  
          out.append([xIntAvg, yIntAvg, closestCirc[2]])
  else:
    if len(circleList) > 1:
      maxCirc = circleList[0]
      for circ in circleList:
        if circ[2] > maxCirc[2]:
          maxCirc = circ
      out.append(maxCirc)
  
  
  frameOut = out.draw(frameOut)
  out.draw(frameOut)
  #if drawAvg:
    #cv2.circle(frameOut, (int(avg[0]), int(avg[1])), int(avg[2]), (0,0,0), 2, 8, 0 )
  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
