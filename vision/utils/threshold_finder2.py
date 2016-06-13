#!/usr/bin/env python
"""
Program for finding thresholds on some given channel

Usage:

    ./threshold_finder.py [path to media]
"""

from __future__ import print_function

import os
import cv2
import numpy as np
from sys import argv

path = ''
draw_contours = False

# Constants for the names of the trackbars, since they're specified by name
tbar_play_video_name = 'Play Video'
tbar_channel_select_name = 'Select Channel (HSV)'
tbar_block_size_name = 'Block Size'
tbar_thresh_name = 'Threshold'

# Contants for the names of the windows, since they're specified by name
win_default_name = 'original'
win_debug_name = 'debug'


def main():
    base_dir = os.getcwd()

    if len(argv) > 1:
        path = argv[1]

    if not path:
        print("Must provide a path to get footage from")
        exit()

    filename = os.path.join(base_dir, path)

    if not os.path.isfile(filename):
        print("Invalid Path - File does not exist")
        exit()

    create_interface()

    vc = cv2.VideoCapture(filename)
    run(vc)
    vc.release()
    cv2.destroyAllWindows()


def run(capture):
    current_frame = get_new_frame(capture)

    while capture.isOpened():
        if cv2.getTrackbarPos(tbar_play_video_name, win_debug_name):
            try:
                current_frame = get_new_frame(capture)
            except StopIteration:
                print("End of clip")
                break

        debug_frame = process_frame(current_frame.copy())

        cv2.imshow(win_default_name, current_frame)
        cv2.imshow(win_debug_name, debug_frame)
        cv2.waitKey(40)


def process_frame(frame):
    """ Process frame based on user input """
    hue = cv2.getTrackbarPos(tbar_channel_select_name, win_debug_name)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = frame[:,:,0]
    
    #shift hue by desired amount
    frame += hue
    mode = 'normal'
    
    if mode=="normal":
        pass
        
    elif mode=="absolute":
        frame = cv2.subtract(127 , cv2.absdiff(frame,127))
        frame = cv2.multiply(2,frame)
        
    elif mode=="inverted":
        frame = cv2.subtract(255-frame)
        

    block_size = cv2.getTrackbarPos(tbar_block_size_name, win_debug_name)
    threshold = cv2.getTrackbarPos(tbar_thresh_name, win_debug_name)

    if not block_size % 2 == 1:
        block_size += 1
        cv2.setTrackbarPos(tbar_block_size_name, win_debug_name, block_size)

    if block_size <= 1:
        block_size = 3
        cv2.setTrackbarPos(tbar_block_size_name, win_debug_name, block_size)

    adaptive = cv2.adaptiveThreshold(frame, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY_INV,
                                     block_size,
                                     threshold)

    if draw_contours:
        cframe = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        contours, hierarchy = cv2.findContours(adaptive,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(cframe, contours, -1, (255, 255, 255), 3)
        return cframe
    else:
        return adaptive


def get_new_frame(vc):
    """ Get a new image from a media source """
    rval, frame = vc.read()
    if not rval:
        raise StopIteration
    return frame


def get_channel(frame, channel):
    """ Get a specific channel from an image"""
    splitf = cv2.split(frame)

    return splitf[channel]


def create_interface():
    """ Create windows and trackbars """
    cv2.namedWindow(win_default_name)
    cv2.namedWindow(win_debug_name)

    # Function that activates on trackbar movement
    def nothing(x):
        pass

    cv2.createTrackbar(tbar_play_video_name, win_debug_name, 0, 1, nothing)
    cv2.createTrackbar(tbar_channel_select_name, win_debug_name, 0, 255, nothing)
    cv2.createTrackbar(tbar_thresh_name, win_debug_name, 25, 75, nothing)
    cv2.createTrackbar(tbar_block_size_name, win_debug_name, 25, 49, nothing)


if __name__ == '__main__':
    main()
