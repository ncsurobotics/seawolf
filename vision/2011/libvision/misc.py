
import math

import cv

def draw_lines(src, lines, limit=None):
    '''Draws lines on the image.

    Arguments:
        src - Source image which to draw lines on.
        lines - A list of lines.  This should be in the format of rho, theta
            pairs: [(rho, theta), ...].  This is the same format which
            cv.HoughLines2() returns.
        limit - If given, it only that many number of lines will be drawn.

    '''
    if not limit:
        limit = len(lines)

    for rho, theta in lines[:limit]:
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho 
        y0 = b * rho
        pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
        pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
        cv.Line(src, pt1, pt2, cv.RGB(255, 0, 0), 1, cv.CV_AA, 0)
