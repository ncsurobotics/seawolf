from Graphics_GUI_3 import *
from Conversions_GUI_3 import *

#constants
Horizontal = 0
Vertical = 1
BorderWidth = 10

"""
Class for a slider component. Sliders can be disabled so that they are read only,
but generally they are moveable.
"""
class Slider:
    def __init__(self, x, y, width, length, maxR, minR, barType, mapUp, mapDown, enabled, title, hubName):
        self.slide = 0
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.max = maxR
        self.min = minR
        self.barType = barType
        self.title = title
        self.mapUp = mapUp
        self.mapDown = mapDown
        self.enabled = enabled
        self.hubName = hubName
        self.paused = False
        self.change = False
        self.follow = False
        pass

    def drawTitle(self):
        if self.barType == Vertical:
            textAt( self.x - 25, self.y - 40, self.title, WHITE )
        if self.barType == Horizontal:
            textAt( self.x, self.y - 50, self.title, WHITE )
        pass

    def draw(self):
        sliding_bar_color = RED
        
        if self.enabled:
            #background
            rect( self.x - BorderWidth, self.y - BorderWidth, self.width + BorderWidth * 2, self.length + BorderWidth * 2, BACKGROUND_COLOR)
            #outer mid rect
            rect( self.x, self.y, self.width, self.length, GREY)
            #inner mid rect
            rect(self.x + BorderWidth / 2, self.y + BorderWidth / 2, self.width - BorderWidth, self.length - BorderWidth, WHITE)
            sliding_bar_color = LIGHT_GREY

        #slider
            
        #outer
        
        if self.barType == Horizontal:
            rect( self.x + self.slide - 5, self.y, 10, self.length, sliding_bar_color)
        if self.barType == Vertical:
            rect( self.x, self.y +  self.slide - 5, self.width, 10, sliding_bar_color)
     
        #inner
            
        #clear text
        if self.enabled:
            if self.barType == Vertical:
                #clear
                rect( self.x - 70, self.y - 30, 90, 25, BACKGROUND_COLOR)
                #text
                textAt( self.x - 70, self.y - 10, "%.2f" % ( self.slideValue() ), WHITE )
            if self.barType == Horizontal:
                #clear
                rect( self.x, self.y - 40, 90, 30, BACKGROUND_COLOR )
                #text
                textAt( self.x, self.y - 20, "%.2f" % ( self.slideValue() ), WHITE )
        pass

    def move(self,event,x,y,flags,param):
        if not self.enabled:
            return
        if event == cv2.EVENT_LBUTTONDOWN:
            if( isOnSlider( x, y, self.x, self.y, self.width, self.length ) ):
                    self.follow = True
                    self.change = True

        if event == cv2.EVENT_LBUTTONUP:
            if self.follow:
                self.change = 1
                self.follow = False
                    
            
        if self.follow:
            self.change = True
            if self.barType == Horizontal:
                if( x >= self.x and x <= self.x + self.width ):
                    self.slide = x - self.x
            if self.barType == Vertical:
                if( y >= self.y and y <= self.y + self.length ):
                    self.slide = y - self.y
        pass

    """
    Calculates the value that should be displayed on the slider based on where the slider is.
    """
    def slideValue(self):
        if self.barType == Horizontal:
                return mapValTo(self.slide, 0, self.width, self.mapUp, self.mapDown)
        if self.barType == Vertical:
                return mapValTo(self.slide, self.length, 0, self.mapUp, self.mapDown)

    """
    Sets the slider to be at a specific point on the scale.
    """
    def setSlideValue(self, val):
        if self.mapDown - self.mapDown * .1 >= val and val >= self.mapUp * 1.1:
            if self.barType == Vertical:
                self.slide = ( -(self.length / (self.mapDown - self.mapUp ) ) * ( val - self.mapUp ) ) + self.length
            if self.barType == Horizontal:
                self.slide = ( ( self.width / (self.mapDown - self.mapUp ) ) * ( val - self.mapUp ) )

    """
    Sets the slider value for the depth read only slider.
    """
    def setSlideValueForDepthReadOnlySlider( self, val ):
        #bad value
        if (-3.0 <= val and val <= 0.5) == False:
                return 
        #real value
        self.slide = int(round(-42.9 * (val + 3) + 150, 0))