import sys
import numpy as np
import cv2
import time
import Entities
from Entities.Utilities import debugFrame
import copy


"""
keys:

q to quit
[ to skip back
] to skip forward
r to restart

skip skips 100 frames 
"""

skip = 100

def error(message):
  print "ERROR: %s" % message
  sys.exit(1)

def writeHeader(outputFile, header):
  line = 'frame, time'
  for word in header:
    line = line + ", " + word
  line = line + "\n"
  outputFile.write(line)
  
def writeOutput(outputFile, count, time, header, output):
  line = str(count) + ", " + str(time)
  for key in header:
    a = str(output[key])
    line = line + ", " + a
  line = line  + "\n"
  outputFile.write(line)
  
def main():
  
  if len(sys.argv) != 4 and len(sys.argv) != 5:
    error('usage: Entity inputFile outPutfile [scale]\n(for webcam, set inputfile to cam) ')
  if (sys.argv[1] not in Entities.VisEntities):
    errMsg = "Invalied Entity\nPossibleEntiies are:\n"
    for key in Entities.VisEntities:
      errMsg+= "\t" + key + "\n"
    error(errMsg)
  vision = Entities.VisEntities[sys.argv[1]]
  inputFile = sys.argv[2]
  outputFile = open(sys.argv[3], 'w')
  fileLine = "inputFile, %s, " % (inputFile)
  entityLine = "entity, %s, " % (sys.argv[1])
  visObjLine = "visObj, %s, " % (vision.visObj)
  #this line lest test program now its no longer getting config lines
  outputFile.write("configLine, " + fileLine + entityLine + visObjLine + "\n") 
  header = vision.keys
  writeHeader(outputFile, header)
  count = 0
  #if inputFile is cam, then we are streaming from the webcam
  #calling cv2.VideoCapture(0) opens up webcam
  if inputFile == "cam":
    inputFile = 0
  cap = cv2.VideoCapture(inputFile)
  if (not cap.isOpened()):
    error("cannot open file %s" % inputFile)
  scaled = False
  if len(sys.argv) == 5:
    scaled = True
    scale = float(sys.argv[4])
  else:
    scale = 1
  a, frame = cap.read()
  height, width, _ = frame.shape
  height = int(scale * height)
  width = int(scale * width)

  frame_idx = 0

  while(True):
    key = cv2.waitKey(10) & 0xFF

    # quit
    if key == ord('q'):
      break
    
    # rewind
    if key == ord('['):
      cap.release()
      cap = cv2.VideoCapture(inputFile)
      for i in range(max(frame_idx - skip, 0)):
        a, frame = cap.read()
        if not a:
          break
      frame_idx -= skip

    # skip forward
    if key == ord(']'):
      for i in range(skip):
        a, frame = cap.read()
        frame_idx += 1
        if not a:
          break
      frame_idx += 1
    
    # restart
    if key == ord('r'):
      cap.release()
      cap = cv2.VideoCapture(inputFile)
      frame_idx = 0
    
    
    if not a:
      break
    
    a, frame = cap.read()
    frame_idx += 1

    
    frame = cv2.resize(frame, (width, height))
    debugFrame("original", frame)
    t = time.time()
    output = vision.ProcessFrame(frame)
    count += 1
    t = time.time() - t
    writeOutput(outputFile, count, t, header, output.dict())
  outputFile.close()
  cv2.destroyAllWindows()
  cap.release()
    

  

if __name__ == '__main__':
  main()
