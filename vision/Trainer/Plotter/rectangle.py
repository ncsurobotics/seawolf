import cv2

# thickness of center point in rectangle
CENTER_RAD = 5

class Rectangle(object):
  def __init__(self, x, y, w, h, color=(0,255,0)):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.color = color
  def setColor(self, color):
    self.color = color
  def draw(self, img):
    cv2.rectangle(img, (int(self.x), int(self.y)), (int(self.x + self.w), int(self.y + self.h)), self.color, thickness=3, lineType=8, shift=0)
    cv2.rectangle(img, (int(self.x + self.w/2 - CENTER_RAD/2), int(self.y + self.h / 2 - CENTER_RAD/2)), (int(self.x + self.w / 2 + CENTER_RAD / 2), int(self.y + self.h / 2 + CENTER_RAD/2)), self.color, thickness=3, lineType=8, shift=0)
