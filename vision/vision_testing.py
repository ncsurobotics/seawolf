import cv2
import numpy as np
import os

'''
    This test program allows for quick and easy checking of thresholds and 
    other parameters against a test video.  Each test recieves a frame and 
    returns a processed frame, allowing you to optionally chain processing
    operations together.
'''


def preprocessing(frame):
    '''
        Perform static changes to the frame
    '''
    frame = cv2.medianBlur(frame, 5)
    return frame


def run_tests(frame):
    ''' 
        Change which tests are performed and chain them together.  By chaining 
        together tests, you can quickly see the results of your changes
    '''
    frame = test_adaptive_threshold(frame)
    # frame = test_contours(frame)
    # frame = test_edge_detection(frame)
    # frame = test_hough_lines(frame)
    return frame


def test_adaptive_threshold(frame):
    ''' 
        Perform an adaptive threshold
    '''
    block = 25
    thresh = 15
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    frame = cv2.adaptiveThreshold(frame,
                          255,
                          cv2.ADAPTIVE_THRESH_MEAN_C,
                          cv2.THRESH_BINARY_INV,
                          block,
                          thresh)

    frame = cv2.erode(frame, kernel)
    frame = cv2.dilate(frame, kernel)
    return frame


def test_contours(frame):
    '''
        Takes the contours of the image
    '''
    return frame


def main():
    '''
        Change the video file path and channel
    '''
    filename = 'FOOTAGE/cbins1.avi'

    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
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

        ## Change channel to hue, saturation, value, red, blue, green, etc. ##
        frame = saturation

        frame = run_tests(frame)

        cv2.imshow('debug', frame)
        cv2.waitKey(15)

    vc.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
