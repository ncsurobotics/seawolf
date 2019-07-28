from rabbit import Rabbit
import pickle

r = Rabbit()

r.send('db.command', pickle.dumps({'get' : True, 'name' : 'my_var', 'value' : 57}))