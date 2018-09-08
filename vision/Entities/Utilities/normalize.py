import numpy as np


"""
turns the frame into  a normalized frame
input opencv frame, sf the scaling factor for the brightness of pixels
output normalized opencv frame
"""
def norm(frame, sf = 255):
  Z = np.float32(frame.reshape((-1, 3)))
  C = np.copy(Z)
  Z = Z**2
  #adding .0000001 to avoid divide by 0
  s = np.sqrt(sum(np.transpose(Z)) + .0000001)
  Z = C / s[:, None]
  Z = Z * sf 
  z = np.uint8(Z)
  z = z.reshape((frame.shape))
  return z




