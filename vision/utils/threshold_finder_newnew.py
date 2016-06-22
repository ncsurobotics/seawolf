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
tbar_block_size_name2 = 'Block Size2'
tbar_thresh_name = 'Threshold'
tbar_thresh_name2 = 'Threshold2'
tbar_blur = "blurs"
tbar_erode_name = "erode"
tbar_dilate_name = 'dilate'
tbar_output_select_name = "output"


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

    frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    # keep the original
    #frame = cv2.blur(frame,(blur,blur))
    raw_frame = frame

    # run adaptive threshold
    adaptive_frame = adaptiveThreshold(frame)
    frame = adaptive_frame

    # perform morphology
    morph_frame = morphology(frame)
    frame = morph_frame
    
    # select output
    stage = cv2.getTrackbarPos(tbar_output_select_name, win_debug_name)
    if stage == 0:
        final_frame = raw_frame
    elif stage == 1:
        final_frame = adaptive_frame
    elif stage == 2:
        final_frame = morph_frame
    else:
        final_frame = frame

    return final_frame

def process_block(tbar_name):
    block_size = cv2.getTrackbarPos(tbar_name, win_debug_name)
    if not block_size % 2 == 1:
        block_size += 1
        cv2.setTrackbarPos(tbar_name, win_debug_name, block_size)

    if block_size <= 1:
        block_size = 3
        cv2.setTrackbarPos(tbar_name, win_debug_name, block_size)
    return block_size

def adaptiveThreshold(frame):
    # select a channel
    channel = cv2.getTrackbarPos(tbar_channel_select_name, win_debug_name)
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:,:,channel]
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:,:,2]
    frame = frame1

    # adaptive Threshold
    block_size = process_block(tbar_block_size_name)
    block_size2 = process_block(tbar_block_size_name2)
    threshold = cv2.getTrackbarPos(tbar_thresh_name, win_debug_name)
    threshold2 = cv2.getTrackbarPos(tbar_thresh_name2, win_debug_name)

    frame = cv2.adaptiveThreshold(frame, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY_INV,
                                     block_size,
                                     threshold)

    print (block_size2)
    frame2 = cv2.adaptiveThreshold(frame2,
                                    255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY_INV,
                                    block_size2,
                                    threshold2)
       
    frame = cv2.add(frame,frame2)

    return frame

def morphology(frame):
    erode_factor = cv2.getTrackbarPos(tbar_erode_name, win_debug_name)
    dilate_factor = cv2.getTrackbarPos(tbar_dilate_name, win_debug_name)

    if erode_factor < 1:
        erode_factor = 1

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_factor, erode_factor))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_factor, erode_factor))
    frame = cv2.erode(frame, kernel)
    frame = cv2.dilate(frame, kernel2)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_factor, dilate_factor))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_factor, dilate_factor))
    frame = cv2.dilate(frame, kernel2)
    frame = cv2.erode(frame, kernel)

    return frame

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
    cv2.createTrackbar(tbar_channel_select_name, win_debug_name, 1, 2, nothing)
    cv2.createTrackbar(tbar_thresh_name, win_debug_name, 12, 75, nothing)
    cv2.createTrackbar(tbar_thresh_name2, win_debug_name, 23, 75, nothing)
    cv2.createTrackbar(tbar_block_size_name, win_debug_name, 33, 49, nothing)
    cv2.createTrackbar(tbar_block_size_name2, win_debug_name, 49, 49, nothing)
    cv2.createTrackbar(tbar_blur, win_debug_name,3,21,nothing)
    cv2.createTrackbar(tbar_erode_name, win_debug_name, 4, 30, nothing)
    cv2.createTrackbar(tbar_dilate_name, win_debug_name, 4, 30, nothing)
    cv2.createTrackbar(tbar_output_select_name, win_debug_name, 0, 10, nothing)

if __name__ == '__main__':
    main()
