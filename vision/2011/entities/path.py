
import time
from random import choice

import cv

from entities.base import VisionEntity

class Path(VisionEntity):

    name = "Path"
    camera_name = "down"

    def find(self, frame, debug=False):

        # Debug Info
        if debug:
            font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, .5, .5)
            cv.PutText(frame, "Debug info goes here!", (0, frame.height-100), font, (0,0,0))

        # Did we see entity?
        time.sleep(0.1)
        return choice([True, False])
