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
           
      tokens = tokenizer(line)
      entity = parser(tokens)
      if entity:
        entities.append(entity)
        
      
     

      
  except Exception as e:
    print "ERROR parsing: %d" % (lc)
    print e
    traceback.print_exc()
    tokens = 'error'
  finally:
    f.close()
    if tokens == 'error':
      raise Exception('error reading config file')
    
    

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
  #splitting based on white space
  toksTmp = line.split()
  
  #searching for/grouping parenthesis
  i = -1
  tokens = []
  while i < len(toksTmp) - 1:
    i += 1
    tokens.append(toksTmp[i])
    #this will not work for nested parenthesis, but there should not be any in config file
    if '(' in toksTmp[i]:
      par = i
      i += 1
      while ')' not in toksTmp[i]:
        tokens[par] += toksTmp[i]
        i += 1
      tokens[par] += toksTmp[i]
      
  return tokens
      

def parser(tokens):
  try:
    #the first token should be the name of the entity
    obj = tokens[0]
    #the next should be key value pairs
    args = {}
    for i in range(2, len(tokens), step = 2):
      k = tokens[i - 1]
      v = tokens[i]
      try:
        v = toIntList(v)
      args[k] = v
    



def possibleEnts():
  out = ''
  for k, v in Entities.__dict__.items():
     if type(v) is type(type):
             out += '------------------\n'
             out += k
             out += '\n'
  return out

      
      
  
  
  
    
  
  

