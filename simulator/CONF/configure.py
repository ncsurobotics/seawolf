import traceback
import Entities

def readFile(fileName):
  
  try:
    lc = 0
    f = open(fileName, 'r')
    ents = []
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
      entity = evalEnt(tree)
      ents.append(entity)
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
      return ents
    
    

COMMENT = '#'
def removeComment(line):
  try:
    return line[0:line.index('#')]
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
    
  
def evalEnt(tree):
  obj = tree.pop(0)
  args = {}
  while tree:
    key = tree.pop(0)
    val = tree.pop(0)
    if type(val) is not float and type(val) is not list:
      #val must be a color if it is not a number or a list
      val = colors[val]
    if type(val) is list:
      #if val is a list make it a tuple so colors work with cv2
      val = tuple(val)
    args[key] = val
  #try:
  return Entities.__dict__[obj](**args)
  #except:
   # print "Available entites are:"
    #print possibleEnts()
    #raise Exception("Unable to locate entity: " + obj)


colors = {
          'green' : [0, 255, 0],
          'red'   : [0, 0, 255],
          'blue'  : [255, 0, 0],
         }

def possibleEnts():
  out = ''
  for k, v in Entities.__dict__.items():
     if type(v) is type(type):
             out += '------------------\n'
             out += k
             out += '\n'
  return out


      
      
  
  
  
    
  
  

