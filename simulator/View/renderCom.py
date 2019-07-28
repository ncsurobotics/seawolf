import pickle

class Message:
  def __init__(self, command, data):
    self.command = command
    self.data = data
  
  def serialize(self):
    return pickle.dumps(self.__dict__)

  def fromBytes(serialBytes):
    msg = pickle.loads(serialBytes)
    return Message(msg['command'], msg['data'])
  
  def __str__(self):
    return str(self.__dict__)

  def __repr__(self):
    return self.__str__()

# Carry a list of messages
class Messages:
  def __init__(self, messages):
    self.messages = messages
  def serialize(self):
    objs = []
    for msg in self.messages:
      objs.append(msg.__dict__)
    return pickle.dumps(objs)
  def fromBytes(serialBytes):
    objs = pickle.loads(serialBytes)
    msgs = []
    for obj in objs:
      msgs.append(Message(obj['command'], obj['data']))
    return msgs


# Command table
"""
ROT
POS
ENTITIES
UPDATE_ENTITY
"""