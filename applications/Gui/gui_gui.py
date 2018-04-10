from gui_textbox import *
class GUI:
    #global BACKGROUND_COLOR
    BACKGROUND_COLOR = (0,0,0)
    class __GUI:
        
        def __init__(self):
            self.components = []
    instance = None
    
    def __init__(self):
        if not GUI.instance:
            GUI.instance = GUI.__GUI()
        
    def handleMouseEvent(self, event, x, y, flags, param):
        for comp in self.instance.components:
            comp.handleMouseEvent(x,y,event)

    def drawComponents(self):
        for c in self.instance.components:
            c.draw()

    def addComponent(self, c):
        self.instance.components.append(c)
    def modifySelectedTextBox(self, k):
        for c in self.instance.components:
            if isinstance(c, TextBox) and c.selected:
                c.modifyText(k)
                return
"""
#Components
    ROLL = 0
    PITCH = 1
    YAW = 2
    DEPTH = 3
    DEPTH_READER = 4
    FORWARD = 5
    BOW = 6
    STERN = 7
    PORT = 8
    STAR = 9
    STRAFET = 10
    STRAFEB = 11
    PLAY_BUTTON = 12
"""