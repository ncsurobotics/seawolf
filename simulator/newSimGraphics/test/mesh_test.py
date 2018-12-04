from test_util import fail
import sys
sys.path.append('../')
from mesh import Mesh

mesh = Mesh('successful_many_faces.mesh', folder = './meshes/')

bad_meshes = ['bad_color.mesh', 'bad_points.mesh', 'unknown_image.mesh']
for bad_mesh in bad_meshes:
  try:
    mesh = Mesh(bad_mesh, folder = './meshes/')
    fail('Made mesh: ' + bad_mesh)
  except ValueError:
    pass