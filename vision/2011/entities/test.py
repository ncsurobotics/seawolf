
import time
from random import choice

import cv

from entities.base import VisionEntity

class Test(VisionEntity):
    '''A test entity for reference, education, and debugging.

    If you want to learn how to write a vision entity, you should read the
    documentation in the VisionEntity class (in base.py).  Then, if everything
    is not clear, you should read through this and use it as an example.

    '''

    name = "Test"
    camera_name = "down"

    def find(self, frame, debug=False):

        # Process the frame
        # We just sleep and act like we're processing
        time.sleep(0.1)

        # Debug info is written to the frame and displayed, but ONLY if
        # debug=True.  Do NOT write to the frame if debug=False.
        if debug:
            font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, .5, .5)
            cv.PutText(frame, "Debug info goes here!", (0, frame.height-100), font, (0,0,0))

        # Did we see the entity?
        # return True or False
        return choice([True, False])
