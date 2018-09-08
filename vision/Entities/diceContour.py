import cv2
import numpy as np
import math
from Utilities import GatePole as Pole
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "buoys"
obj = visObjects[visObj]
keys = obj().out.keys()

def ProcessFrame(frame):
  print("called")
  out = obj()
  frameOut = frame.copy()
  HEIGHT,WIDTH,_  = frame.shape
  contImg = np.zeros((HEIGHT,WIDTH,3), np.uint8)
  frame = norm(frame)
  mean, std = cv2.meanStdDev(frame)

  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  print "m: %d, std %d" % (mean, std)
  #r = frame[:, :, 2]
  r = cv2.GaussianBlur(r, (9, 9), 0)
  debugFrame("red", r)
  if std > 6:
    edges = cv2.Canny(r, std * 1.8 , std * 1.2)
  else:
    edges = cv2.Canny(r, 30 , 20)
  debugFrame("edges", edges)
  lines = cv2.HoughLinesP(edges, 4, math.pi/180, 200, minLineLength = 100, maxLineGap = 50)
  if isinstance(lines, list):
    print "numLines: %d" % len(lines[0])
    for line in lines[0]:
      p1 = (line[0], line[1])
      p2 = (line[2], line[3])
      dx = p1[0] - p2[0]
      dy = abs(p1[1] - p2[1])
      theta = math.atan2(dy, dx)
      if abs(theta - math.pi/2) <  10 *math.pi/180:
        cv2.line(frameOut, p1, p2, (255, 0, 255), 5)

  contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  dice = []
  for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if area < WIDTH * HEIGHT / 2:
      cv2.drawContours(contImg, contours, i, (255, 255, 255), 5)
      x,y,w,h = cv2.boundingRect(contours[i])
      if w * h > 700 and h != 0 and w/h < 2 and w/h > 1/2:
        cv2.rectangle(frameOut,(x,y),(x+w,y+h),(0,0,255),2)
        dice.append([x + w/2, y + h/2, (w+h) / 2])

  
  debugFrame("contours", contImg)
  print "Contours: ", len(contours)
  if(len(dice) >= 2):
    for die in dice:
      out.append(die)
  frameOut = out.draw(frameOut)

  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
