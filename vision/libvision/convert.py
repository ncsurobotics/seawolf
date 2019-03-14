import numpy as np
import cv2.cv as cv


def cv_to_cv2(frame):
    '''Convert a cv image into cv2 format.

    Keyword Arguments:
    frame -- a cv image
    Returns a numpy array that can be used by cv2.
    '''
    cv2_image = np.asarray(frame[:, :])
    return cv2_image


def cv2_to_cv(frame):
    '''Convert a cv2 image into cv format.

    Keyword Arguments:
    frame -- a cv2 numpy array representing an image.
    Returns a cv image.
    '''
    container = cv.fromarray(frame)
    cv_image = cv.GetImage(container)
    return cv_image


def cv2_to_cv_protected(frame):
    '''Convert a cv2 image into cv format.

    Keyword Arguments:
    frame -- a cv2 numpy array representing an image.
    Returns a cv image.
    '''
    frame = frame.copy()  # makes the frame contiguous
    container = cv.fromarray(frame)
    cv_image = cv.GetImage(container)
    return cv_image
