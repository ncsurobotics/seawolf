import os
import cv2
import numpy as np
from sys import argv

path = ''
draw_contours = False


def main():

    base_dir = os.getcwd()

    if len(argv) > 1:
        path = argv[1]

    if not path:
        raise Exception("Must provide a path to get footage from")

    filename = os.path.join(base_dir, path)

    if not os.path.isfile(filename):
        print "Invalid Path - File does not exist"
        exit()

    vc = cv2.VideoCapture(filename)

    create_interface()
    run(vc)
    vc.release()


def run(capture):
    current_frame = get_new_frame(capture)

    while capture.isOpened():

        if cv2.getTrackbarPos('Play Video', 'debug'):
            current_frame = get_new_frame(capture)

        try:
            debug_frame = process_frame(current_frame.copy())
        except StopIteration:
            print "End of clip"
            break

        refresh_display(current_frame, debug_frame)


def get_channel(frame, channel):
    splitf = cv2.split(frame)

    return splitf[channel]


def refresh_display(ref, debug):
    cv2.imshow('original', ref)
    cv2.imshow('debug', debug)
    cv2.waitKey(40)


def process_frame(frame):
    channel = cv2.getTrackbarPos('HSV', 'debug')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = get_channel(frame, channel)

    block_size = cv2.getTrackbarPos('Block size', 'debug')
    threshold = cv2.getTrackbarPos('Threshold', 'debug')

    if not block_size % 2 == 1:
        block_size += 1
        cv2.setTrackbarPos('Block size', 'debug', block_size)

    if block_size <= 1:
        block_size = 3
        cv2.setTrackbarPos('Block size', 'debug', block_size)

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


def create_interface():
    cv2.namedWindow('original')
    cv2.namedWindow('debug')

    # Function that activates on trackbar movement
    def nothing(x):
        pass

    cv2.createTrackbar('Threshold', 'debug', 25, 75, nothing)
    cv2.createTrackbar('Block size', 'debug', 25, 49, nothing)
    cv2.createTrackbar('Play Video', 'debug', 0, 1, nothing)
    cv2.createTrackbar('HSV', 'debug', 1, 2, nothing)


def get_new_frame(vc):
    rval, frame = vc.read()
    if not rval:
        raise StopIteration
    return frame


if __name__ == '__main__':
    main()
