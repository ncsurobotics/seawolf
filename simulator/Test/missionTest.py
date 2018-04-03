import numpy as np

class MissionTest(object):
  
  def __init__(self, missionName = 'nameOfMission', actual = None, within = 0, expected = None):
    """
    missionName is the name of the mission test to run this test after
    tests  is the list of test to run after 
    expected is the expeted result
    within is the accepted tolerance to the expected
    actual is a lambda/function to get the desired value
    """
    self.missionName = missionName
    self.expected = expected
    self.actual = actual
    self.within = within
    self.testActual = None
    self.passed = None
  
  def run(self):
    self.testActual = self.actual()
    self.passed =  np.linalg.norm(np.float32(self.testActual) - np.float32(self.expected)) < self.within
    return self.passed
  
  def wasRan(self):
    return not self.passed is None
  
  
      
  def __repr__(self):
    out = "afer %s %s is within %4.2f of %s\n" % (self.missionName, self.actual.__name__, self.within, str(self.expected))
    if self.passed:
      out = "--------------------PASSED----------------\n" + out 
      #this works because self.passed is set to none at initiation 
    elif self.passed is not None:
      out = "--------------------FAILED----------------\n" + out
      out += "actual value was " + str(self.testActual) + "\n"
    else:
      out = "--------------------NOT RAN----------------\n" + out
    out += "--------------------------------------------\n"
    return out
       
