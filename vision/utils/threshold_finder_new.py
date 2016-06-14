#!/usr/bin/env python
"""
Program for finding thresholds on some given channel

Usage:

    ./threshold_finder.py [path to media]
"""

from __future__ import print_function

import os
import cv2
import numpy as np
from sys import argv

class WindowManager:
    def __init__(self, processor):
        self.processor = processor
        self.window = None
        

    def define_gui(self, config):
        # define window

        pipeline = self.processor.pipeline.get_kwargs()

        # define nothing function
        for process in pipeline:
            for tbar in processor.get_tbar_def(process)
                tbar_name = tbar['name']
                tbar_min = tbar['min']
                tbar_max = tbar['max']
                tbar_func = tbar['func']
                cv2.creatTrackbar(tbar['name'], self.window, tbar['min'], tbar['max'], tbar['func'])


    def print(self):

    def process(self):

    def collect_inputs(self):

    def flip(self):
        current_frame = self.get_new_frame(capture)

    def get_new_frame(vc):
        """ Get a new image from a media source """
        rval, frame = vc.read()
        if not rval:
            raise StopIteration
        return frame
        

class FrameProcessor:
    def __init__(self):
        


    def adaptive_thresh(self):
        pass
    
    def despeckle(self):
        pass

    def blot(self):
        pass


    def algorithm1(self):


    def load_algorithm(self, algorithm):
        self.queue.append(algorithm)


    def collect_inputs(self):

    def attach_tbar(self, func, tbar_name, min, max, input_func=None):

    def get_tbar_def(self):

    


def main():
    # load the footage
    vc = win.load(argv[1])

    # 
    win.create_interface()

    # 
    win.

    # configure processor
    processor = FrameProcessor()

    # build window manager based on processor
    win = WindowManager(processor)

    # run the program
    while 1:
        frame get_new_frame()
        win.flip()