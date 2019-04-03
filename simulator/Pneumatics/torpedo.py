import seawolf as sw

def fireTorpedo():
  print "Firing torpedo", torpedo
  print sw.var.get
  #import time
  #time.sleep(20)
  #print sw.var.get('Sim.xTorpedo')
  #sw.var.set('Sim.xLoc', 10)

class Torpedo(object):
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