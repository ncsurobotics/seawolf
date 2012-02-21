
from __future__ import division
import math

import pid
from mixer import mixer

def pairwise_disjoint(*args):
    for i in range(0, len(args) - 1):
        for e in args[i+1:]:
            if not e.isdisjoint(args[i]):
                return False
    return True

def add_angle(a, b):
    return (((a + 180) + b) % 360) - 180

def circular_average(numbers, high=2*math.pi, low=0):
    '''Averages a set of numbers in a circular fashion.

    high and low are the ends of the wraparound point.  Going any higher than
    high wraps around to low.

    '''

    # Since we will be using sin and cos, we scale the numbers from the range
    # high-low to the range 2*pi-0.
    linear_factor = 2*math.pi / (high - low)

    total_x = 0
    total_y = 0
    for number in numbers:
        angle = (number - low) * linear_factor
        total_x += math.sin(angle)
        total_y += math.cos(angle)
    average_angle = math.atan2(total_x, total_y)
    return average_angle / linear_factor + low

def circular_range(numbers, high=2*math.pi, low=0):
    '''Finds the range of a set of numbers in a circular fashion.

    high and low are the ends of the wraparound point.  Going any higher than
    high wraps around to low.

    '''

    highest_range = 0
    numbers = sorted(numbers)
    for i in xrange(len(numbers)):

        range = abs(numbers[i] - numbers[(i+1)%len(numbers)])

        # Take the shorter distance around the circle
        if range > (high-low)/2:
            range = (high-low) - range

        if range > highest_range:
            highest_range = range

    return highest_range

def circular_distance(a, b, high=2*math.pi, low=0):
    '''Finds the distance between a and b in a circular fashion.

    high and low are the ends of the wraparound point.  Going any higher than
    high wraps around to low.

    '''

    a -= low
    b -= low
    diff = high - low

    a = a % diff
    b = b % diff
    if abs(a-b) < diff/2:
        return abs(a-b)
    else:
        return diff - abs(a-b)

