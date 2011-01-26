
import time
from random import choice, randrange

import cv

from entities.base import VisionEntity

class ExampleEntity(VisionEntity):
    '''An example entity for reference, education, and debugging.

    If you want to learn how to write a vision entity, you should read the
    documentation in the VisionEntity class (in base.py).  Then, if everything
    is not clear, you should read through this and use it as an example.

    '''

    name = "Example"

    # camera_name is the name of the camera you want to look through to search
    # for this entity (must be a string).  The name can actually be any string
    # you want, but the user will need to specify an index corresponding to the
    # camera, or an exception will be raised.
    #
    # Before you go making up your own camera names, you can look at the camera
    # names already used by entities by running:
    #  $ python run.py -h
    # The help description for the -c option lists used camera names.
    camera_name = "down"

    def __init__(self):

        # The entity should contain some information about position or
        # orientation.  __init__ will initialize those variables to None until
        # the entity is seen.
        self.position = None

        # Note that __init__ should only be used to initialize pickleable data.
        # The object will be initialized, pickled, then used, so anything such
        # as graphics initialization should not be done in __init__.  Instead,
        # you should define a self.initialize_non_pickleable() function.

    def find(self, frame, debug=True):

        # Process the frame
        # We just sleep and act like we're processing.
        time.sleep(0.1)

        # Debug info is written to the frame and displayed, but ONLY if
        # debug=True.  Do NOT modify the frame if debug=False, because the
        # frame could be reused elsewhere.
        if debug:
            font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, .5, .5)
            cv.PutText(frame, "Debug info goes here!", (0, frame.height-100), font, (0,0,0))

        is_seen = choice([True, False])

        # If the object was seen, we set some location/orientation informaion
        # and return True.  This object will be sent to mission control
        # whenever find() returns True, and it will use the information such as
        # self.position.
        if is_seen:
            self.position = randrange(0, 100)

        return is_seen

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return "<ExampleEntity position=%s>" % self.position
