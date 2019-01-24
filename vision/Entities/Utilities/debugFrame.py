from srv.windows import imshow, wasKilled

"""
Updates the window with the given name to display the frame.
If the window doesn't exist, it is created.
Again specifies
"""
def debugFrame(name, frame, again=False):
  if again or not wasKilled(name):
    imshow(name, frame) 