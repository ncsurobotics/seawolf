# pylint: disable=E1101
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
        cv.Line(src, pt1, pt2, cv.RGB(255, 0, 0), 3, cv.CV_AA, 0)


def draw_linesC(src, lines, color, limit=None):
    '''Draws lines on the image in given color, because I'm sick of red.

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
        cv.Line(src, pt1, pt2, cv.RGB(color[0],color[1],color[2]), 3, cv.CV_AA, 0)



def get_channel(frame, channel):
    '''
    Returns a single channel image containing the specified channel from frame.

    The channel given is 0-indexed.

    '''
    result = cv.CreateImage(cv.GetSize(frame), 8, 1)
    previous_coi = cv.GetImageCOI(frame)
    cv.SetImageCOI(frame, channel+1)  # COI is 1-indexed
    cv.Copy(frame, result)
    cv.SetImageCOI(frame, previous_coi)
    return result

def scale_32f_image(image):

    result = cv.CreateImage(cv.GetSize(image), 8, image.channels)
    channel_image = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_32F, 1)
    channel_scaled = cv.CreateImage(cv.GetSize(image), 8, 1)
    print "CHANNELS:", image.channels
    for channel_num in xrange(1, image.channels+1):

        cv.SetImageCOI(image, channel_num)
        cv.Copy(image, channel_image)
        maximum = cv.MinMaxLoc(channel_image)[1]
        print "MAXIMUM:", maximum
        cv.ConvertScale(channel_image, channel_scaled, 255/maximum)

        cv.SetImageCOI(result, channel_num)
        cv.Copy(channel_scaled, result)

    cv.SetImageCOI(image, 0)
    cv.SetImageCOI(result, 0)
    return result
