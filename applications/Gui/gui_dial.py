from gui_component import *
from gui_graphics import *

class Dial(Component):
    def __init__(self, x, y, title):
        self.radius = 60
        self.follow = False
        self.desiredBearing = math.pi/4
        self.actualBearing = 0
        self.following = False
        self.title = title
        self.paused = False
        Component.__init__(self, x, y, title)
    def handleMouseEvent(self, x, y, event):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.follow = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.follow = False
        self.move(x,y)
        pass  
    def draw(self):
        circle(self.x, self.y, self.radius, CHROME_BLUE)
        line(self.x, self.y, self.x - self.radius * math.cos(self.actualBearing), self.y + self.radius * math.sin(self.actualBearing), 2, RED )
        line(self.x, self.y, self.x - self.radius * math.cos(self.desiredBearing), self.y + self.radius * math.sin(self.desiredBearing), 2, GREEN )
        textAt(self.x - self.radius/2, self.y - self.radius - 5, self.title, WHITE)
        pass
    #move desired bearing toward (x,y), using special 180 and -180 scale
    def move(self, x, y):
        if isInCircle(self.x, self.y, self.radius, x, y) and self.follow:
            self.desiredBearing = heading(self.x,self.y,self.x + (self.x - x) / 2, self.y - (self.y - y) / 2)
        pass
    def moveReadIndicator(self, degrees):
        pass
       
