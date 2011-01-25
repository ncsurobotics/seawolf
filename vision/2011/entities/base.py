
class VisionEntity(object):
    '''Defines an entity, or object that can be located.'''

    # A human readable name for this entity
    name = "VisionEntity"

    # Camera to look through when finding this entity.  Frames from this camera
    # will be passed to VisionEntity.find().  Subclasses MUST specify a camera.
    #
    # The camera name should be a string.
    camera_name = None

    def find(self, frame, debug=False):
        '''Find the VisionEntity in the given frame.

        Whenever find() returns True, the entity's object is sent to mission logic.

        Arguments:
            frame - The image from the camera specified in
                VisionEntity.camera_name that may or may not contain the entity
                being searched for.
            debug - If True, debugging information may be written to the given
                frame.  The frame will be displayed after the function completes.
                If False, find() is NOT allowed to edit frame!!!

        Returns true when the entity is seen.  When the entity is seen, find()
        also records information in the object about where the entity was seen.  

        See test.py for a simple, well documented example of how to write a
        vision entity.

        '''
        raise NotImplementedError("This subclass must be implemented!")

    def __repr__(self):
        return "<%s>" % self.name
