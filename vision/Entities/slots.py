import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "slots"
obj = visObjects[visObj]
keys = obj([False, []]).keys
SCREEN_AREA = 200000

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
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  
  """
  Contours
  """
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contour_img = np.copy(frame)
  real_contours = []
  for cnt in contours:
      area = cv2.contourArea(cnt)
      # this is the area of the screen
      # often, the whole sceen is detected as a contour :/
      # here, we remove it
      if area < SCREEN_AREA / 10:
        cv2.drawContours(contour_img, [cnt], 0, (0,255,0), 3)
        real_contours.append(cnt)
  debugFrame("contours", contour_img)
  contours = real_contours

  mean, std = cv2.meanStdDev(frame)
  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  r = cv2.GaussianBlur(r, (9, 9), 0)

  holes = []
  for i in range(len(contours)):
    epsilon = 0.02*cv2.arcLength(contours[i],True)
    approx = cv2.approxPolyDP(contours[i],epsilon,True)
    perimeter = cv2.arcLength(contours[i], True)
    area = cv2.contourArea(contours[i])
    # 4 sides means this may be a rectangle
    # if rectangle, then perimeter = 2 * (L + W) and area = L * W
    # if pretend rectangle is square, L = W -> p = 4 * S, a = S ^ 2
    # then S should be sqrt(a) or p / 4
    area_side = math.sqrt(area)
    perimeter_side = perimeter / 4
    x,y,w,h = cv2.boundingRect(contours[i])
    area_bound = w * h
    MIN_HOLE_AREA = 400

    bound_actual_area_ratio = 0
    if area_bound != 0 and area != 0:
      bound_actual_area_ratio = area_bound / area
      if area > 1:
        bound_actual_area_ratio = area / area_bound

    print "area", area, bound_actual_area_ratio
    possible_lens = [4]
    # and abs(area_side - perimeter_side) < 2
    if len(approx) in possible_lens and bound_actual_area_ratio > .5 and area > MIN_HOLE_AREA:
      cv2.fillConvexPoly(frameOut, approx, (255,0,0))
      hole = x,y,w,h
      holes.append(hole)
  
  out = obj([True, holes])
  out.updateHistory(holes)
  frameOut = out.draw(frameOut)
  debugFrame("out", frameOut)
  return out
def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
