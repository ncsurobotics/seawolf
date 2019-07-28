from rabbit import Rabbit

r = Rabbit()

r.create_queue('sim.view')
r.create_queue('sim.render')
r.create_queue('db.command')
