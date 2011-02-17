
import cv

class VisionEntity(object):
    '''Defines an entity, or object that can be located.
    
    Subclasses must:
        - Implement a find() method.
    Subclasses should:
        - Implement a __repr__() method.
        - Implement a initialize_non_pickleable() method.
        - Contain useful information about the entity's location.
        
    '''

    # A human readable name for this entity
    name = "VisionEntity"

    # Camera to look through when finding this entity.  Frames from this camera
    # will be passed to VisionEntity.find().  Subclasses MUST specify a camera.
    #
    # The camera name should be a string.
    camera_name = None

    def find(self, frame, debug=True):
        '''Find the VisionEntity in the given frame.

        Whenever find() returns True, the entity's object is sent to mission
        logic.

        Arguments:
            frame - The image from the camera specified in
                VisionEntity.camera_name that may or may not contain the entity
                being searched for.
            debug - If True, debugging information should be written to the
                frame.

        Returns true when the entity is seen.  When the entity is seen, find()
        also records information in the object about where the entity was seen.  
        See test.py for a simple, well documented example of how to write a
        vision entity.

        '''
        raise NotImplementedError("This subclass must be implemented!")

    def __repr__(self):
        return "<%s>" % self.name

    def create_trackbar(self, var, max=255):
        '''Function to create trackbar for a variable.

        Arguments:
            var - The variable name to create a trackbar for.  The variable
                name must be already defined as self.<variable name> and
                initialized to some value.
            max - The maximum value the trackbar can slide to.  Min is always
                zero.

        '''
        cv.CreateTrackbar("%s" % var, self.name, getattr(self, var), max,
            lambda value: setattr(self, var, value))

    def initialize_non_pickleable(self, debug=True):
        '''Called once after the object is created.

        __init__() cannot be used to initialize non-pickleable data, since the
        object is usually pickled and sent to a subprocess before use.  This
        function is for doing things such as opening file handles, initializing
        graphics, and other things that don't transfer when the object is
        pickled.

        Arguments:
            debug - If True, no graphical windows should be displayed.

        '''
        pass
