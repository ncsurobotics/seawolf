
from base import Entity, Container

class DoublePathEntity(Entity):

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("DoublePath should not be instantiated. Instead, create two paths in the simulator.")

    @staticmethod
    def find_paths(robot, entities):
        paths = []
        for entity in entities:
            print "Looking at:", entity
            if entity.__class__.__name__ == "PathEntity":

                found, data = entity.find(robot)
                print "  ", found, data
                if found:
                    paths.append(data)

        c = Container()
        c.paths = paths
        return c
