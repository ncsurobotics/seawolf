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
  # multiplier of                                     std dev init was   2.65
  ret, thresh = cv2.threshold(red, np.mean(red) - max(np.std(red), 10) * 1.20065, 255, cv2.THRESH_BINARY_INV)
  debugFrame("threshOg", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  mean, std = cv2.meanStdDev(frame)
  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  r = cv2.GaussianBlur(r, (9, 9), 0)
  

  std = std if std > 6 else 6
  std_scale = 2.7
  edges = cv2.Canny(r, std * std_scale, std * std_scale)
  debugFrame("edges", edges)

  lines = cv2.HoughLinesP(edges, 4, math.pi/180, 40, minLineLength = 60, maxLineGap = 20)
  parallel = {}
  group_thresh = 10.0 * math.pi/180.0
  poles = []
  # how similar in degrees angles need to be to be viewed as parallel
  DEG_CLOSENESS = 15
  if isinstance(lines, np.ndarray) and (len(lines[0]) > 30):
    return out
  if isinstance(lines, np.ndarray):
    #print "numLines: %d" % len(lines[0])
    for line in lines[0]:
      p1 = (line[0], line[1])
      p2 = (line[2], line[3])
      dx = p1[0] - p2[0]
      dy = abs(p1[1] - p2[1])
      theta = math.atan2(dy, dx)
      # standardize theta to be positive, (a line's angle can be represented either way it could point)
      if theta <0:
        theta = theta + math.pi
      #cv2.line(frameOut, p1, p2, (0, 0, 255), 5)

      rounded_angle = int( (theta * 180 / math.pi) / (DEG_CLOSENESS) )
      if rounded_angle not in parallel:
        parallel[rounded_angle] = [(line, theta)]
      else:
        parallel[rounded_angle].append( (line, theta) )
    
    parallel_groups = 0
    for angle in parallel:
      group = parallel[angle]
      if len(group) > 1:
        parallel_groups += 1

    if parallel_groups >= 2:
      avg_lines = []
      print "+" * 10, parallel_groups
      for angle in parallel:
        group = parallel[angle]
        if len(group) > 1:
          grey_col = 0#angle * 1000 % 255
          color = (grey_col, grey_col, grey_col)
          print "group is", "angle", angle, "len", len(group)
          avg_line = [0,0,0,0]
          for line, angle in group:
            p1 = (line[0], line[1])
            p2 = (line[2], line[3])
            for i in range(4):
              avg_line[i] += line[i]
            cv2.line(frameOut, p1, p2, color, 5)
          # draw avg line
          for i in range(4):
            avg_line[i] /= len(group)
          p1 = (avg_line[0], avg_line[1])
          p2 = (avg_line[2], avg_line[3])
          cv2.line(frameOut, p1, p2, (0, 0, 255), 5)
          avg_lines.append(avg_line)

      DIST_THRESH = 60
      RADIUS = 5
      JOINT_COLOR = (255,0,0)
      
      joint_groups = []
      #iterate thru all avg lines and find ones that r close, then "save" the ones that r
      # also find 2 furthest away points
      max_dist = 0
      max_pts = (0,0), (0,0)
      for i in range(len(avg_lines)):
        for j in range(i + 1, len(avg_lines)):
          x1,y1,x2,y2 = avg_lines[i]
          x3,y3,x4,y4 = avg_lines[j]
          coord_groups = ( ( (x1,y1), (x2,y2) ), ( (x3,y3), (x4,y4) ) )
          # iterate thru all combos between x/y 1 & 2 and x/y 3 & 4
          for k1 in range(2):
            for k2 in range(2):
              x1 = coord_groups[0][k1][0]
              y1 = coord_groups[0][k1][1]
              x2 = coord_groups[1][k2][0]
              y2 = coord_groups[1][k2][1]
              
              new_dist = math.sqrt( (x1 - x3) ** 2 + (y1 - y3) ** 2 )
              if new_dist <= DIST_THRESH:
                cv2.circle(frameOut, (x1,y1), RADIUS, JOINT_COLOR, -1)
                cv2.circle(frameOut, (x3,y3), RADIUS, JOINT_COLOR, -1)
                joint_groups.append(avg_lines[i])
                joint_groups.append(avg_lines[j])
                if new_dist >= max_dist:
                  max_dist = new_dist
                  max_pts = (x1,y1), (x2,y2)

        # draw joint groups
        for line in joint_groups:
          p1 = (line[0], line[1])
          p2 = (line[2], line[3])
          cv2.line(frameOut, p1, p2, (0, 255, 255), 3)

        if len(joint_groups) != 0:
          FAR_COLOR = (255,255,255)
          cv2.circle(frameOut, max_pts[0], 7, FAR_COLOR, -1)
          cv2.circle(frameOut, max_pts[1], 7, FAR_COLOR, -1)


          
            
      
        

      import time
      time.sleep(.01)


  
  for i in range(len(contours)):
      epsilon = 0.085*cv2.arcLength(contours[i],True)
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
        if( abs(TARGET_ANGLE - abs(angle)) < 5 ) and abs(mag1 - mag2) < MAX_LEN_DIF and mag1 > MIN_LEN:
            out = obj([True, int(center[0]), int(center[1]), int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])])
            frameOut = out.draw(frameOut)

  debugFrame("out", frameOut)
  return out
def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
