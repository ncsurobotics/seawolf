import cv2
import numpy as np
import os
from sys import argv

'''
    This test program allows for quick and easy checking of thresholds and 
    other parameters against a test video.  Each test recieves a frame and 
    returns a processed frame, allowing you to chain processing operations 
    together.

    USAGE:
        The video file can be passed in as a command-line argument, or by using
        the filename variable in main().  Channel (hue, saturation, etc), is 
        also changed in main().  Everything else is in a function.
'''

### Fallback if no argument is provided ###
path = '../FOOTAGE/cbuoy1.avi'

def preprocessing(frame):
    '''
        Perform static changes to the frame
    '''
    kernel_size = 5
    frame = cv2.medianBlur(frame, kernel_size)
    return frame


def run_tests(frame):
    ''' 
        Change which tests are performed and chain them together.  By chaining 
        together tests, you can quickly see the results of your changes
    '''
    frame = test_adaptive_threshold(frame)
    frame = test_contours(frame)
    # frame = test_edge_detection(frame)
    # frame = test_hough_lines(frame)
    # frame = test_hough_circles(frame)
    return frame


def test_adaptive_threshold(frame):
    ''' 
        Perform an adaptive threshold
    '''
    block_size = 25
    threshold = 15
    kernel_size = 3

    frame = cv2.adaptiveThreshold(frame,
                                  255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY_INV,
                                  block_size,
                                  threshold)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    frame = cv2.erode(frame, kernel)
    frame = cv2.dilate(frame, kernel)
    return frame


def test_contours(frame):
    '''
        Takes the contours of the image
    '''
    contours, hierarchy = cv2.findContours(frame,
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (255, 255, 255), 3)
    return frame


def test_edge_detection(frame):
    ''' 
        Finds the edges of the image
    '''
    frame = cv2.Canny(frame, 100, 250, apertureSize=3)
    return frame


def test_hough_lines(frame):
    '''
        Detect lines in the image
    '''
    #frame = cv2.HoughLines(frame, )
    pass


def main():
    '''
        Change the video file path and channel manually
    '''
    base_dir = os.path.dirname(__file__)
    filename = os.path.join(base_dir, path)
    if len(argv) > 1:
        filename = argv[1]

    vc = cv2.VideoCapture(filename)

    cv2.namedWindow('original')
    cv2.namedWindow('debug')

    while True:
        rval, frame = vc.read()
        if not rval:
            break
        cv2.imshow('original', frame)

        BGRframe = frame
        HSVframe = cv2.cvtColor(BGRframe, cv2.COLOR_BGR2HSV)

        (blue, green, red) = cv2.split(BGRframe)
        (hue, saturation, value) = cv2.split(HSVframe)

        ##################################
        ## Change channel to hue, saturation, value, red, blue, green, etc. ##
        frame = saturation
        ##################################

        frame = preprocessing(frame)
        frame = run_tests(frame)

        cv2.imshow('debug', frame)
        cv2.waitKey(15)

    vc.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
