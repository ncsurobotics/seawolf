"""
Pyglet window code adapted from:
https://www.youtube.com/watch?v=Hqg4qePJV2U
"""
from pyglet.gl import *
from pyglet.window import key
import math
from pywavefront import visualization, Wavefront
import array
import numpy as np
import cv2
import io
from threading import Thread, Lock
from http.server import BaseHTTPRequestHandler, HTTPServer
from queue import Queue
import renderCom as rc
from bytesMailBox import BytesMailBox
import comAddresses

command_queue = Queue()
screen_shot_queue = Queue()
HOST_NAME = 'localhost'
RENDER_ADDRESS_FILE = 'renderAddress.txt'

def runServer():
  mailBox = BytesMailBox(ip_and_port=comAddresses.RENDER_ADDRESS)
  port = mailBox.getPort()
  ip = mailBox.getIp()
  f = open(RENDER_ADDRESS_FILE, "w")
  f.write(ip + ':' + str(port))
  f.close()
  while True:
    commands = mailBox.receive()[0]
    command_queue.put(commands)
    screen_shot = screen_shot_queue.get()
    mailBox.send(screen_shot, comAddresses.VIEW_ADDRESS)
    pass
  
  print('Started server at ', HOST_NAME, port)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  http.server_close()
  print('Stopped server')


class Material:
  def __init__(self, color=None, image=None):
    self.color = color
    self.image = image
  def setImage(self, image, isColor=False):
    self.image = self.get_tex(image, isColor)

  def get_tex(self, file, isColor=False):
    #bad ref here
    self.img_tex = pyglet.image.load(file)

    #set color here
    if isColor:
      r, g, b = self.color
      self.img_tex.set_data('RGB', 1, bytes([int(r * 255), int(g * 255), int(b * 255)]))

    tex = self.img_tex.texture
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    return pyglet.graphics.TextureGroup(tex)

# prob want to add better mapping image to face
# store face vertex indexes and texture data
class Face:
  def __init__(self, vert_idxs, material):
    self.vert_idxs = vert_idxs
    self.material = material


class Mesh:
  
  """
  Assumes .obj has only 1 .mtl and that the mtl file
  is declared before the uses of materials in the obj file.
  """
  def __init__(self, mesh_file):
    with open(mesh_file) as f:
      lines = f.readlines()

    verts = []
    faces = []

    self.mtl = None
    self.materials = {}

    current_material = None

    for line in lines:
      if line.strip(' ').startswith('v '):
        coords = line.split(' ')[1:4]
        for i in range(len(coords)):
          coords[i] = float(coords[i])
        verts.append(coords)
      elif line.strip(' ').startswith('f '):
        s = line.split(' ')
        s = s[1 : len(s) + 1]
        for i in range(len(s)):
            s[i] = s[i].split('/')
            s[i] = int(s[i][0])
        faces.append(Face(vert_idxs=s, material=self.materials[current_material]))
      elif line.startswith('mtllib'):
        self.materials = self.parseMtl(line.split(' ')[1])
      elif line.startswith('usemtl'):
        current_material = line.split(' ')[1].strip('\n')
    self.faces = faces
    self.verts = verts
    #for m in self.materials:
    #  print(m, '\n\t', self.materials[m].image.texture.width, '\t', self.materials[m].color)
    #exit()
  
  def parseMtl(self, mtl_file):
    self.mtl = mtl_file.strip('\n')
    materials = {}

    materials['BlankMaterial'] = Material()
    materials['BlankMaterial'].color = [0,0,0]
    materials['BlankMaterial'].setImage('white_pixel.png', isColor=True)

    with open(self.mtl) as f:
      lines = f.readlines()
    current_material = None
    for line in lines:
      if line.startswith('newmtl'):
        current_material = line.split(' ')[1].strip('\n')
        materials[current_material] = Material()
      elif line.startswith('Kd'):
        colors = line.split(' ')[1:4]
        for i in range(len(colors)):
          colors[i] = float(colors[i])
        materials[current_material].color = colors
      elif line.startswith('map_Kd'):
        image = line.split(' ')[1].strip('\n')
        materials[current_material].setImage(image)
    for material_name in materials:
        if materials[material_name].image == None:
          materials[material_name].setImage('white_pixel.png', isColor=True)
          
    return materials

class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self, loc=[0,0,0]):
        self.batch = pyglet.graphics.Batch()
        self.mesh = Mesh('slots.obj')

        # maps the texture
        tex_coords_quad = ('t2f',(0,0, 1,0, 1,1, 0,1, ))
        tex_coords_tri = ('t2f',(0,0, 1,0, 1,1, ))
        

        x,y,z = loc
        X,Y,Z = x+1,y+1,z+1

        # these are faces, inside are the vertices
        for face in self.mesh.faces:
            vertices = []
            for vert_idx in face.vert_idxs:
                vertex = self.mesh.verts[vert_idx - 1][::]
                for i in range(len(vertex)):
                    vertex[i] += loc[i]
                for coord in vertex:
                    vertices.append(coord)
            #print(vertices)
            if face.material.image != None:
                if len(face.vert_idxs) == 3:
                    self.batch.add(3, GL_TRIANGLES, face.material.image, ('v3f', vertices), tex_coords_tri)
                elif len(face.vert_idxs) == 4:
                    self.batch.add(4, GL_QUADS, face.material.image, ('v3f', vertices), tex_coords_quad)
        self.loc = loc

    def draw(self):
        #self.draw_box()
        self.batch.draw()

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self,dx,dy):
        dx/=6; dy/=6; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90: self.rot[0] = 90
        elif self.rot[0]<-90: self.rot[0] = -90
        #print(dx, dy)

    def update(self,dt,keys):
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)
        #print("~~~~", rotY, dx, dz)
        if keys[key.W]:self.pos[0]+=dx; self.pos[2]-=dz
        if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
        if keys[key.A]: self.pos[0]-=dz; self.pos[2]-=dx
        if keys[key.D]: self.pos[0]+=dz; self.pos[2]+=dx

        if keys[key.SPACE]: self.pos[1]+=s
        if keys[key.LSHIFT]: self.pos[1]-=s

class Window(pyglet.window.Window):

    def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2],)
    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
    def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    def set2d(self): self.Projection(); gluOrtho2D(0,self.width,0,self.height); self.Model()
    def set3d(self): self.Projection(); gluPerspective(70,self.width/self.height,0.05,1000); self.Model()

    def setLock(self,state):
      self.lock = state
      self.set_exclusive_mouse(state)
      lock = False
      mouse_lock = property(lambda self:self.lock,setLock)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.models = []
        for i in range(1):
            for j in range(1):
                self.models.append(Model(loc=[j,0,-i]))
        self.player = Player((0.5,1.5,1.5),(-30,0))
        self.set_visible(True)

    def on_mouse_motion(self,x,y,dx,dy):
      #print('x')
      global lock
      if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self,KEY,MOD):
        global lock
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock

    def update(self,dt):
        self.player.update(dt,self.keys)
        # handle commands to update the environment
        self.handle_commands()
        # send out a screenshot of the environment
        self.update_screenshot()

    def update_screenshot(self):
        # only have 1 screenshot in the queue at once (don't overfill when no subscribers)
        if screen_shot_queue.qsize() < 1:
          screen_shot = pyglet.image.get_buffer_manager().get_color_buffer()
          dummy_file = io.BytesIO()
          screen_shot.save('.png', file=dummy_file)
          dummy_file.seek(0)
          screen_shot_queue.put(dummy_file.getvalue())

    def on_draw(self):
        global lock
        #print('draw')
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        for model in self.models:
            model.draw()
        glPopMatrix()

    def handle_commands(self):
      if command_queue.qsize() > 0:
        msg_bytes = command_queue.get()
        print('msg is', msg_bytes)
        msg = rc.Message.fromBytes(msg_bytes)
        print("GOT MESSAGE", msg)
        if msg.command == 'ROT':
          self.player.rot = msg.data
        if msg.command == 'LOC':
          self.player.lloc = msg.data

if __name__ == '__main__':
    window = Window(width=854,height=480,caption='Render',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    Thread(target=runServer).start()
    pyglet.app.run()



