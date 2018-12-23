import cv2
import numpy as np
#2d source triangle
#3d points, dest triangle
#image
#convert to 2 points
#draw to camera

"""
Return bounding box that is adjusted for image boundaries.
"""
def getBoundingBox(img, tri):
  # Find bounding rectangle for triangle inside the image
  r = cv2.boundingRect(tri)
  # height and width of img
  h, w, _ = img.shape
  
  #only allow r to be on screen
  r_x, r_y, r_w, r_h = r
  #x
  if r_x <= 0:
    r_x = 0
  #y
  if r_y <= 0:
    r_y = 0
  #x+w
  if r_x + r_w >= w:
    r_w = w - r_x - 1
  #y+h
  if r_y + r_h >= h:
    r_h = h - r_y - 1

  if r_w < 0:
    r_w = 0
  if r_h < 0:
    r_h = 0

  r = (r_x, r_y, r_w, r_h)
  return r

# Warps and alpha blends triangular regions from img1 and img2 to img, or src to dest, or foreground to background
# Using code from https://www.learnopencv.com/warp-one-triangle-to-another-using-opencv-c-python/
def warpTriangle(img1, img2, tri1, tri2, alpha=None) :

  r1 = cv2.boundingRect(tri1)
  r2 = getBoundingBox(img2, tri2)

  # Offset points by left top corner of the respective rectangles
  tri1Cropped = []
  tri2Cropped = []
  
  for i in xrange(0, 3):
      tri1Cropped.append(((tri1[0][i][0] - r1[0]),(tri1[0][i][1] - r1[1])))
      tri2Cropped.append(((tri2[0][i][0] - r2[0]),(tri2[0][i][1] - r2[1])))

  # Crop input image
  img1Cropped = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

  # Given a pair of triangles, find the affine transform.
  warpMat = cv2.getAffineTransform( np.float32(tri1Cropped), np.float32(tri2Cropped) )

  # Apply the Affine Transform just found to the src image
  img2Cropped = cv2.warpAffine( img1Cropped, warpMat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

  # Get mask by filling triangle
  mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
  
  cv2.fillConvexPoly(mask, np.int32(tri2Cropped), (1.0, 1.0, 1.0), 16, 0)

  img2Cropped = img2Cropped * mask

  # Copy triangular region of the rectangular patch to the output image
  img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )
  
  img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Cropped
  #return img2

class Triangle(object):
  # points should be in form [[x1,y1], [x2,y2], ..., [xn,yn]]
  # tricoords in form of [[x1,y1,z1], [x2,y2,z2], ..., [xn,yn,zn]]
  def __init__(self, srcTri, img):
    #self.srcTri3d = 
    self.srcTri2d = srcTri
    self.srcImg = img #img
    #only need to update this
    #self.dest2d = [[400,200], [160,270], [400,400]]
    self.srcTri2d = np.float32([self.srcTri2d])
    #self.dest2d = np.float32([self.dest2d])
    pass
  
  #draw points used for debugging
  def draw(self, img, drawPts=False, alpha=None):
    newFrame = warpTriangle(self.srcImg, img, self.srcTri2d, self.dest2d, alpha=alpha)
    if drawPts:
      i = 0
      cols = [(0,0,255), (0,255,0), (255,0,0)]
      for pt in self.dest2d[0]:
        x = int(pt[0])
        y = int(pt[1])
        cv2.circle(img, (x,y), 6, cols[i], -1)
        i += 1
  def setDest2d(self, newPts):
    self.dest2d = np.float32([newPts])