class GatePole(object):
  """
  This is a class for keeping track of the poles for the gate
  """
  
  def __init__(self, p1, p2):
    """
    p1 and p2 are points
    points are the tuple (x, y)
    """
    self.p1 = p1
    self.p2 = p2
    
  
  def getX(self):
    """
    poles are assumed to go up and down
    therefore the x value should tell us where they are on the page
    """
    return (p1[0] + p2[0])/2
