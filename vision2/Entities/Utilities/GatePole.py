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
    self.added = 1
    
    
  
  def getX(self):
    """
    poles are assumed to go up and down
    therefore the x value should tell us where they are on the page
    """
    return (self.p1[0] + self.p2[0])/2
  
  def add(self, pole):
    """
    this function averages this pole with another line on the same pole
    done the way it is because cannot reassign tupple so have to remake it 
    """
    self.p1 = ((self.p1[0] * self.added + pole.p1[0])/(self.added + 1), self.p1[1])
    self.p2 = ((self.p2[0] * self.added + pole.p2[0]) /(self.added + 1), self.p2[1])
    self.added += 1
    return 
  
