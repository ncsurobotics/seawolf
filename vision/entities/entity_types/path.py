from base_object import BaseObject

class Path(BaseObject):
    def __init__(self, arg1, arg2):
        self.loc = arg1
        self.angle = arg2
        self.theta = arg2
        self.id = 0
        self.last_seen = 2
        self.seencount = 1
