import cv2
import numpy as np
from Utilities import norm


keys = ["leftPole", "rightPole", "centerPoint"]
lp = "leftPole"
rp = "rightPole"
cp = "centerPoint"

def ProcessFrame(frame):
  out = {}
  out[lp] = 0
  out[rp] = 0
  out[cp] = 0
  frame = norm(frame)
  red = frame[:,:,2]
  debugFrame("red", red)
 
 
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  ret, thresh = cv2.threshold(red, 120, 255, cv2.THRESH_BINARY)
  kernel = np.ones((5,5),np.uint8)
  thresh = cv2.dilate(thresh,kernel, iterations = 1)
  debugFrame("thresh", thresh)
  _, contours, hierchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  possiblePoles = []
  for cont in contours:
    (center, (w, h), ang) = cv2.minAreaRect(cont)
    area = w * h
    aspectRatio = h / w
    if aspectRatio < 1:
    	aspectRatio = 1/aspectRatio
    angp = abs(ang)
    angp = abs(angp - round((angp/90.0)) * 90)
    if angp < 10.0 and area > minArea and abs(aspectRatio - 7) < 2:
      possiblePoles.append((cont, center))
    
  possiblePoles = sorted(possiblePoles, key = sortPoles)
  if len(possiblePoles) > 1:
  	prevPole = possiblePoles[0]
  	poles = [prevPole]
  	for pole in possiblePoles:
  	  diff = abs( pole[1][0] - prevPole[1][0])
  	  if (diff > 20):
  	    poles.append(pole)
  	  prevPole = pole 
  	if (len(poles) == 2):
  	  left = poles[0]
  	  right = poles[1]
  	  out[rp] = int(right[1][0])
  	  out[lp] = int(left[1][0])
  	  out[cp] = out[lp] + (out[rp] - out[lp])/2
  	  cv2.circle(frame, (out[cp], int((right[1][1] + left[1][1])/2)), 10, (0, 0, 0), 3)
  	  cv2.drawContours(frame, [left[0], right[0]], -1, (0,0, 0), 3) 
  	  
  debugFrame("out", frame) 
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
