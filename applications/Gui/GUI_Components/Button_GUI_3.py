from Graphics_GUI_3 import *
from Conversions_GUI_3 import *

global BorderWidth
BorderWidth = 10

"""
Button that stays on as long as the mouse button.
Off when the mouse button is. Not a toggle button.
More like a springy button. Or a keyboard key.
"""
class Button:
    def __init__( self, x, y, width, length ):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.pressed = False
        self.change = False
        pass

    def drawTitle(self):
        pass

    def draw(self):
        if(self.pressed):
            color = GREEN
            msg = "Pausing"
        else:
            color = LIGHT_GREY
            msg = "Pause"

        rect(self.x - BorderWidth, self.y - BorderWidth, self.width + 2 * BorderWidth, self.length + 2 * BorderWidth, GREY )
        rect(self.x, self.y, self.width, self.length, color)
        textAt(self.x, self.y + 30, msg, DARK_GREY)
        pass

    def move(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN and not self.pressed:
            if isOnSlider(x, y, self.x, self.y, self.width, self.length):
                self.pressed = True
                self.change = True
        if event == cv2.EVENT_LBUTTONUP:
            self.pressed = False
            self.change = True                
        pass
