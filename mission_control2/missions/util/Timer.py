import time

class Timer(object):
  
  
  def __init__(self, timeOut = 0):
    """
    time out is time to run in secconds
    """
    self.timeOut = timeOut
    self.restart()
    
  
  def restart(self):
    self.startTime = time.time()
    
  
  def timeLeft(self):
    return self.timeOut > (time.time() - self.startTime)
  """ For getting remaining time for debugging"""
  def remainingTime(self):
    return (time.time() - self.startTime)