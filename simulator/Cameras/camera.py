import cv2
import numpy as np
import svr

NEAR = -1
FAR = -2
BEHIND = -3
GOOD = 1

DB = False
def dbPrint(msg):
  if DB:
    print msg
#all [x, y, z] arrays are expected to be in meters and of the format, +x is right, +y is forward, neg z is down. 

class Camera(object):

  """
  name = name of the svr stream to show
  frameSize = 1 by 2 array that holds the size of the desired frame
  transform = np.float32 3 by 3 matrix that when a 1 by 3 input point is multiplied by it, it turns it into [x, y, 1/sf] were x and y are points on the image, and the last number is the scale
  sf = scalefactor in meters per pixel  
  """
  def __init__(self, name, 
                     frameSize = [480, 640, 3], 
                     transform = np.float32([[1, 0, 0], [0, 1, 0], [0, 0, -1]]),
                     sf = .01
              ):
   
    
    self.frameSize = frameSize
    offset = np.float32(self.frameSize)[:2]/2
    self.offset = np.float32([offset[1], offset[0]])
    self.name = name
    self.count = 0
    
    #the effect of distance on the size of things, in example at a sf of .01 and distance of 1 meter, 1 meter takes up 100 pixels.
    self.far = 10 * sf
    self.near = .001 * sf
    
    #the matrix for scailing, makes the last cordinate the distance/scale factor
    self.transform = transform
    
    #making the next frame
    self.newFrame()
  
  def newFrame(self):
    self.frame = np.zeros(self.frameSize, np.uint8)
  
  
 
  #displays frame on svr
  def show(self):
    #cv2.imshow(self.name, self.frame)
    
    cv2.imwrite("./PICS/" + self.name + str(self.count) + ".png", self.frame)
    self.count+= 1
    #converting image to type desired by svr
    container = cv2.cv.fromarray(np.copy(self.frame))
    cv_image = cv2.cv.GetImage(container)
    svr.debug(self.name, cv_image)
  
  
  """
  draws line on camera plane
  p1 = start point of line [x, y, z]
  p2 = end point of line [x, y, z]
  color = (b, g, r) color of line
  thickness = widht of line in meters
  """
  def drawLine(self, p1, p2, color, thickness):
    (cont, pts) = self.scalePts([p1, p2])
    if cont < 0:
      return self.scaleErr(cont, color)
      
    #scaling the width of line to be drawn
    thickness = int(thickness * (self.getSF(p1) + self.getSF(p2))/2)
    
    #doing this because openCV draw line function does not accept bigger thickness
    if thickness > 255:
      thickness = 255
    
    #making the points intgers and setting up for line
    pts = np.int32(pts)
    p1 = pts[0]
    p2 = pts[1]
    
    cv2.line(self.frame, (p1[0], p1[1]), (p2[0], p2[1]), color, thickness = thickness)
    return
  
  """
  used to scale list of pts, 
  pts = [ [x, y, z], [x, y, z], ...] list/array of pts to scale
  returns [x, y] pts to put on frame
  """
  def scalePts(self, pts):
    outPts = []
   
    for pt in pts:
      dbPrint( pt )
      pt = np.dot(self.transform, pt)
      dbPrint( pt )
      dbPrint( "*****")
      if pt[2] < 0: 
        return (BEHIND, outPts)
      elif pt[2] < self.near:
        return (NEAR, outPts)
      elif pt[2] > self.far:
        return (FAR, outPts)
      else:
        pt = pt/pt[2]
        outPts.append(self.offset - pt[0:2])
    
    return (GOOD, outPts)
  
  """
  pt = [x, y, z], pt to get the desired scale factor
  return muliply value by return value to scale it
  """
  def getSF(self, pt):
    #print (np.dot(self.transform, pt)[2])
    
    return 1/ (np.dot(self.transform, pt)[2])
  
  """ handles erros cases when scaling """
  def scaleErr(self, Err, color):
    dbPrint( Err)
    #currently nothing done when 0 distance when projecting to plane of picture, this either means picture is off frame or whole frame should be this color
    return
    
  """
  draws polygon on camera frame
  pts = pts of the corner of the polygon to draw in 3d space
  color = (b, g, r) color of the polygon
  """
  def drawPoly(self, pts, color):
    (cont, pts) = self.scalePts(pts)
    if cont > 0:
      cv2.fillConvexPoly(self.frame, np.int32([pts]), color)
    else:
      self.scaleErr(cont, color)
  
  """
  draws circle in camera plane
  pt = point in 3d space relative to camera in meters of the center of the circle
  rad = radius in meters of the circle
  color = (b, g, r)
  """
  def drawCirc(self, pt, rad, color):
    (cont, pts) = self.scalePts([pt])
    if cont < 0:
      return self.scaleErr(cont, color)
    rad = int(rad * self.getSF(pt))
    ptc = np.int32(pts[0])
    dbPrint(pt)
    dbPrint(rad)
    if cont > 0:
      cv2.circle(self.frame,(ptc[0], ptc[1]) , rad, color = color, thickness = -1)
    else:
      self.scaleErr(cont, color)
  
  
  
  
  
  
