# import cv2
# import numpy as cv

# img = cv2.imread('fly.png',0)

# # Create SURF object. You can specify params here or later.
# # Here I set Hessian Threshold to 400
# surf = cv2.SURF(400)

# # Find keypoints and descriptors directly
# kp, des = surf.detectAndCompute(img,None)

# print len(kp)

# # Check present Hessian threshold
# print surf.hessianThreshold

# # We set it to some 50000. Remember, it is just for representing in picture.
# # In actual cases, it is better to have a value 300-500
# surf.hessianThreshold = 50000

# # Again compute keypoints and check its number.
# kp, des = surf.detectAndCompute(img,None)

# print len(kp)

# img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)
# plt.imshow(img2),plt.show()

# # Check upright flag, if it False, set it to True
# print surf.upright

# surf.upright = True

# # Recompute the feature points and draw it
# kp = surf.detect(img,None)
# img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)

# plt.imshow(img2),plt.show()

### ORB ###

import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('aliens.png',0)          # queryImage
img2 = cv2.imread('alien-1-1.png',0) # trainImage

# Initiate SIFT detector
orb = cv2.ORB()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], flags=2)

plt.imshow(img3),plt.show()
