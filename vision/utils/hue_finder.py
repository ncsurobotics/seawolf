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
tbar_hue_select_name = 'Hue'
tbar_span_name = 'Span'
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
    current_frame = cv2.resize(current_frame,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_NEAREST)

    #while video is not closed
    while capture.isOpened():
        
        #check if play "button" is active
        if cv2.getTrackbarPos(tbar_play_video_name, win_debug_name):
            try:
                current_frame = get_new_frame(capture)
            except StopIteration:
                print("End of clip")
                break
                
        #scale the frame down
        current_frame = cv2.resize(current_frame,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_NEAREST)

        #make a copy of the raw frame, and print it to the debug frame
        debug_frame = process_frame(current_frame.copy())

        #print the image
        cv2.imshow(win_default_name, current_frame)
        cv2.imshow(win_debug_name, debug_frame)

        #set refresh rate
        cv2.waitKey(40)


def process_frame(frame):
    """ Process frame based on user input """
    center_val = cv2.getTrackbarPos(tbar_hue_select_name, win_debug_name)
    span_val = cv2.getTrackbarPos(tbar_span_name, win_debug_name)
    
    
    #get mirror point from values
    offset_val = 90 - center_val
    mirror_val = 180 - center_val
    
    #get bounds

    #convert to hsv
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #convert grayscale
    frame = get_channel(frame_hsv, 0)
    
    #setupe debug window
    temp = cv2.resize(frame,None,fx=3,fy=1,interpolation=cv2.INTER_NEAREST)
    (h,w) = temp.shape
    x1 = 0
    x2 = w/3
    x3 = 2* w/3
    output_frame = np.zeros(temp.shape+(3,), np.uint8)
    
    #print input frame (#1)
    output_frame[0:h,0:x2] = cv2.cvtColor(cv2.multiply(1.42,frame), cv2.COLOR_GRAY2BGR) ####################
    
    #print rough threshold frame (#2)
    output_frame[0:h,x2:x3] = cv2.cvtColor(
        cv2.inRange(frame,center_val-span_val/2.0,center_val+span_val/2.0),
        cv2.COLOR_GRAY2BGR
        ) #############################
    
    #generate a blank canvas
    (height,width) = frame.shape
    normalized_hue_frame = np.zeros((height,width,1), np.uint8)
    
    if (offset_val < 0):
        #mask for values above cutoff and shift down
        msk = cv2.inRange(frame, -offset_val, 180) #generate mask
        #print("cv2.inRange(frame, {}, {})".format(-offset_val,180))

    else:
        #mask for values below cutoff and shift up
        msk = cv2.inRange(frame, 0, 180-offset_val) #generate mask
        #print("cv2.inRange(frame, {}, {})".format(0, 180-offset_val))
        
    #selectively shift values down
    normalized_hue_frame = cv2.add(frame,offset_val, mask=msk) #temp = raw frame shift up where it counts
    
    #generate mask and wrap/flip values
    msk = cv2.bitwise_not(msk) #work
    inverted_frame = cv2.subtract(180,frame) #works
    
    
    
    #fill flipped regions with wrapped values
    temp = cv2.add(normalized_hue_frame, inverted_frame, mask=msk) #
    normalized_hue_frame = cv2.add(temp,normalized_hue_frame)
    
    
    #normalize
    distance_frame = cv2.absdiff(normalized_hue_frame,90)
    normalized_hue_frame = cv2.subtract(180,distance_frame)
    
    #print final frame (#3)
    output_frame[0:h,x3:w] = cv2.cvtColor(
        cv2.multiply(1.42,normalized_hue_frame),
        cv2.COLOR_GRAY2BGR) ################
    #frame_hsv[:,:,0] = normalized_hue_frame
    #output_frame[0:h,x3:w] = cv2.cvtColor(frame_hsv,cv2.COLOR_HSV2BGR) ################
    
    
    
    
    
    return output_frame
   
    #get inputs
    #block_size = cv2.getTrackbarPos(tbar_block_size_name, win_debug_name)
   


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

    #trackbars on the debug window
    #cv2.createTrackbar(tbar_play_video_name, win_debug_name, 0, 1, nothing)
    cv2.createTrackbar(tbar_hue_select_name, win_debug_name,0,180,nothing)
    cv2.createTrackbar(tbar_span_name,win_debug_name,0,180,nothing)
    cv2.setTrackbarPos(tbar_span_name, win_debug_name,30)

if __name__ == '__main__':
    main()
