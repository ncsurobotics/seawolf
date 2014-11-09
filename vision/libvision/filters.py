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
            index = y * hsv.width * 3 + x * 3
            h = ord(data[0 + index])
            s = ord(data[1 + index])
            v = ord(data[2 + index])

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


def otsu_get_threshold(src):
    '''
    Find the optimal threshold value for a grey level image using Otsu's
    method.

    This is baised on Otsu's original paper published in IEEE Xplore: "A
    Threshold Selection Method from Gray-Level Histograms"

    '''

    if src.nChannels != 1:
        raise ValueError("Image must have one channel.")

    # Compute Histogram
    hist = cv.CreateHist([256], cv.CV_HIST_ARRAY, [[0, 255]], 1)
    cv.CalcHist([src], hist)

    # Convert to Probability Histogram
    cv.NormalizeHist(hist, 1)

    overall_moment = 0
    for t in xrange(256):
        overall_moment += t * cv.QueryHistValue_1D(hist, t)

    # Find the threshold t that gives the highest variance
    # Suffixes _b and _f mean background and foreground
    num_pixels = src.width * src.height
    weight_b = 0
    moment_b = 0
    highest_variance = 0
    best_threshold = 0
    for t in xrange(256):

        hist_value = cv.QueryHistValue_1D(hist, t)

        weight_b += hist_value
        weight_f = 1 - weight_b
        if weight_b == 0:
            continue
        if weight_f == 0:
            break

        moment_b += t * hist_value
        moment_f = overall_moment - moment_b

        mean_b = moment_b / weight_b
        mean_f = moment_f / weight_f

        variance_between = weight_b * weight_f * \
            (mean_b - mean_f) ** 2

        if variance_between >= highest_variance:
            highest_variance = variance_between
            best_threshold = t

    return best_threshold


def otsu_threshold(src, max_value=255, threshold_type=cv.CV_THRESH_BINARY):
    # TODO: Documentation
    threshold = otsu_get_threshold(src)
    dst = cv.CreateImage((src.width, src.height), 8, 1)
    cv.Threshold(src, dst, threshold, max_value, threshold_type)
    return dst
