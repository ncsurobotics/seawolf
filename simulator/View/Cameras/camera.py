#uses code from as the core: https://www.youtube.com/watch?v=g4E9iq0BixA
#adapted for opencv
import cv2
import numpy as np
import pygame, sys, math
from triangle import Triangle
from mesh import Mesh
from timer import Timer
import svr

def dist(x1,y1,x2,y2):
  return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# Magic function used in converting 3d point to 2d
def rotate2d(pos,rad):
    x,y = pos
    s,c = math.sin(rad),math.cos(rad)
    return x*c-y*s,y*c+x*s

# Distance between 2 3d vectors
def dist3d(v1, v2):
    return math.sqrt( (v1[0]- v2[0])**2 + (v1[1]- v2[1])**2 + (v1[2]- v2[2])**2 )

# Find the center of a list of points
def center(pts):
    ptSize = len(pts[0])
    c = [0] * ptSize # makes a list filled with zeros of len ptSize
    for pt in pts:
        for i in range(ptSize):
            c[i] += pt[i]
    for i in range(ptSize):
        c[i] /= ptSize
    return c

# if an object is further away than FADE_DIST, don't draw it
# too far away in water to see
FADE_DIST = 4000

# width and height of window
w,h = 400, 400
# center (x,y) of window
cx,cy = w/2, h/2

# zoom/scale factor used when rendering the objects
f_factor = 500.0

# blue background of the sea
background = (190, 158, 31)

"""
Camera has:

name
pos
rot
rot_offset
frame
frameSize
noise
noiseTimer
"""
class Cam:
    def __init__(self, name, pos=(0,0,0), rot_offset=(0,0), rot=(0,0)):
        self.name = name
        self.pos = list(pos)
        self.rot = list(rot)
        self.rot_offset = list(rot_offset)
        self.states = dict()

        #blank frame initially
        self.frame = np.zeros((h,w,3), np.uint8)
        self.frameSize = self.frame.shape

        #inital noise
        self.noise =  np.random.normal(loc = 0, scale = 4, size = self.frameSize)
        #how often noise gets updated
        self.noiseTimer = Timer(.5)

        for c in "wasd .lp;'f":
            self.states[c] = False

    def draw(self, meshes):
        #set frame to background
        self.frame[:] = background + self.noise
        #add noise to frame, new noise generated when the timer goes off
        if self.noiseTimer.timeUp():
            self.noiseTimer.restart()
            self.noise =  np.random.normal(loc = 0, scale = 4, size = self.frameSize)
        
        """
        Lists used when drawing the mesh objects in space.
        """
        face_coord_list = [] # list of the 2d coordinates that define each face
        faces = [] # stores each face being drawn
        depth = [] # stores face depth data

        """
        Iterate through all meshes, figure out how to convert them to 2d space.
        """
        for mesh in meshes:
            """
            Make lists for recording the 3d and 2d coordinates of the points in the mesh.
            """
            vert_list = [] # holds the 3d coordinates of each point in the mesh
            screen_coords = [] # holds the onscreen 2d coordinates of each point in the mesh

            """
            Record 2d and 3d points, turn 3d vert_list into 2d screen_coords.
            """
            for x,y,z in mesh.points:
                x -= self.pos[0]
                y -= self.pos[1]
                z -= self.pos[2]

                x,z = rotate2d((x,z), self.rot[1] + self.rot_offset[1])
                y,z = rotate2d((y,z), self.rot[0] + self.rot_offset[0])

                vert_list += [ (x,y,z) ]

                f = f_factor * abs(z) ** -1
                #f = f_factor * abs(z) ** -.6
                x, y = x*f, y*f
                screen_coords += [(cx + int(x), cy+int(y))]

            """
            Onscreen asks "are any of the mesh's points on screen?"
            It should ask is any point within the mesh's points on screen?

            Goal to make sure that the face being drawn is on screen.
            """
            on_screen = False
            for f in range(len(mesh.faces)):
                face = mesh.faces[f]
                for i in face.points:
                    x,y = screen_coords[i]
                    if vert_list[i][2] > 0 and x>0 and x<w and y >0 and y<h:
                        on_screen = True
                        break
                if on_screen:
                    break
           
            """
            Draw the mesh if it is on screen.
            """
            if on_screen:
                for f in range(len(mesh.faces)):
                    face = mesh.faces[f]
                    coords = [screen_coords[i] for i in face.points]
                    verts = [vert_list[i] for i in face.points]
                    face_coord_list += [coords]
                    faces += [mesh.faces[f]]
                    depth+=[sum(sum(vert_list[j][i]/len(face.points) for j in face.points)**2 for i in range(3))]

            """
            Order the faces so that the ones furthest away are drawn first, then the closer ones.
            This makes sure that the closest faces are what the viewer sees.
            """
            order = sorted(range(len(face_coord_list)), key=lambda i:depth[i], reverse=1)
            for i in order:
                if depth[i] > .05 and depth[i] < FADE_DIST:
                    try:
                        # face is drawn onto the frame
                        faces[i].draw(face_coord_list[i], self.frame)
                    except:
                        pass
                
    def yaw(self, rad):
        self.rot[1] += rad
    def pitch(self, rad):
        self.rot[0] += rad

    def update(self, events):
        #print self.states['w']
        if len(events['keyup']) > 0:
            self.states[chr(events['keyup'].pop(0))] = False
        if len(events['keydown']) > 0:
            self.states[chr(events['keydown'].pop(0))] = True
        s = .1
        if self.states[' ']:
            self.pos[1]+=s
        if self.states['.']:
            self.pos[1]-=s

        x,y = s * math.sin(self.rot[1] + self.rot_offset[1]), s*math.cos(self.rot[1] + self.rot_offset[1])

        if self.states['w']:
            #print "W"
            self.pos[0] += x; self.pos[2] += y
        if self.states['s']:
            self.pos[0] -= x; self.pos[2] -= y
        if self.states['a']:
            self.pos[0] -= y; self.pos[2] += x
        if self.states['d']:
            self.pos[0] += y; self.pos[2] -= x
        
        s = 5
        x = 0
        y = 0
        if self.states['l']:
            x = -1
        if self.states["'"]:
            x = 1
        if self.states['p']:
            y = -1
        if self.states[';']:
            y = 1
        
        x /= 200.0
        y /= 200.0

        self.rot[0] += y * s
        self.rot[1] += x * s

        if self.states['f']:
            return 1
        return 0


    #displays frame on svr
    def show(self):
        container = cv2.cv.fromarray(np.copy(self.frame))
        cv_image = cv2.cv.GetImage(container)
        svr.debug(self.name, cv_image)