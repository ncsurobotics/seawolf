import cv2
import numpy as np


from VisObj import visObjects


visObj = "gate"
obj = visObjects[visObj]
keys = (obj([False, 0, 0])).keys


def ProcessFrame(frame):
  out = obj([False, 0, 0])
  red = frame[:,:,2]
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  ret, thresh = cv2.threshold(red, 120, 255, cv2.THRESH_BINARY)
  kernel = np.ones((5,5),np.uint8)
  thresh = cv2.dilate(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  contours, hierchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
  	  out = obj([True, int(right[1][0]), int(left[1][0])])
  	  frame = out.draw(frame)
  	  cv2.drawContours(frame, [left[0], right[0]], -1, (0,0, 0), 3) 
  	  
  debugFrame("out", frame)
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
