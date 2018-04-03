import seawolf as sw
def yaw():
  return sw.var.get("SEA.Yaw")

def location():
  return [ sw.var.get('Sim.xLoc'),
           sw.var.get('Sim.yLoc'),
           sw.var.get('Sim.zLoc'),
         ]
  
