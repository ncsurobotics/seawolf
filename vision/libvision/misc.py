import math

import cv
import cv2
import numpy as np


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
        pt1 = (cv.Round(x0 + 1000 * (-b)), cv.Round(y0 + 1000 * (a)))
        pt2 = (cv.Round(x0 - 1000 * (-b)), cv.Round(y0 - 1000 * (a)))
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
        pt1 = (cv.Round(x0 + 1000 * (-b)), cv.Round(y0 + 1000 * (a)))
        pt2 = (cv.Round(x0 - 1000 * (-b)), cv.Round(y0 - 1000 * (a)))
        cv.Line(src, pt1, pt2, cv.RGB(color[0], color[1], color[2]), 3, cv.CV_AA, 0)


def get_channel(frame, channel):
    '''
    Returns a single channel image containing the specified channel from frame.

    The channel given is 0-indexed.

    '''
    result = cv.CreateImage(cv.GetSize(frame), 8, 1)
    previous_coi = cv.GetImageCOI(frame)
    cv.SetImageCOI(frame, channel + 1)  # COI is 1-indexed
    cv.Copy(frame, result)
    cv.SetImageCOI(frame, previous_coi)
    return result
'''
def center_track(founds,candidates,confirmeds,max_trans,max_expand):
    #The next section repeats three times. Try to simplify function?
    for found in founds[:]:
        for candidate in candidates:
            if math.fabs(found.midx-candidate.midx) < max_trans and math.fabs(found.midy-candidate.midy) < max_trans and math.fabs(found.size - candidate.size)<max_expand:
                ID = candidate.id
                candidate = found
                candidate.id = ID
                founds.remove(found)

    for found in founds[:]:
        for confirmed in confirmeds:
            if math.fabs(found.midx-confirmed.midx) < max_trans and math.fabs(found.midy-confirmed.midy) < max_trans and math.fabs(found.size - confirmed.size)<max_expand:
                ID = confirmed.id
                confirmed = found
                confirmed.id = ID
                founds.remove(found)

    for candidate in candidates[:]:
        for confirmed in confirmeds:
            if math.fabs(candidate.midx-confirmed.midx) < max_trans and math.fabs(candidate.midy-confirmed.midy) < max_trans and math.fabs(candidate.size - confirmed.size)<max_expand:
                ID = confirmed.id
                confirmed = candidate
                confirmed.id = ID
                candidates.remove(candidate)


#def update_center(candidates,confirmed,seencount_thresh, lastseen_thresh)


#objs1 and objs2 should be lists of obj
def compare_mids_ObjList(objs1,objs2,max_trans,max_expand):
    for obj1 in objs1[:]:
        for obj2 in objs2:
            if math.fabs(obj1.midx-obj2.midx) < max_trans and math.fabs(obj1.midy-obj2.midy) < max_trans and math.fabs(obj1.size - obj2.size)<max_expand:
                ID = obj2.id
                obj2 = obj1
                obj1.id = ID
                obj1.remove(obj2)


#obj1: one to be overwritten
#obj2: one to overwrite with
def overwrite_obj(obj1,obj2):
    obj1.midx = obj2.midx
    obj1.midy = obj2.midy
    obj1.corner1 = obj2.corner1
    obj1.corner2 = obj2.corner2
    obj1.corner3 = obj2.corner3
    obj1.corner4 = obj2.corner4
'''


def scale_32f_image(image):

    result = cv.CreateImage(cv.GetSize(image), 8, image.channels)
    channel_image = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_32F, 1)
    channel_scaled = cv.CreateImage(cv.GetSize(image), 8, 1)
    print "CHANNELS:", image.channels
    for channel_num in xrange(1, image.channels + 1):

        cv.SetImageCOI(image, channel_num)
        cv.Copy(image, channel_image)
        maximum = cv.MinMaxLoc(channel_image)[1]
        print "MAXIMUM:", maximum
        cv.ConvertScale(channel_image, channel_scaled, 255 / maximum)

        cv.SetImageCOI(result, channel_num)
        cv.Copy(channel_scaled, result)

    cv.SetImageCOI(image, 0)
    cv.SetImageCOI(result, 0)
    return result

def shift_hueCV2(frame, shift, mode="normal"):
    #shift hue by desired amount
    frame = frame + shift
    
    if mode=="normal":
        pass
        
    elif mode=="absolute":
        frame = cv2.subtract(127 , cv2.absdiff(frame,127))
        frame = cv2.multiply(2,frame)
        
    elif mode=="inverted":
        frame = cv2.subtract(255-frame)
        
    return frame
    

def cv_to_cv2(frame):
    '''Convert a cv image into cv2 format.
    
    Keyword Arguments:
    frame -- a cv image
    Returns a numpy array that can be used by cv2.
    '''
    cv2_image = np.asarray(frame[:,:])
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
