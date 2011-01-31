
import cv

def hsv_filter(src, min_h, max_h, min_s, max_s, min_v, max_v):
    '''Takes an 8-bit bgr src image and does simple hsv thresholding.

    A binary image of the same size will be returned.  HSV values have the
    following ranges:
           Hue - 0 to 360
    Saturation - 0 to 255
         Value - 0 to 255

    '''

    # OpenCV expects hue to be ranged from 0-180, since 0-360 wouldn't fit
    # inside a byte.  
    max_h /= 2
    min_h /= 2
    
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    binary = cv.CreateImage(cv.GetSize(src), 8, 1)
    cv.SetZero(binary)
    cv.CvtColor(src, hsv, cv.CV_RGB2HSV)

    data = hsv.tostring()
    for y in xrange(0, hsv.height):
        for x in xrange(0, hsv.width):
            index = y*hsv.width*3 + x*3
            h = ord(data[0+index])
            s = ord(data[1+index])
            v = ord(data[2+index])
            if h >= min_h and \
               h <= max_h and \
               s >= min_s and \
               s <= max_s and \
               v >= min_v and \
               v <= max_v:

                cv.Set2D(binary, y, x, (255,))

    return binary
