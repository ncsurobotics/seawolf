import sys
sys.path.append('../intercom')
from rabbit import Rabbit
import ZODB, ZODB.FileStorage
import json as pickle

storage = ZODB.FileStorage.FileStorage('data/hub_db.fs')
db = ZODB.DB(storage)
db_conn = db.open()

def set_var(name, value):
  with db.transaction() as connection:
    return connection.root().setdefault(name, value)

def get_var(name):
  with db.transaction() as connection:
    return connection.root().get(name)

def get_vars():
  with db.transaction() as connection:
    d = {}
    for key in connection.root():
      d[key] = connection.root()[key]
    return d


r = Rabbit()

#program that handles database interactions

# todo, should pass command type (get/set in props headers)
def handle_command(ch, method, props, body):
  # treat body as name : value pair
  command = pickle.loads(body)
  #print('command:', command)
  if 'set' in command:
    set_var(command['name'], command['value'])
    r.reply(props, pickle.dumps({'name' : command['name'], 'value' : command['value']}))
  # treat body as variable name
  elif 'get' in command:
    r.reply(props, pickle.dumps({'value' : get_var(command['name'])}))
    pass
  elif 'get_all' in command:
    r.reply(props, pickle.dumps({'all' : get_vars()}))
    pass
  #print('db', db.get_vars())


r.create_queue('db.command')
r.create_consumer('db.command', handle_command)

r.start_consuming()