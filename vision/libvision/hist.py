
from __future__ import division

import cv

def histogram_image(hist, color=(255,255,255), background_color=(0,0,0), num_bins=256):
    '''Returns an image displaying the the given histogram.'''

    max_value = int(cv.GetMinMaxHistValue(hist)[1])

    img = cv.CreateImage((num_bins,num_bins), 8, 3)
    cv.Set(img, background_color)

    for i in xrange(num_bins):
        height = int(cv.QueryHistValue_1D(hist, i) / max_value * num_bins)
        cv.Line(img, (i,num_bins), (i,num_bins-height), color)

    return img
