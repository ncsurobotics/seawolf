x = 0
y = 0

# keep track of if the mouse button currently being held
left_mouse_clicked = False
right_mouse_clicked = False
# keep track of is mouse button has newly clicked or not
left_mouse_just_clicked = False
right_mouse_just_clicked = False

MOUSE_LEFT_DOWN = 1
MOUSE_LEFT_UP = 4

MOUSE_RIGHT_DOWN = 2
MOUSE_RIGHT_UP = 5

def mouseEvent(event, new_x, new_y, flags, param):
  global x, y, left_mouse_clicked, right_mouse_clicked, left_mouse_just_clicked, right_mouse_just_clicked
  x = new_x
  y = new_y
  if event == MOUSE_LEFT_DOWN:
    left_mouse_clicked = True
    left_mouse_just_clicked = True
  if event == MOUSE_LEFT_UP:
    left_mouse_clicked = False
    left_mouse_just_clicked = False
  if event == MOUSE_RIGHT_DOWN:
    right_mouse_clicked = True
    right_mouse_just_clicked = True
  if event == MOUSE_RIGHT_UP:
    right_mouse_clicked = False
    right_mouse_just_clicked = False

def getMousePos():
  return x, y

def getLeftMouseClicked():
  return left_mouse_clicked

def getRightMouseClicked():
  return right_mouse_clicked

def getLeftMouseNewlyClicked():
  global left_mouse_just_clicked
  was_newly_clicked = left_mouse_just_clicked
  left_mouse_just_clicked = False
  return was_newly_clicked

def getRightMouseNewlyClicked():
  global right_mouse_just_clicked
  was_newly_clicked = right_mouse_just_clicked
  right_mouse_just_clicked = False
  return was_newly_clicked
