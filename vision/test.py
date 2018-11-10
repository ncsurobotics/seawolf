import sys
import numpy as np
import cv2
import time
import Entities


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
    errMsg = "Invalied Entity\nPosiibleEntiies are:\n"
    for key in Entities.VisEntities:
      errMsg+= "\t" + key + "\n"
    error(errMsg)
  print("hell")
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
  while(1):
      if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    
      a, frame = cap.read()
      frame = cv2.resize(frame, (width, height))
      if not a:
        break
      cv2.imshow("original", frame)
      t = time.time()
      output = vision.ProcessFrame(frame)
      count += 1
      t = time.time() - t
      writeOutput(outputFile, count, t, header, output.dict())
      '''if (t < .1):
        time.sleep(.1 - t)'''
      
  outputFile.close()
  cv2.destroyAllWindows()
  cap.release()
    

  

if __name__ == '__main__':
  main()
