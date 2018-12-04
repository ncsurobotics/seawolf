from triangle import Triangle
import cv2
import math

colors = {
          'red'      : (0,0,255),
          'blue'     : (255,0,0),
          'green'    : (0,255,0),
          'white'    : (255,255,255)
}

def dist(x1,y1,x2,y2):
  return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def dirn(x1,y1,x2,y2):
  return math.atan2((y2-y1),(x2-x1))

# different mesh faces can be:

#
##    = left_triangle
###

  #
 ##   = right_triangle
### 

###
###   = rectangle
###

"""
Raise an error at the given line for the given mesh file.
"""
def error(msg, folder, file, line):
  error_msg = "Error in file " + folder + file + " at line: " + str(line) + ", " + msg
  raise ValueError( error_msg )

class Mesh(object):
  #read mesh from file
  def __init__(self, file_name, loc=[0,0,0], scale=[1,1,1], orientation=0, folder=''):
    self.name = file_name.replace('.mesh', '')
    self.orientation = orientation
    f = open(folder+file_name, "r")
    text = f.read()
    lines = text.split('\n')
    self.points = []
    #tuples of ([point idx], color/triangle)
    self.faces = []
    #dictionary of triangle imgs
    self.imgs = dict()

    #figure out where points and faces start
    try:
      point_start = lines.index('points:')
      face_start = lines.index('faces:')
    except ValueError:
      error('Points or Faces incorrectly defined in mesh file: ', folder, file_name, 0)

    #iterate through all lines with faces

    for lineIdx in range(len(lines)):
      line = lines[lineIdx]
      #if the first character is '#' or the line is newline, skip the line
      if len(line) == 0 or line[0] == '#':
        continue
      line = line.split(' ')
      
      #read lines with points
      if lineIdx > point_start and lineIdx < face_start:
        pt = []
        for coord in line:
          pt.append(float(coord))
        self.points.append(pt)
      
      #read lines with faces
      if lineIdx > face_start:
        #check if the face is a color, rectangle, or face
        if line[0] == 'color':
          pts = [int(str_val) for str_val in line[1:len(line) - 1]]
          color_name = line[len(line) - 1]
          if not color_name in colors:
            error("Unknown color: " + color_name, folder, file_name, lineIdx)
          #face should only be 3 or 4 (triangle or rectangle)
          if len(pts) == 3:
            self.faces.append((pts, colors[color_name]))
          elif len(pts) == 4:
            self.faces.append((pts[0:3], colors[color_name]))
            self.faces.append(([pts[2], pts[3], pts[0]], colors[color_name]))
          else:
            error('Incorrect number of points (must be 3 or 4', folder, file_name, lineIdx)
        elif line[0] == 'image':
          #last element in line is image
          img_name = line[len(line) - 1]
          if folder+img_name not in self.imgs:
            img = cv2.imread(folder+img_name, flags=-2)
            if img.__class__.__name__ == 'NoneType':
              error('Image: ' + folder+img_name + " does not exist", folder, file_name, lineIdx)
            self.imgs[folder+img_name] = img
          img = self.imgs[folder+img_name]

          #get image dimensions
          height, width, _ = img.shape

          #check what part of the image to get triangle(s) from and make faces
          if line[len(line) - 2] == 'rectangle':
            pts = [int(str_val) for str_val in line[1:5]]
            left_triangle_points = [ [0,0], [0,height], [width,height] ]
            right_triangle_points = [ [width,height], [width, 0], [0,0] ]
            left_face_points = pts[0:3]
            right_face_points = [ pts[2], pts[3], pts[0] ]
            self.faces.append((left_face_points, Triangle(left_triangle_points, img)))
            self.faces.append((right_face_points, Triangle(right_triangle_points, img)))
          elif line[len(line) - 2] == 'left_triangle':
            pts = [int(str_val) for str_val in line[1:4]]
            triangle_points = [ [0,0], [0,height], [width,height] ]
            face_points = pts[0:3]
            self.faces.append((pts, Triangle(triangle_points, img)))
          elif line[len(line) - 2] == 'right_triangle':
            pts = [int(str_val) for str_val in line[1:4]]
            triangle_points = [ [width,height], [width, 0], [0,0] ]
            self.faces.append((pts, Triangle(triangle_points, img)))
          else:
            error('Incorrectly image triangle/rectangle', folder, file_name, lineIdx)
        
        else:
          error('Incorrectly defined face', folder, file_name, lineIdx)
    #scale
    self.points = [(x*scale[0], y*scale[1], z*scale[2]) for x,y,z in self.points]
    #set the location
    x,y,z = loc
    self.points = [(x+X/2, y+Y/2, z+Z/2 ) for X,Y,Z in self.points]
    pass
  
  def faceTypeAt(self, idx):
    return self.faces[idx][1].__class__.__name__
  
  def center(self):
    center = [0,0,0]
    for point in self.points:
      for i in range(len(point)):
        center[i] += point[i]
    for i in range(len(center)):
        center[i] /= len(self.points)
    return center

  def roll(self, rad):
    #just x and y get rotated
    cx, cy = self.center()[0:2]
    polar = []
    for pt in self.points:
      x, y, z = pt
      mag = dist(cx, cy, x, y)
      head = dirn(cx, cy, x, y)
      polar.append((mag, head + rad))
    for i in range(len(self.points)):
      mag = polar[i][0]
      rad = polar[i][1]
      self.points[i] = [mag * math.cos(rad) + cx, mag * math.sin(rad) + cy, self.points[i][2]]
    pass

  def turn(self, rad):
    #just x and y get rotated
    center = self.center()
    cx, cz = center[0], center[2]
    polar = []
    for pt in self.points:
      x, y, z = pt
      mag = dist(cx, cz, x, z)
      head = dirn(cx, cz, x, z)
      polar.append((mag, head + rad))
    for i in range(len(self.points)):
      mag = polar[i][0]
      rad = polar[i][1]
      self.points[i] = [mag * math.cos(rad) + cx,  self.points[i][1], mag * math.sin(rad) + cz]
    pass
  def move(self, delta):
    for i in range(len(self.points)):
      self.points[i] = (self.points[i][0] + delta[0], self.points[i][1] + delta[1], self.points[i][2] + delta[2])
    #print "moving", self.points
    
"""
For failing a test.
"""
def fail(msg):
  print "TESTS FAILED"
  print msg
  exit()

"""
Run to test the mesh program.
"""
if __name__ == '__main__':


  mesh = Mesh('successful_many_faces.mesh', folder = './test/meshes/')
  
  bad_meshes = ['bad_color.mesh', 'bad_points.mesh', 'unknown_image.mesh']
  for bad_mesh in bad_meshes:
    try:
      mesh = Mesh(bad_mesh, folder = './test/meshes/')
      fail('Made mesh: ' + bad_mesh)
    except ValueError:
      pass


  #print mesh.faces[2][1].srcImg
  """
  cv2.polylines(mesh.faces[2][1].srcImg, mesh.faces[2][1].srcTri2d.astype(int), True, (0,0,255), 2, 16)
  cv2.imshow('source triangle', mesh.faces[2][1].srcImg)
  mesh.roll(math.pi/3.0)
  #print mesh.points
  while True:
    key = cv2.waitKey(20) & 0xFF
    if key == ord('q'):
      break
  cv2.destroyAllWindows()
  """