import traceback
import sys
sys.path.append('../simulator')
sys.path.append('../mission_control2')


import SimEntities
import Test.utilities
from Test.missionTest import MissionTest as test

#this is used filter out the entity objects
entityType = type(type)
#getting the entities from the Entity package
env = {k:v for (k,v) in SimEntities.__dict__.items() if type(v) is entityType}
env['test'] = test



import missions
missionType = type(type)
missionTypes = {k:v for (k, v) in missions.__dict__.items() if type(v) is missionType}
env.update(missionTypes)


#getting functions from test utilities that get actual value from hub to compare to expected
testLambdas = {k:v for (k,v) in Test.utilities.__dict__.items() if callable(v)}
#possible colors
colors = {
          'green' : [0, 255, 0],
          'red'   : [0, 0, 255],
          'blue'  : [255, 0, 0],
         }
#variables
variables = {}
variables.update(colors)
variables.update(testLambdas)
#adding mission names to variables
variables.update({k:k for (k, v) in missionTypes.items()})


#reads file line by line 
def readFile(fileName):
  
  try:
    lc = 0
    f = open(fileName, 'r')
    ents = []
    tests = []
    miss = []
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
      #adding parenthesis to line to make it more lisp like and esier to parse recursively
      line = '(' + line + ')'
      tokens = tokenizer(line)
      tree = parser(tokens)
      obj = evalLine(tree)
      if type(obj) is  test:
        tests.append(obj)
      elif type(obj).__name__ in missionTypes:
        miss.append(obj)
      else:
        ents.append(obj)
  except Exception as e:
    print "ERROR parsing: %d" % (lc)
    print e
    traceback.print_exc()
    tokens = 'error'
  finally:
    f.close()
    if tokens == 'error':
      raise Exception('error reading config file')
    else:
      return ents, tests, miss
    
    

#removes comment part from line
COMMENT = '#'
def removeComment(line):
  try:
    return line[0:line.index(COMMENT)]
  except:
    return line

def tokenizer(line):
  """
  breaks line up into tokens
  returns list of tokens
  """
  modify =    [
                (')', ' ) '),
                ('(', ' ( '),
                (',', ' ')
              ]
  for k, v in modify:
    line = line.replace(k, v)
  return line.split()

def parser(tokens):
  if len(tokens) == 0:
    return SyntaxError('Unexpected EOF')
  token = tokens.pop(0)
  if token == '(':
    L = []
    while tokens[0] != ')':
      L.append(parser(tokens))
    tokens.pop(0)
    return L
  elif token == ')':
    raise SyntaxError('unexpected )')
  else:
    return atom(token)


def atom(token):
  """
  try to make everything a number if cant then make it string
  """
  try: return float(token)
  except ValueError:
    return str(token)  
    
def evalLine(tree):
  obj = tree.pop(0)
  args = {}
  while tree:
    key = tree.pop(0)
    val = tree.pop(0)
    if type(val) is str:
      #val might be a color or lambda if it is a string
      val = variables[val]
    if type(val) is list:
      #if val is a list make it a tuple so colors work with cv2
      val = tuple(val)
    args[key] = val
  try:
    return env[obj](**args)
  except:
    print "Available entites are:"
    print possibleEnts()
    raise Exception("Unable to locate entity: " + obj)



def possibleEnts():
  out = ''
  for k, v in env.items():
             out += '------------------\n'
             out += k
             out += '\n'
  return out


      
      
  
  
  
    
  
  

