class Component:
    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title
        self.change = False
    
    #@abstractmethod
    def handleMouseEvent(self, x, y, event):
        pass
    #@abstractmethod
    def draw(self):
        pass
    def move(self, x, y):
        pass
