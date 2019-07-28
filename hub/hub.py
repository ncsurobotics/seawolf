import sys
sys.path.append('../intercom')
from rabbit import Rabbit
from rpcCaller import RpcCaller
import json as pickle

def connect(application_name):
  return Application(application_name)

class Application:
  def __init__(self, name):
    self.name = name
    self.rabbit = Rabbit()
    # for when a message is sent to this app
    self.msg_queue = Application.get_application_msg_queue(name)
    self.rabbit.create_queue(self.msg_queue)
    # for rpc calls, responses go here
    self.resp_queue = Application.get_application_resp_queue(name)
    self.rabbit.create_queue(self.resp_queue)
    # for remote procedure calls
    self.rpc = RpcCaller(self.resp_queue, self.rabbit)

  @staticmethod
  def get_application_msg_queue(application_name):
    return application_name + '.msg'

  @staticmethod
  def get_application_resp_queue(application_name):
    return application_name + '.resp'
  

  def set_var(self, name, value):
    resp_bytes = self.rpc.call('db.command', pickle.dumps({'set' : True, 'name' : name, 'value' : value}))
    return pickle.loads(resp_bytes)

  def get_var(self, name):
    resp_bytes = self.rpc.call('db.command', pickle.dumps({'get' : True, 'name' : name}))
    return pickle.loads(resp_bytes)

  def get_vars(self):
    resp_bytes = self.rpc.call('db.command', pickle.dumps({'get_all' : True}))
    return pickle.loads(resp_bytes)
  
  def notify(self, application_name, msg, serialize=True):
    if serialize:
      msg = pickle.dumps(msg)
    self.rabbit.send(Application.get_application_msg_queue(application_name), msg)
    pass
  
  def receive(self, serialize=True):
    msg = self.rabbit.get(Application.get_application_resp_queue(queue_name))
    if serialize:
      msg = pickle.loads(msg)
    return msg



