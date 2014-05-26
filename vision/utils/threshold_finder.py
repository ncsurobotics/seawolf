import os
import cv2
import numpy as np
from sys import argv

path = ''
draw_contours = False


def main():

    if len(argv) > 1:
        path = argv[1]

    base_dir = os.getcwd()
    filename = os.path.join(base_dir, path)

    if not os.path.isfile(filename):
        print "Invalid Path - File does not exist"
        exit()

    cv2.namedWindow('original')
    cv2.namedWindow('debug')

    vc = cv2.VideoCapture(filename)

    frame, debug = get_new_frame(vc)
    prior = debug.copy()

    cv2.createTrackbar('Threshold', 'original', 25, 75, nothing)
    cv2.createTrackbar('Blocksize', 'original', 25, 49, nothing)
    cv2.createTrackbar('Play Video', 'original', 0, 1, nothing)

    while True:
        if cv2.getTrackbarPos('Play Video', 'original'):
            frame, debug = get_new_frame(vc)
            prior = debug.copy()
        else: #### For amusement and/or a seizure, comment out this else block and observe the result ####
            debug = prior.copy()
        debug = refresh_frame(debug)
        cv2.imshow('original', frame)
        cv2.imshow('debug', debug)
        cv2.waitKey(50)


def nothing(x):
        pass


def refresh_frame(img):
    block_size = cv2.getTrackbarPos('Blocksize', 'original')
    threshold = cv2.getTrackbarPos('Threshold', 'original')

    if not block_size % 2 == 1:
        block_size += 1
        cv2.setTrackbarPos('Blocksize', 'original', block_size)

    if block_size <= 1:
        block_size = 3
        cv2.setTrackbarPos('Blocksize', 'original', block_size)

    adaptive = cv2.adaptiveThreshold(img, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY_INV,
                                     block_size,
                                     threshold)

    if draw_contours:
        black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        contours, hierarchy = cv2.findContours(adaptive,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(black, contours, -1, (255, 255, 255), 3)
        return black
    return adaptive


def get_new_frame(vc):
    rval, frame = vc.read()
    if not rval:
        print "End of clip"
        exit()
    debug = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    (h, s, v) = cv2.split(debug)
    debug = s
    return frame, debug


if __name__ == '__main__':
    main()
