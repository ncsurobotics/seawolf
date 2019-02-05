import cv2
import numpy as np

"""
Params:
- image
- box in form x,y,w,h
- amount to scale by (floating point)
- offset of output image in output image

Returns: (img, new_rects)
- scaled image, fit inside of the original dimensions
- how the rectangles map onto the scaled image
"""

def scale(img, rect, scale):
  new_rect = None
  img = cv2.resize(img, None, fx=scale, fy=scale)
  new_rect = []
  for i in range(len(rect)):
    new_rect.append(scale * rect[i])
  x,y,w,h = new_rect
  x,y,w,h = int(x), int(y), int(w), int(h)
  out_img = np.zeros((h, w, 3), np.uint8)
  out_img = img[y:y+h, x:x+w]

  

  return out_img, (0,0,w,h)

"""
Using algorithm from https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/

Params:

- image
- box around object in form x,y,w,h
- amount to rotate by (degrees)
- dim of output image (h,w)

Returns: (img, new_rects)
- rotated image (adjusted size for rotation)
- how the rectangles map onto the rotated image
"""
def rotate(img, rect, angle):
  h, w, _ = img.shape
  M = cv2.getRotationMatrix2D((w/2,h/2), -angle,1)
  cos = np.abs(M[0,0])
  sin = np.abs(M[0,1])
  nW = int(h*sin + w*cos)
  nH = int(h*cos + w*sin)
  M[0, 2] += (nW/2) - (w/2)
  M[1, 2] += (nH/2) - (h/2)
  
  dst = cv2.warpAffine(img,M,(nW,nH))
  new_rect = None
  return dst, new_rect

def rotate_cut(img, rect, angle):
  h, w, _ = img.shape
  M = cv2.getRotationMatrix2D((w/2,h/2), -angle,1)
  
  dst = cv2.warpAffine(img,M,(w,h))
  new_rect = None
  return dst, new_rect


def main():
  name = '/home/ben/seawolf/vision/Trainer/Plotter/haar_train/pos/frame-131.jpg'
  img = cv2.imread(name)
  img, _ = scale(img, (100, 100, 400, 400), .3)
  deg = 0
  while True:
    rot_img, _ = rotate_cut(img, None, deg)
    deg += 10
    cv2.imshow('image', rot_img)
    if cv2.waitKey(0) & 0xff == ord('q'):
      break
  cv2.destroyAllWindows()
if __name__ == '__main__':
  main()
