import cv2
import numpy as np
#2d source triangle
#3d points, dest triangle
#image
#convert to 2 points
#draw to camera

"""
Warps and alpha blends triangular regions from img1 and img2 to img.
Code from https://www.learnopencv.com/warp-one-triangle-to-another-using-opencv-c-python/
"""
def warpTriangle(img1, img2, tri1, tri2) :
    
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(tri1)
    r2 = cv2.boundingRect(tri2)

    h, w, _ = img2.shape
    
    #only allow r2 to live on screen
    r2_x, r2_y, r2_w, r2_h = r2
    #x
    if r2_x <= 0:
      r2_x = 0
    #y
    if r2_y <= 0:
      r2_y = 0
    #x+w
    if r2_x + r2_w >= w:
      r2_w = w - r2_x - 1
    #y+h
    if r2_y + r2_h >= h:
      r2_h = h - r2_y - 1
    r2 = (r2_x, r2_y, r2_w, r2_h)
    
    #print r2
    

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
  def draw(self, img, drawPts=False):
    warpTriangle(self.srcImg, img, self.srcTri2d, self.dest2d)
    if drawPts:
      i = 0
      cols = [(0,0,255), (0,255,0), (255,0,0)]
      for pt in self.dest2d[0]:
        x = int(pt[0])
        y = int(pt[1])
        cv2.circle(img, (x,y), 6, cols[i], -1)
        i += 1

  def convertTo2d(self, camera, offset):
    #iterate through 3d points
    pts2d = []
    for pt in self.points:
      #add offset
      pt2d = [0,0]
      pts2d.append(pt2d)
    self.srcTri2d = np.float32([pts2d])
    return self.srcTri2d
  
  def setDest2d(self, newPts):
    self.dest2d = np.float32([newPts])

"""
  #assume convertTo2d has been called
  #offset is location in 3d space with camera
  def draw(self, camera, offset):
    #for pt in self.srcTri2d:
    pass
"""

"""
imgIn = cv2.imread("robot.jpg")
imgOut = 255 * np.ones(imgIn.shape, dtype = imgIn.dtype)

t = Triangle(0, 0, imgIn)
t.draw(imgOut)
cv2.imshow("Output", imgOut)
cv2.waitKey(0)
"""