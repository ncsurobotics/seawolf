"""
Run through a video and draw boxes over significant objects.
Records box positions.

To make a new box, hit 'n'.
To select a box, click on it (it will turn red).
To delete a box, hit 'k'.
To pause/unpause, hit the space bar.
To skip 100 frames, hit 's'. Skip will save the data if it exits the video.

Hit q to quit and save or x to quit but not save.
"""
import numpy as np
import cv2
from key import getKeyPress
from mouse import mouseEvent, getMousePos, getLeftMouseClicked, getLeftMouseNewlyClicked
from util import dist
from rectangle import Rectangle
import sys
import time
from subprocess import call
import csv
import os

# constants
DEFAULT_RECT_WIDTH = 50
DEFAULT_RECT_HEIGHT = 50
MAX_CORNER_DIST = 100

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
paused = True

# how many seconds must pass between frames
frame_delay = .3

# true for 1 iteration of loop every time a frame is loaded
new_frame = True

# list containing all data about images and records of them
rectangle_records = []

# number of data frames collected for training
rectangles_collected = 0

# number of frames skipped when you hit skip
skip_amount = 100

#make a new save directory, labeled data, data-1, data-2, ...
n = 1
save_directory = './data/'
while os.path.exists(save_directory):
  save_directory = './data-' + str(n) +'/'
  n += 1
os.makedirs(save_directory)

# initial frame
if cap.isOpened():
  ret, frame = cap.read()
  prev_frame = frame.copy()

last_frame_read_time = time.time()




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
# cannot move rectangle corners outside of frame
def moveCornerTo(r, corner_idx, x, y, frame):
  screen_height, screen_width, _ = frame.shape
  if x < 0:
    x = 0
  if y < 0:
    y = 0
  if x >= screen_width:
    x = screen_width - 1
  if y >= screen_height:
    y = screen_height - 1

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

def recordRectangles(rectangle_records, rectangles, frame_idx, frame):
  global rectangles_collected
  rectangles_collected += len(rectangles)
  if len(rectangles) and frame.__class__.__name__ != 'NoneType':
    height, width, _ = frame.shape

    for r in rectangles:
      # make sure saved rectangle is within frame bounds
      x_min = r.x
      y_min = r.y
      x_max = r.x + r.w
      y_max = r.y + r.h
      if x_min < 0:
        x_min = 0
      if y_min < 0:
        y_min = 0
      if x_max >= width:
        x_max = width - 1
      if y_max >= height:
        y_max = height - 1

      record = (frame_idx, width, height, x_min, y_min, x_max, y_max)
      rectangle_records.append(record)
    print "Collected", rectangles_collected, "frames"
    

def saveRectangles(rectangle_records, img_name='frame', class_name="class", save_frames=True):
  if not len(rectangle_records):
    return
  print "Saving rectangle data"
  #save label information into csv file
  with open(save_directory + 'labels.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    for record in rectangle_records:
      frame_idx, width, height, min_x, min_y, max_x, max_y = record
      file_name = img_name + '-' + str(frame_idx) + '.jpg'
      writer.writerow( (file_name, width, height, class_name, min_x, min_y, max_x, max_y) )
    
  if save_frames:
    print "Saving video frames"
    # reopen the video and save each frame
    # save the image
    cap = cv2.VideoCapture(videoFileName)
    frame_idx = 0
    record_idx = 0
    last_frame_idx = rectangle_records[len(rectangle_records) - 1][0]

    while cap.isOpened() and frame_idx <= last_frame_idx:
      ret, frame = cap.read()
      record_frame_idx = rectangle_records[record_idx][0]

      if record_frame_idx == frame_idx:
        frame_save_path = save_directory + 'frame-' + str(frame_idx) + '.jpg'
        if not os.path.isfile(frame_save_path):
          cv2.imwrite(frame_save_path, frame)
        record_idx += 1
      frame_idx += 1

    cap.release()
    
  
  

while(cap.isOpened()):

  # Get key press
  key = getKeyPress()

  # toggle paused if the key pressed was space
  if key == ord(' '):
    paused = not paused

  # only play video if not paused
  if not paused:
    # only read frames every frame_delay seconds
    if time.time() - last_frame_read_time >= frame_delay:
      # current frame
      ret, frame = cap.read()
      last_frame_read_time = time.time()
      frame_idx += 1
      new_frame = True
    else:
      frame = prev_frame.copy()
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
      #print selected_corner
      r, corner_idx = selected_corner
      moveCornerTo(r, corner_idx, x, y, frame)
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
  if not paused and new_frame:
    recordRectangles(rectangle_records, rectangles, frame_idx, frame)

  # if the current frame was new, it is now old
  new_frame = False

  # display the frame
  if frame.__class__.__name__ != 'NoneType':
    cv2.imshow(windowName,frame)
  else:
    break
  # quit the program
  if key == ord('q') or key == ord('x'):
    break
  
  if key == ord('s'):
    print "Skipping ", skip_amount, "frames, at frame number ", frame_idx
    for i in range(skip_amount):
      ret, frame = cap.read()

      # save and quit
      if not ret:
        print "exiting"
        saveRectangles(rectangle_records)
        cap.release()
        cv2.destroyAllWindows()
        exit()

    last_frame_read_time = time.time()
    frame_idx += skip_amount
    new_frame = True
    prev_frame = frame.copy()


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# only save data if key was q
if key == ord('q'):
  saveRectangles(rectangle_records)