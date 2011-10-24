
from base import Entity, Container

class GateEntity(Entity):

    def find(self, robot):
        c = Container()
        c.left_pole = -1
        c.right_pole = 100
        return c
