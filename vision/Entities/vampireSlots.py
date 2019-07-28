import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects

visObj = "slots"
obj = visObjects[visObj]
keys = obj([False, []]).keys
SCREEN_AREA = 5000 #200000

vampireHoles = [(.187, .131), (.842, .134), (.596, .625)]
casinoHoles = [(.187, .131), (.842, .134), (.524, .888)]

# gradient coordinate of holes on slots rectangle
EXPECTED_HOLES = vampireHoles

def sortKeyVal(keyVal):
  return keyVal[1][0]

def mostCommonFrequencies(freqs, num=1):
  if num > len(freqs):
    raise ValueError("Not enough elements in dictionary")

  freqs_array = []
  for key in freqs:
    freqs_array.append([key, freqs[key]])
  freqs_array.sort(key = sortKeyVal, reverse=True)
  print "sorted", freqs_array

  keys = []
  for i in range(num):
    print "DIV", freqs_array[i]
    keys.append(freqs_array[i][1][1] / freqs_array[i][1][0])

  print "keys is", keys
  
  return keys

#isNearHole(EXPECTED_HOLES, (x, y), (x_min, y_min, width, height), 15)
def isNearHole(holes, contour_loc, board, cutoffDist):
  board_w, board_h = board
  contour_x, contour_y = contour_loc
  for hole in holes:
    abs_x, abs_y = board_w * hole[0], board_h * hole[1]
    print("RAEL DIST", math.sqrt( (abs_x - contour_x) ** 2 + (abs_y - contour_y) ** 2 ), abs_x, abs_y, contour_x, contour_y)
    if math.sqrt( (abs_x - contour_x) ** 2 + (abs_y - contour_y) ** 2 ) <= cutoffDist:
      return True
  return False

"""
Finds bent path in image where path is bends 45 degrees midway through.
"""
def ProcessFrame(frame):
  import time
  #time.sleep(.1)
  out = obj([False, []])
  
  #frame = norm(frame)
  frameOut = np.copy(frame)
  m = cv2.mean(frame)
  red = dist(frame, [0,  0, 255])
  red = blur = cv2.blur(red,(5,5))
  debugFrame("red", red)

  yellow = dist(frame, [0,  255, 255])
  yellow = blur = cv2.blur(yellow,(5,5))
  debugFrame("yellow", yellow)

  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  # multiplier of                                     std dev init was   2.65
  #ret, thresh = cv2.threshold(yellow, 100, 255, cv2.THRESH_BINARY_INV)
  w = 10
  ret, thresh = cv2.threshold(yellow, 213 - w, 213 + w, cv2.THRESH_BINARY_INV)
  debugFrame("threshOg", thresh)
  threshOg = thresh[::]
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)


  """
  Hough
  """

  circleList = []

  minDeg = 80.0
  s = .8
  d = 3.7 
  maxrad = 80
  minrad = 10
  step = 50
  """
  for radius in range(minrad + step, maxrad + 1, step):
    circles =  cv2.HoughCircles(image = red, method = cv2.cv.CV_HOUGH_GRADIENT, dp = 4.2, minDist =  2 * radius, param2 = int((2 * radius * math.pi)/8.94), minRadius = radius - step, maxRadius = radius)
    msg = "minRadius: %d, maxRadius %d" % (radius - step, radius)
    if type(circles) != type(None):
      print msg + " found: %d" % (len(circles))
      for circ in circles[0,:]:
        circleList.append(circ)
        cv2.circle(frameOut, (circ[0], circ[1]), circ[2], (0,0,0), 2, 8, 0 )
    else:
      print msg + " no circ found"
  """

  #lines

  maxDegDif = 15

  minLineLength = 100
  maxLineGap = 20

  std = 8
  edges = cv2.Canny(red, std * 2.5,  1.2* std)
  lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
  poles = []
  

  INIT_MIN = 9999
  INIT_MAX = -1
  min_x = INIT_MIN
  max_x = INIT_MAX
  min_y = INIT_MIN
  max_y = INIT_MAX

  # store x coords of vert lines, y of horiz. Categorize them into different value boundaries.
  horiz = {}
  vert = {}
  cut_off = 20
  min_height = 20
  min_width = 40

  if lines.__class__.__name__ != 'NoneType':
    for x0,y0,x1,y1 in lines[0]:
      theta = math.atan2(y1-y0, x1-x0)
      deg = theta * 180 / math.pi
      # vert lines
      if abs( abs(int(deg)) - 90) <= maxDegDif:
        #cv2.line(frameOut,(x0,y0),(x1,y1),(255,0,255),5)
        x_avg = (x0 + x1) / 2
        idx = x_avg / int(cut_off)
        if idx in vert:
          vert[idx][0] += 1
          vert[idx][1] += x_avg
        else:
          vert[idx] = [1, x_avg]
      
      # horiz lines
      if abs( abs(int(deg)) - 0) <= maxDegDif:
        #cv2.line(frameOut,(x0,y0),(x1,y1),(0,0,255),5)
        y_avg = (y0 + y1) / 2
        idx = y_avg / int(cut_off)
        if idx in horiz:
          horiz[idx][0] += 1
          horiz[idx][1] += y_avg
        else:
          horiz[idx] = [1, y_avg]

    try:
      max_num = 3
      if len(vert) < max_num:
        max_num = len(vert)
      x_list = mostCommonFrequencies(vert, num=max_num)
      #for x in x_list:
      #  cv2.line(frameOut,(x, 0),(x, 100),(255,255,255),5)
      x_min, x_max = min(x_list), max(x_list)

      
      max_num = 4
      if len(horiz) < max_num:
        max_num = len(horiz)
      y_list = mostCommonFrequencies(horiz, num=max_num)
      print "\t\t\t\t\t\t\t\t\tY's", y_list
      #for y in y_list:
      #  cv2.line(frameOut,(0, y),(100, y),(255,255,255),5)
      y_min, y_max = min(y_list), max(y_list)

      # height of the slots over the width
      targ_aspect_ratio = 1.7

      forceThrowOut = False
      try:
        actual_targ_aspect_ratio = float(y_max - y_min) / float(x_max - x_min)
      except Exception as e:
        forceThrowOut = False

      throwOut = forceThrowOut or abs(x_max - x_min) < min_width or abs(actual_targ_aspect_ratio - targ_aspect_ratio) > .4 #or abs(y_max - y_min) < min_height

      if not throwOut:
        h, w, _ = frame.shape
        cv2.rectangle(frameOut, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 255, 0), thickness=7, lineType=8, shift=0)
        #cv2.rectangle(frameOut, (int(x_min), int(0)), (int(x_max), int(h)), (255, 0, 0), thickness=7, lineType=8, shift=0)
        #targ_x =  
        #cv2.rectangle(frameOut, (int(x_min), int(0)), (int(x_max), int(h)), (255, 0, 0), thickness=7, lineType=8, shift=0)
        
        print "*" * 15, targ_aspect_ratio, 

        sub = thresh[y_min:y_max, x_min:x_max]
        debugFrame("sub", sub)

        #contours, _ = cv2.findContours(sub, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #contour_img = np.copy(frame[0:h, x_min:x_max])

        """
        Contours
        """
    
        contours, _ = cv2.findContours(sub, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_img = np.copy(frame[y_min:y_max, x_min:x_max])
        real_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # this is the area of the screen
            # often, the whole sceen is detected as a contour :/
            # here, we remove it
            #h, w, _ = sub.shape
            x, y, w, h = cv2.boundingRect(cnt)
            aspectRatio = float(h) / w
            if area < SCREEN_AREA and .5 <= aspectRatio and aspectRatio <= 2 and isNearHole(EXPECTED_HOLES, (x + w / 2, y + h / 2), (x_max - x_min, y_max - y_min), 30):
              cv2.drawContours(contour_img, [cnt], 0, (0,255,0), 3)
              real_contours.append(cnt)
        debugFrame("contours", contour_img)
        contours = real_contours

        holes = []
        for cnt in real_contours:
          x, y, w, h = cv2.boundingRect(cnt)
          holes.append((x + x_min, y + y_min, w, h))

          """
          possible_lens = [4]
          # and abs(area_side - perimeter_side) < 2
          if len(approx) in possible_lens and bound_actual_area_ratio > .5 and area > MIN_HOLE_AREA:
            cv2.fillConvexPoly(frameOut, approx, (255,0,0))
            hole = x,y,w,h
            holes.append(hole)
          """
        out = obj([True, holes])

    except ValueError as e:
      print "Not enough nums"
  
  #out.updateHistory(holes)
  frameOut = out.draw(frameOut)
  debugFrame("out", frameOut)
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
