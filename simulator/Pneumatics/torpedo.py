import seawolf as sw

TORPEDO_SPEED = 1

def fireTorpedo():
  print "Firing torpedo", torpedo
  try:
    sw.var.set('Sim.torpedoVel', TORPEDO_SPEED)
    sw.var.set('Sim.torpedoPitch', sw.var.get('SEA.Pitch'))
    sw.var.set('Sim.torpedoYaw', sw.var.get('SEA.Yaw'))
    sw.var.set('Sim.xTorpedo', sw.var.get('Sim.xLoc'))
    sw.var.set('Sim.yTorpedo', sw.var.get('Sim.yLoc'))
    sw.var.set('Sim.zTorpedo', sw.var.get('Sim.zLoc'))
    sw.var.set('Sim.torpedoVel', TORPEDO_SPEED)
  except Exception as e:
    for i in range(100):
      print e
  import time
  #time.sleep(300)

def moveTorpedo():
  print "moving torpedo"
  torpedo.update()

class Torpedo(object):
  def __init__(self, loc=[0,0,0], dire=0, vel=0):
    self.loc = loc
    self.dire = dire
    self.vel = vel
    sw.loadConfig("../conf/seawolf.conf")
    sw.init("Simulator : Pneumatics")
  def fire(self, dire, vel):
    pass
  def update(self):
    sw.var.set('Sim.xTorpedo', sw.var.get('Sim.xTorpedo') + TORPEDO_SPEED)
    print "Torpedo update"
    print sw.var.get('Sim.xTorpedo')

torpedo = Torpedo()