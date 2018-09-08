"""
Vision Objects
all objects to be found by mission should be implemented as a vision object
a vison object implements three methods:
		draw(frame) -> draws the object onto the input frame and retuns the modified frame
		keys -> returns the self.keys for output dict
		dict() -> returns self.out a dictionary containing important values
"""
class VisObj(object):
  
  """
  draws the obj onto the input cv2/numpy frame
  frame = cv2/numpy rgb frame
  output = input frame with vision object drawn on to it
  """
  def draw(self, frame):
    Exception("draw(frame) method not implemented")
  
  def dict(self):
    if (self.out != None):
      return self.out
    
    Exception("self.out not defined")
	   
  
  


"""
  returns string of values for csv file of output
	input = nothing
	dict = dictionary with keys from header Keys

  def dict(self):
	  Exception("dict() method not implemented")
"""

