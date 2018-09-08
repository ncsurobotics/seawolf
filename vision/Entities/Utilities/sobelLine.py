import numpy as np
import cv2
import math

keys = ["test1", "test2"]

def ProcessFrame(frame):
  exception("todo: make work as function")
  #blurred = cv2.medianBlur(frame, 5)
  blurred = cv2.medianBlur(frame, 5)
  #blurred = frame
  #blue = blurred[:,:,0]
  #green = blurred[:,:,1]
  #red = blurred[:,:,2]
  #cv2.imshow("red", red)
  #cv2.imshow("blue", blue)
  #cv2.imshow("green", green)
  out = {}
  out["test1"] = 1
  out["test2"] = 2
  hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
  #cv2.imshow('hue', hsv[:,:,0])
  #cv2.imshow('sat', hsv[:,:,1])
  sat = hsv[:,:,1]
  cv2.imshow('sat', sat)
  im = sat
  ret, ogThresh = cv2.threshold(im, 170, 255, cv2.THRESH_BINARY_INV)
  thresh = ogThresh
  kernel = np.ones((5,5), np.uint8)
  thresh = cv2.dilate(thresh, kernel, iterations = 3)
  cv2.imshow("thresh", thresh)
  contours, hierchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contoursThresh = []
  shp = frame.shape
  sobOut = np.ones((shp[0], shp[1])).astype(np.uint8)
  for cont in contours:
    a = cv2.contourArea(cont) + 1
    p = cv2.arcLength(cont,True)
    loc = (cont[0][0][0], cont[0][0][1])
    pa = p/a
    #print cv2.moments(cont, binaryImage = True)
    stringOut = "%d, %1.3f, %d" % (a, (p/a), len(cont))
    #cv2.putText(frame, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
    x,y,w,h = cv2.boundingRect(cont)
    wh = float(w)/h
    region = thresh[y:y+h, x:x+w]
    mom = cv2.moments(region)
    stringOut = "m10/ m01=%.2f" % (mom['nu20']/mom['nu02'])
    cv2.putText(frame, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    if a > 100 and a < 9000 and abs(1 - mom['nu20']/mom['nu02']) < .4:
      contoursThresh.append(cont)
      #cv2.putText(frame, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
      
      sobX = cv2.Sobel(region, cv2.CV_64F, 1, 0, ksize = 3)
      sobY = cv2.Sobel(region, cv2.CV_64F, 0, 1, ksize = 3)
      sob = (((np.arctan2(sobY, sobX)) + math.pi ) * 255/(2*math.pi)).astype(np.uint8)
      sob[sob == 127] = 0
      radians = sob[sob != 0]
      radains = cv2.GaussianBlur(radians, (5,5), 0)
      end = len(radians)
      diff = abs(radians[0:(end - 1)] - radians[1:end])
      corners = len(diff[diff > 60])
      sobOut[y:y+h, x:x+w] = sob
      
      
      
  cv2.drawContours(frame, contoursThresh, -1, (0,0, 0), 3)
  cv2.imshow("cont", frame)
  cv2.imshow("sob", sobOut)
  #cv2.imshow('val', hsv[:,:,2])
  return out




