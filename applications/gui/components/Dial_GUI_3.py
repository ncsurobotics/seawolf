from Graphics_GUI_3 import *
from Conversions_GUI_3 import *

BackgroundDial = 1.3
InnerDial = 1.1

"""
Class for a Dial component. Has both a desired bearing it wants to get to,
and an actual bearing.
"""
class Dial:
    #BackgroundDial = 1.3
    #InnerDial = 1.1
    #textDx = -25
    #textDy = -20
    def __init__(self, x, y, radius, color, title, hubName):
        self.x = x
        self.y = y
        self.radius = radius
        self.desiredBearing = 0
        self.actualBearing = 0
        self.paused = False
        self.color = color
        self.title = title
        self.follow = False
        self.hubName = hubName
        self.change = False

    def drawTitle(self):
        textAt( self.x - 8 * len( self.title ), self.y - 105, self.title, WHITE )

    def draw(self):
        #background
        circle(self.x, self.y, int(self.radius * BackgroundDial), BACKGROUND_COLOR)
        #outer circle main
        circle(self.x, self.y, int(self.radius * InnerDial), GREY)
        #inner circle main
        circle(self.x, self.y, self.radius, WHITE)
        #line read
        line(self.x, self.y, int( self.x - self.radius * math.cos( self.actualBearing ) ), int( self.y + self.radius * math.sin( self.actualBearing ) ), 4, RED )
        #line write
        line(self.x, self.y, int( self.x - self.radius * math.cos( self.desiredBearing) ), int( self.y + self.radius * math.sin( self.desiredBearing ) ), 4, DARK )      
        #outer circle small
        circle( int( self.x - self.radius * math.cos( self.desiredBearing ) ), int( self.y + self.radius * math.sin(self.desiredBearing) ), self.radius/4, DARK )
        #inner circle small
        circle( int( self.x - self.radius * math.cos( self.desiredBearing ) ), int( self.y + self.radius * math.sin(self.desiredBearing) ), self.radius/6, WHITE )
        #clear text
        rect( self.x - 75, self.y - self.radius - 50, 170, 35, BACKGROUND_COLOR)      
        #text write
        textAt( self.x - 75, self.y - self.radius - 20, str( toRealDegrees( int( round( math.degrees( self.desiredBearing ),0 ) ) ) ), WHITE )
        #text read
        textAt( self.x + 25, self.y - self.radius - 20, str( toRealDegrees( int( round( math.degrees( self.actualBearing ), 0 ) ) ) ), RED )
        #clear text paused
        rect( self.x + 8 * len( self.title), self.y - 125, 55, 25, BACKGROUND_COLOR )  
        #text paused
        if self.paused:
            textAt( self.x + 8*len( self.title ), self.y - 105, str( 1.0 ), WHITE )
        else:
            textAt( self.x + 8*len( self.title ), self.y - 105, str( 0.0 ), WHITE )

    def move(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            #if close enough
            if dist(self.x, self.y, x,y) <= self.radius*1.4:
                       self.follow = True
                       self.change = True

        if event == cv2.EVENT_LBUTTONUP:
            if self.follow == True:
                self.change = True
                self.follow = False

        if self.follow == True:
            self.desiredBearing = heading( self.x, self.y , self.x + (self.x - x) / 2, self.y - (self.y - y) / 2)
            self.change = True
        pass
    