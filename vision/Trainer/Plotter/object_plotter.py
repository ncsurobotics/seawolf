"""
Run through a video and draw boxes over significant objects.
Records box positions.

To make a new box, hit 'n'.
To select a box, click on it (it will turn red).
To delete a box, hit 'k'.
To pause/unpause, hit the space bar.
"""
import numpy as np
import cv2
from key import getKeyPress
from mouse import mouseEvent, getMousePos, getLeftMouseClicked, getLeftMouseNewlyClicked
from util import dist
from rectangle import Rectangle
import sys

# constants
DEFAULT_RECT_WIDTH = 50
DEFAULT_RECT_HEIGHT = 50
MAX_CORNER_DIST = 20

if len(sys.argv) != 2:
  print "Error:"
  print "Usage: python object_plotter.py videoFilePath > outFile"
  exit()
videoFileName = sys.argv[1]

windowName = 'Object Plotter'

cv2.namedWindow(windowName)

cap = cv2.VideoCapture(videoFileName)

cv2.setMouseCallback(windowName, mouseEvent)

# List of the rectangles in the image
rectangles = []

# the current frame's number
frame_idx = 0

# the currently selected rectangle
selected_rect = None

# the curently selected corner and its idx
selected_corner = None

# whether the video is paused or not
paused = False

# initial frame
if cap.isOpened():
  ret, frame = cap.read()
  prev_frame = frame.copy()

def drawRectangles(img, rectangles):
  for r in rectangles:
    r.draw(img)

# return the index of the first rectangle that x,y is inside of
# if not found, return -1
def whichRectMouseIn(rectangles, x, y):
  for i in range(len(rectangles)):
    r = rectangles[i]
    if x >= r.x and x <= r.x + r.w and y >= r.y and y <= r.y + r.h:
      return i
  return -1

# corner_idx = 0, 1, 2, 3, 4 for left top, right top, left bottom, right bottom corners, center
# find the corner closest to x,y of all the rectangles
# return (rectangle, corner_idx)
def closestCorner(rectangles, x, y):
  corner_idx = -1
  closest_rect = None
  min_dist = None
  for r in rectangles:
    # top left corner
    if min_dist == None or dist(x,y,r.x,r.y) <= min_dist:
      min_dist = dist(x,y,r.x,r.y)
      closest_rect = r
      corner_idx = 0
    # top right corner
    if min_dist == None or dist(x, y, r.x + r.w, r.y) <= min_dist:
      min_dist = dist(x, y, r.x + r.w, r.y)
      closest_rect = r
      corner_idx = 1
    # bottom left corner
    if min_dist == None or dist(x, y, r.x, r.y + r.h) <= min_dist:
      min_dist = dist(x, y, r.x, r.y + r.h)
      closest_rect = r
      corner_idx = 2
    # bottom right corner
    if min_dist == None or dist(x, y, r.x + r.w, r.y + r.h) <= min_dist:
      min_dist = dist(x, y, r.x + r.w, r.y + r.h)
      closest_rect = r
      corner_idx = 3
    # center
    if min_dist == None or dist(x, y, r.x + r.w / 2, r.y + r.h / 2) <= min_dist:
      min_dist = dist(x, y, r.x + r.w / 2, r.y + r.h / 2)
      closest_rect = r
      corner_idx = 4
  if min_dist != None and min_dist <= MAX_CORNER_DIST:
    return (closest_rect, corner_idx)
  # no corner close enough was found
  return None

# if a corner of a rectangle is <= MAX_CORNER_DIST, move it to x, y
def moveCornerTo(r, corner_idx, x, y):
  # top left corner
  if corner_idx == 0:
    r.w += r.x - x
    r.h += r.y - y
    r.x = x
    r.y = y
  # top right corner
  if corner_idx == 1:
    r.w = x - r.x
    r.h += r.y - y
    r.y = y
  # bottom left corner
  if corner_idx == 2:
    r.h = y - r.y
    r.w += r.x - x
    r.x = x
  # bottom right corner
  if corner_idx == 3:
    r.w = x - r.x
    r.h = y - r.y
  # center
  if corner_idx == 4:
    r.x = x - r.w / 2
    r.y = y - r.h / 2
  
  if r.h < 0:
    r.h = 0
  if r.w < 0:
    r.w = 0

def printRectangles(rectangles, frame_idx):
  print frame_idx
  for r in rectangles:
    print r.x, r.y, r.w, r.h

while(cap.isOpened()):

  # Get key press
  key = getKeyPress()

  # toggle paused if the key pressed was space
  if key == ord(' '):
    paused = not paused

  # only play video if not paused
  if not paused:
    # current frame
    ret, frame = cap.read()
    # update previous frame
    if frame.__class__.__name__ != 'NoneType':
      prev_frame = frame.copy()
  else:
    frame = prev_frame.copy()
  
  # make new rectangle
  if key == ord('n'):
    x, y = getMousePos()
    w, h = DEFAULT_RECT_WIDTH, DEFAULT_RECT_HEIGHT
        
    rectangles.append(Rectangle(x, y, w, h))

  # kill current rect
  if key == ord('k'):
    if selected_rect != None:
      rectangles.remove(selected_rect)
      selected_rect = None

  # if user does left click, see if they select rectangle
  if getLeftMouseClicked():
    x, y = getMousePos()
    inner_box_idx = whichRectMouseIn(rectangles, x, y)
    if inner_box_idx != -1:
      # unselect previous selected rect back to green
      if selected_rect != None:
        selected_rect.setColor((0,255,0))
      # select new rect
      selected_rect = rectangles[inner_box_idx]
      selected_rect.setColor((0,0,255))
    
    # if a corner has been selected, drag it
    if selected_corner != None:
      print selected_corner
      r, corner_idx = selected_corner
      moveCornerTo(r, corner_idx, x, y)
  # if the left button isn't down, deselect the corner
  else:
    selected_corner = None
  if getLeftMouseNewlyClicked():
    # look through all corners and see if they are close enough to be dragged
    # then drag them
    selected_corner = closestCorner(rectangles, x, y)

  # draw the rectangles
  drawRectangles(frame, rectangles)

  # record the rectangles for this frame
  if not paused:
    printRectangles(rectangles, frame_idx)
    frame_idx += 1

  # display the frame
  if frame.__class__.__name__ != 'NoneType':
    cv2.imshow(windowName,frame)
  else:
    break
  if key == ord('q'):
      break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
