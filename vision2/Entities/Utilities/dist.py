import numpy as np


"""
turns the frame into  a gray scale image of distance from input color
input opencv frame, the color you want the distance from
output normalized opencv frame
"""
def dist(frame, color):
  Z = frame.reshape((-1,3))
  color = np.float32(color).reshape((-1, 3))
  dist = Z - color
  dist = dist**2
  dist = sum(np.transpose(dist))
  dist = np.sqrt(dist)
  dist = np.uint8(dist)
  dist = dist.reshape((frame.shape[0:2]))
  return dist





