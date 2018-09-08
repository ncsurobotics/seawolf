import missions


missionType = type(type)
env = {k:v for (k, v) in missions.__dict__.items() if type(v) is missionType}

def readFile(confFile):
  f = open(confFile)
  lc = 0
  ms = []
  try:
    while True:
      line = f.readline()
      if not line:
        break
      lc += 1
      line = line.strip()
      
      line = removeComment(line)
      
      #if the line is empty after removing comments continue to next line
      if not line:
        continue
      #excpecting line to just contain name of mission object
      ms.append(evalLine(line.strip()))
  except:
    print "error reading line %d" % (lc)
  finally:
    f.close()
    return ms

COMMENT = '#'
def removeComment(line):
  try:
    return line[0:line.index(COMMENT)]
  except:
    return line

def evalLine(missionName):
  if missionName not in env:
    print "not found"
    raise Exception("Available missions are: " + str(env.keys()))
  return env[missionName]()
  
