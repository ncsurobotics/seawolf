import cv2
import math
import numpy as np

def dist(pt1, pt2):
  d = 0.0
  for i in range(len(pt1)):
    d += (pt2[i] - pt1[i])**2
  return math.sqrt(d)

#pt a - b
def dif(a, b):
  d = []
  for i in range(len(a)):
    d.append(a[i] - b[i])

class Cube:
    vertices = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    #faces should be triangles?
    faces = (0,1,2),(4,5,6)
    baseTriangles = []
    for face in faces:
      origin = vertices[face[0]]
      a = vertices[face[1]]
      b = vertices[face[2]]
      
      dist_oa = dist(origin, a)
      dist_ob = dist(origin, b)
      dist_ab = dist(a, b)
      bx = (-dist_ab + dist_oa**2 + dist_ob**2)/(2*dist_oa)
      by = math.sqrt(dist_ob**2 - bx**2)
      triangle = np.float32([[[0,0], [dist_oa,0], [bx, by]]])
      triangleCropped = []
      bounding_box = cv2.boundingRect(triangle)
      triangleCropped = []
      for i in range(0, 3):
        triangleCropped.append(((triangle[0][i][0] - bounding_box[0]),(triangle[0][i][1] - bounding_box[1])))
      
      
    #faces = (0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)
    colors = (255,0,0),(255,128,0),(255,255,0), (0,0,0) ,(0,0,255),(0,255,0)
    face_img = cv2.imread("new profile.png")   
    def __init__(self, pos=(0,0,0)):
        x,y,z = pos
        self.verts = [(x+X/2, y+Y/2, z+Z/2 ) for X,Y,Z in self.vertices]