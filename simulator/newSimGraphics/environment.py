#Code used from and based on https://www.youtube.com/watch?v=g4E9iq0BixA
import cv2
import numpy as np
import pygame, sys, math
from cube import Cube
from triangle import Triangle
from mesh import Mesh
from camera import Cam
import srv
from srv.nettools import MailBox
import socket
from timer import Timer

ENGINE_ADDR = ("127.0.0.1", 5105)

def dist(x1,y1,x2,y2):
  return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def rotate2d(pos,rad):
    x,y = pos
    s,c = math.sin(rad),math.cos(rad)
    return x*c-y*s,y*c+x*s

#points where [[cx,cy],[p1x,p1y],[p2x,p2y]] the c points are center
#the other points are 2 other endpoints on section of oval
def drawEllipse(points, color):
    cx,cy = points[0]
    x1,y1 = points[1]
    x2,y2 = points[2]

    #FOR DEBUGGING, delete this
    cv2.circle(frame, (cx,cy), 6, (0,0,255), -1)
    cv2.circle(frame, (x1,y1), 6, (0,255,0), -1)
    cv2.circle(frame, (x2,y2), 6, (255,0,0), -1)


    #get x and y relative to center points
    x1 -= cx
    x2 -= cx
    y1 -= cy
    y2 -= cy

    #calculate
    n = float(x2 ** 2 - x1 ** 2) / ( (x2 ** 2) * (y1 ** 2) - (x1 ** 2) * (y2 ** 2) )
    m = (1 - n * y2 ** 2) / (x2 ** 2)
    a = math.sqrt(1/m)
    b = math.sqrt(1/n)

    #print a, b
    #a = 10
    #b = 10
    s = 1

    endAngle = math.atan2(y2, x2) * 180.0/ math.pi
    startAngle = math.atan2(y1, x1) * 180.0/ math.pi

    #swap end and start angle if gap is too big
    if abs(endAngle-startAngle) > 180:
        temp = endAngle
        endAngle = startAngle
        startAngle = temp
    #-1 thickness means the whole ellipse slice is filled in, convert radians to degrees for angles
    cv2.ellipse(frame, (int(cx),int(cy)), (int(a*s),int(b*s)), 0, startAngle, endAngle, color, thickness=-1)
    return

w,h = 400, 400
cx,cy = w/2, h/2
border = 0#400

cam = Cam((0,0,-5))

STREAMING = False

if STREAMING:
  srv_connection = srv.connection.Connection('NewSimulator')

"""
cubes = [Cube((0,0,0)), Cube((-2,0,0)), Cube((2,0,0))]

for i in range(4):
    for j in range(1):
        cubes.append(Cube((i,0,j)))
"""

meshes = [Mesh('pole-red.mesh', [-2.125,.1,7], [1,3,1], orientation=.2), Mesh('pole-blue.mesh', [1.2,1.3,-4.1], [1,2,1])]
meshes.append(Mesh('wheel.mesh', [-4,.1,6], folder='./entities/wheel/'))
meshes.append(Mesh('dice-1.mesh', [0,0,7], folder='./entities/dice/'))
meshes.append(Mesh('dice-2.mesh', [2.5,0,7], folder='./entities/dice/'))

meshes.append(Mesh('dice-3.mesh', [4,0,7], folder='./entities/dice/'))
meshes.append(Mesh('dice-4.mesh', [0,2,7], folder='./entities/dice/'))
meshes.append(Mesh('dice-5.mesh', [2.5,2,7], folder='./entities/dice/'))

meshes.append(Mesh('dice-6.mesh', [4,2,7], folder='./entities/dice/'))
#meshes.append(Mesh('dice-6.mesh', [2,0,7], folder='./entities/dice/'))

#meshes.append(Mesh('path-bent.mesh', [2.5,2,3], folder='./entities/pathbent/'))



deltas = {
    'pole-red'    : (.01,0,0),
    'pole-blue'   : (-.01,0,0),
    'wheel'       : (0,0,0)
}

key = 0
prev_x, prev_y = None, None
mouseDy = 0
mouseDx = 0

background = (190, 158, 31)


#function to track the movement of the mouse
#expect param to be prev x and prevy
def setMouseDelta(event,x,y,flags,param):
    global prev_x, prev_y, mouseDx, mouseDy
    if prev_x == None:
        prev_x = x
        prev_y = y
    else:
        mouseDx = x - prev_x
        mouseDy = y - prev_y
        prev_x = x
        prev_y = y

cv2.namedWindow('Environment')

cv2.setMouseCallback('Environment', setMouseDelta, [prev_x, prev_y])



#blank frame initially
frame = np.zeros((h,w,3), np.uint8)
frameSize = frame.shape

#inital noise
noise =  np.random.normal(loc = 0, scale = 4, size = frameSize)
#how often noise gets updated
noiseTimer = Timer(.5)

#NULL PARAMS LIES
#triangle = Triangle(0,0,0)
if __name__ == '__main__':
  mailBox = MailBox(ENGINE_ADDR)
  mailBox.sock.settimeout(.001)
  events = dict()
  events['keydown'] = []
  events['mouse'] = []
  events['keyup'] = []
  
  f_factor = 500.0
  while True:
      try:
        newEvents, addr = mailBox.receive()
        events['keydown'].extend(newEvents['keydown'])
        events['mouse'].extend(newEvents['mouse'])
        events['keyup'].extend(newEvents['keyup'])
      except socket.timeout:
          pass

      #print events

      oldKey = key
      key = cv2.waitKey(20) & 0xFF
      #only take in new key presses
      if key == 255:
          key = oldKey
      #set frame to background
      frame[:] = background + noise
      #add noise to frame
      if noiseTimer.timeUp():
        noiseTimer.restart()
        noise =  np.random.normal(loc = 0, scale = 4, size = frameSize)

      #going through all objects, getting all faces
      face_list = []
      face_color = []
      depth = [] # stores all face data
      bounding_boxes = []

      for mesh in meshes:
          mesh.turn(.04)
          #mesh.move(deltas[mesh.name])
          #print mesh.name
          #mesh.roll(.01)
          vert_list = []
          screen_coords = []
          for x,y,z in mesh.points:
              x -= cam.pos[0]
              y -= cam.pos[1]
              z -= cam.pos[2]

              x,z = rotate2d((x,z), cam.rot[1])
              y,z = rotate2d((y,z), cam.rot[0])

              vert_list += [ (x,y,z) ]
              
              f = f_factor * abs(z) ** -1
              #f = f_factor * abs(z) ** -.6
              x, y = x*f, y*f
              screen_coords += [(cx + int(x), cy+int(y))]

          """
          Onscreen asks "are any of the mesh's points on screen?"

          It should ask is any point within the mesh's points on screen?
          """
          #print "+"*50, "mesh"
          on_screen = False
          for f in range(len(mesh.faces)):
              face = mesh.faces[f]
              

              #print " "*10,"-"*50,"face"
              #face[0] has a face's coordinates, face[1] has img/color info
              for i in face[0]:
                  x,y = screen_coords[i]
                  #print x,y
                  if vert_list[i][2] > 0 and x>-border and x<w+border and y >-border and y<h+border:
                      on_screen = True
                      break
              if on_screen:
                  break
          if on_screen:
              for f in range(len(mesh.faces)):
                  face = mesh.faces[f]
                  coords = [screen_coords[i] for i in face[0]]
                  face_list += [coords]
                  face_color += [mesh.faces[f][1]]
                  depth += [sum(sum(vert_list[j][i] for j in face[0])**2 for i in range(3))]
                  """
                  x,y,z = vert_list[face[0][0]]
                  min_z = dist(x,cam.pos[0], z, cam.pos[1])
                  print min_z
                  for i in face[0]:
                      #i is v list idx
                      x,y,z = vert_list[i]
                      d = dist(x,cam.pos[0], z, cam.pos[1])
                      if d < min_z:
                          min_z = d
                      
                  depth += [min_z]
                  """

          #final drawing part
          order = sorted(range(len(face_list)), key=lambda i:depth[i], reverse=1)
          if len(depth) > 0 and depth[0] > .5:
            for i in order:
                try:
                    
                    if face_color[i].__class__.__name__ == 'tuple':
                        #pass
                        cv2.fillPoly(frame, np.array([face_list[i]], np.int32), face_color[i])
                    elif face_color[i].__class__.__name__ == 'Triangle':
                        face_color[i].setDest2d(face_list[i])
                        cv2.fillPoly(frame, np.array([face_list[i]], np.int32), (255,0,0))
                        face_color[i].draw(frame)
                        #drawEllipse(face_list[i], (0,0,0))
                except:
                    pass
                
    
      cv2.imshow("Environment", frame)
      if STREAMING:
        srv_connection.post(frame)

      f_factor += cam.update(events)
      if key == ord('q'):
          break
  cv2.destroyAllWindows()