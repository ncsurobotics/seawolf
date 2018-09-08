Every file in this folder should be a VisionEntity Object.
A VisionEntity consists of the following:
  keys: the keys from the visObj
  processFrame(frame):
                       function processes input 3 channel np array image
                       function returns a visObj  to be used by the calling mission
  debugFrame(name, frame): mehtod is wrapper for cv2.imshow(name, frame)
                       the idea is that it can easily be changed if we don't want debug info
 
New entities need to be added to the __init__.py function then  added to the VisionEntities dictionary. The VisionEntities dictionary makes the test.py function in the directory above work well. 


