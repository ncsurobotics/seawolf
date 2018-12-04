
#3d entity, has coordinates, mesh
class Entity(object):
  def __init__(loc=[0.0,0.0,0.0], mesh):
    self.loc = loc
    self.mesh = mesh
    pass