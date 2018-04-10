from gui_component import *
from gui_graphics import *

global BACKSPACE
BACKSPACE = 8
class TextBox(Component):
    def __init__(self, x, y, value):
        self.selected = False
        self.value = value
        TextBox.charWidth = 20
        TextBox.charHeight = 30
        Component.__init__(self, x, y, "")
    def draw(self):
        color = GREEN if self.selected else GREY
        rect(self.x, self.y - TextBox.charHeight*.8, len(str(self.value))*TextBox.charWidth, TextBox.charHeight, color)
        
        textAt(self.x, self.y, str(self.value), WHITE)
    def modifyText(self, k):
        if k == BACKSPACE:
            self.value = self.value[:-1]
            if len(self.value) == 0:
                self.value = " "
        elif k == ord('\n'):
            self.selected = False
        elif self.selected:
            if self.value == " ":
                self.value = chr(k)
            else:
                self.value += chr(k)
    def getValue():
        return float(self.value)

    def handleMouseEvent(self, x, y, event):
        if event == cv2.EVENT_LBUTTONDBLCLK and isInRect(self.x, self.y - TextBox.charHeight*.8, len(str(self.value))*TextBox.charWidth, TextBox.charHeight, x, y):
            self.selected = True
        elif event == cv2.EVENT_LBUTTONDOWN and not isInRect(self.x, self.y - TextBox.charHeight*.8, len(str(self.value))*TextBox.charWidth, TextBox.charHeight, x, y):
            self.selected = False
        pass
