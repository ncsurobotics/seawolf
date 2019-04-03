import seawolf as sw

def fireTorpedo():
  print "Firing torpedo", torpedo

class Torpedo(Object):
  def __init__(self, loc=[0,0,0], dire=0, vel=0):
    self.loc = loc
    self.dire = dire
    self.vel = vel
  def fire(self, dire, vel):
    pass
  def update(self):
    sw.var.set('Sim.xTorpedo', self.loc[0])
    print "Torpedo update"

torpedo = Torpedo()