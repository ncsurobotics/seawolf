import seawolf as sw


class Pneumatics(object):
    def __init__(self):
        self.arsenal = [
            self._createDevice('Grabber2','PN',1),
            self._createDevice('Grabber1','PN',2),
            self._createDevice('Torpedo2','PN',3),
            self._createDevice('Torpedo1','PN',4),
            self._createDevice('Dropper2','PN',5),
            self._createDevice('Dropper1','PN',6),
        ]

        self.sel = 1

    def _createDevice(self, name, subsystem, ID):
        device = {'name':name, 'subsystem':subsystem, 'id':ID}
        return device

    def next(self):
        self.sel = (self.sel +1) % len(self.arsenal)

    def prev(self):
        self.sel = (self.sel -1) % len(self.arsenal)

    def printActive(self):
        name =  self.arsenal[self.sel]['name']
        print("currently active device: %s" % name)

    def f(self):
        name =  self.arsenal[self.sel]['name']
        ID = self.arsenal[self.sel]['id']
        subsystem = self.arsenal[self.sel]['subsystem']
        print "attempting to fire f() pneumatics ", ID

        if (subsystem=='PN'):
            cmd = ("PNEUMATICS_REQUEST", "fire %d" % ID)
            sw.notify.send(*cmd) #send notification to seawolf

            #print what just happend
            print("%s %s" % cmd)

    def fire(self, location):
         if location >= 0 and location <= 5 and isinstance(location, int):
            self.sel = location
            self.f()
            print "[Pneumatics] Firing location fire() in pneumatics", self.arsenal[self.sel]['id']

missiles = Pneumatics()
