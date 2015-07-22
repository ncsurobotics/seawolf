#!/usr/bin/env python
"""
Compare Hue, Saturation, and Value channels in some media

Usage:

    ./channel_compare.py [path to media]
"""

from __future__ import print_function

import os
import cv2
import sys

path = ''
draw_contours = False

# Constants for the names of the trackbars, since they're specified by name
tbar_play_video_name = 'Play Video'
tbar_invert_name = 'Invert Frame'

# Contants for the names of the windows, since they're specified by name
win_default_name = 'original'
win_hue_name = 'Hue channel'
win_sat_name = 'Saturation channel'
win_val_name = 'Value channel'


def main():
    base_dir = os.getcwd()

    if len(sys.argv) > 1:
        path = sys.argv[1]

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
    """ Update display based on user input """
    current_frame = get_new_frame(capture)

    while capture.isOpened():
        if cv2.getTrackbarPos(tbar_play_video_name, win_default_name):
            try:
                current_frame = get_new_frame(capture)
            except StopIteration:
                print("End of clip")
                break



        (hue_frame, sat_frame, val_frame) = cv2.split(cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV))

        if cv2.getTrackbarPos(tbar_invert_name, win_hue_name):
            hue_frame = cv2.bitwise_not(hue_frame)

        if cv2.getTrackbarPos(tbar_invert_name, win_sat_name):
            sat_frame = cv2.bitwise_not(sat_frame)

        if cv2.getTrackbarPos(tbar_invert_name, win_val_name):
            val_frame = cv2.bitwise_not(val_frame)

        cv2.imshow(win_default_name, current_frame)
        cv2.imshow(win_hue_name, hue_frame)
        cv2.imshow(win_sat_name, sat_frame)
        cv2.imshow(win_val_name, val_frame)

        cv2.waitKey(40)


def get_new_frame(vc):
    """ Read new frame from camera """
    rval, frame = vc.read()
    if not rval:
        raise StopIteration
    return frame


def create_interface():
    """ Create gui, windows and trackbars """
    cv2.namedWindow(win_default_name)
    cv2.namedWindow(win_hue_name)
    cv2.namedWindow(win_sat_name)
    cv2.namedWindow(win_val_name)

    # Function that activates on trackbar movement
    def nothing(x):
        pass

    cv2.createTrackbar(tbar_play_video_name, win_default_name, 0, 1, nothing)
    cv2.createTrackbar(tbar_invert_name, win_hue_name, 0, 1, nothing)
    cv2.createTrackbar(tbar_invert_name, win_sat_name, 0, 1, nothing)
    cv2.createTrackbar(tbar_invert_name, win_val_name, 0, 1, nothing)

if __name__ == '__main__':
    main()
