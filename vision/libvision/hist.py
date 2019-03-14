# pylint: disable=E1101
from __future__ import division
from math import sqrt

import cv


def histogram_image(hist, color=(255, 255, 255), background_color=(0, 0, 0), num_bins=256):
    '''Returns an image displaying the the given histogram.'''

    max_value = int(cv.GetMinMaxHistValue(hist)[1])

    img = cv.CreateImage((num_bins, num_bins), 8, 3)
    cv.Set(img, background_color)

    for i in xrange(num_bins):
        height = int(cv.QueryHistValue_1D(hist, i) / max_value * num_bins)
        cv.Line(img, (i, num_bins), (i, num_bins - height), color)

    return img


def calc_expected_value(hist, num_bins=256):
    sum = 0
    num_datapoints = 0
    for i in xrange(num_bins):
        value = cv.QueryHistValue_1D(hist, i)
        num_datapoints += value
        sum += value * i
    return sum / num_datapoints


def calc_variance(hist, expected_value=None, num_bins=256):

    if expected_value is None:
        expected_value = calc_expected_value(hist, num_bins)

    variance = 0
    sum = 0
    for i in xrange(num_bins):
        value = cv.QueryHistValue_1D(hist, i)
        variance += value * (i - expected_value) ** 2
        sum += value
    return variance / sum


def calc_stddev(hist, expected_value=None, num_bins=256):
    return sqrt(
        calc_variance(hist, expected_value, num_bins=256)
    )


def num_stddev_from_mean(hist, x, num_bins=256):
    '''Calculates how many standard deviations x is away from the mean.'''

    expected_value = calc_expected_value(hist, num_bins)
    stddev = calc_stddev(hist, expected_value, num_bins)
    return (x - expected_value) / stddev
