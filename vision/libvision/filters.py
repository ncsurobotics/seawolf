
import cv

def hsv_filter(src, low_h, high_h, min_s, max_s, min_v, max_v,
    hue_bandstop=False):
    '''Takes an 8-bit bgr src image and does simple hsv thresholding.

    A binary image of the same size will be returned.  HSV values have the
    following ranges:
           Hue - 0 to 360
    Saturation - 0 to 255
         Value - 0 to 255

    If hue_bandstop is True, the low_h and high_h will act as a band stop
    filter on hue, otherwise hue will be a band pass filter.

    '''

    # OpenCV expects hue to be ranged from 0-180, since 0-360 wouldn't fit
    # inside a byte.
    high_h /= 2
    low_h /= 2

    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    binary = cv.CreateImage(cv.GetSize(src), 8, 1)
    cv.SetZero(binary)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)

    data = hsv.tostring()
    for y in xrange(0, hsv.height):
        for x in xrange(0, hsv.width):
            index = y*hsv.width*3 + x*3
            h = ord(data[0+index])
            s = ord(data[1+index])
            v = ord(data[2+index])

            if hue_bandstop:
                if (h <= low_h or h >= high_h) and \
                   s >= min_s and \
                   s <= max_s and \
                   v >= min_v and \
                   v <= max_v:

                    cv.Set2D(binary, y, x, (255,))

            else:
                if h >= low_h and \
                   h <= high_h and \
                   s >= min_s and \
                   s <= max_s and \
                   v >= min_v and \
                   v <= max_v:

                    cv.Set2D(binary, y, x, (255,))

    return binary
