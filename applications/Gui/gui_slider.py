from gui_component import *
from gui_graphics import *
from gui_textbox import *
from gui_gui import *

class  Slider(Component):
    def __init__(self, x, y, width, length, min, max, title):
        self.width = width
        self.length = length
        self.min = min
        self.max = max
        self.title = title
        self.slide = 0
        self.follow = False
        Component.__init__(self, x, y, title)
    def draw(self):
        rect(self.x, self.y, self.width, self.length, CHROME_BLUE)
        pass
    def handleMouseEvent(self, x, y, event):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.follow = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.follow = False
        pass

class VerticalSlider(Slider):
    def __init__(self, x, y, width, length, min, max, title):
        Slider.__init__(self, x, y, width, length, min, max, title)
    #move slider horizontally
    def move(self, x, y):
        if isInRect(self.x, self.y, self.width, self.length, x, y) and self.follow:
            self.slide = y - self.y
        pass
    def draw(self):
        Slider.draw(self)
        rect(self.x, self.y + self.slide, self.width, 10, GREEN)
        textAt(self.x, self.y - 5, self.title, WHITE)
        pass
    def handleMouseEvent(self, x, y, event):
        Slider.handleMouseEvent(self, x, y, event)
        self.move(x, y)
        print(self.title)

class HorizontalSlider(Slider):
    def __init__(self, x, y, width, length, min, max, title):
        self.textBox = TextBox(x, y - 5, "0")
        GUI().addComponent(self.textBox)
        Slider.__init__(self, x, y, width, length, min, max, title)
        
    #move slider horizontally
    def move(self, x, y):
        if isInRect(self.x, self.y, self.width, self.length, x, y) and self.follow:
            self.slide = x - self.x
        pass
    def draw(self):
        Slider.draw(self)
        rect(self.x + self.slide, self.y, 10, self.length, GREY)
        textAt(self.x, self.y - 35, self.title, WHITE)
        pass
    def handleMouseEvent(self, x, y, event):
        Slider.handleMouseEvent(self, x, y, event)
        self.move(x, y)
        print(self.title)
    """
    def setSlideValue(self, i, val):
            if self.mapDown[i] - self.mapDown[i]*.1 >= val and val >= self.mapUp[i] * 1.1:
                    if self.barType[i] == 1:#vertical
                            self.slide[i] = int(round((-(self.length[i]/(self.mapDown[i] - self.mapUp[i])) * (val - self.mapUp[i])) + self.length[i],0))
                    if self.barType[i] == 0:#horiz
                            self.slide[i] = int(round(((self.width[i]/(self.mapDown[i] - self.mapUp[i])) * (val - self.mapUp[i])),0))
    def slideValue(self,i):
        if self.barType[i] == 0: #horiz
                return mapValTo(self.slide[i], 0, self.width[i], self.mapUp[i], self.mapDown[i])
        if self.barType[i] == 1: #vertical
                return mapValTo(self.slide[i], self.length[i], 0, self.mapUp[i], self.mapDown[i])
    """
