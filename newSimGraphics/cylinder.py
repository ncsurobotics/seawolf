import math
class Cylinder:
    circle = []:
    quality = 20
    for i in range(quality):
      circle.append([])
    vertices = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    #faces = (0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)
    faces = (0,1,2),(5,6,7)
    colors = (255,0,0),(255,128,0),(255,255,0), (0,0,0) ,(0,0,255),(0,255,0)       
    def __init__(self, pos=(0,0,0)):
        x,y,z = pos
        self.verts = [(x+X/2, y+Y/2, z+Z/2 ) for X,Y,Z in self.vertices]