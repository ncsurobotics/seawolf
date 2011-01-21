
class VisionEntity(object):
    '''Defines an entity, or object that can be located.'''

    # A human readable name for this entity
    name = "VisionEntity"

    def __init__(self):

        # Cameras to look through when finding this object.
        # Frames from these cameras will be passed to VisionEntity.find().
        camera = None

    def find(self, frames):
        '''Find the VisionEntity in the given frame.

        Returns true when the object is seen.  When an object is seen, find()
        also records information in the object about where the entity was seen.  

        Whenever find() returns True, the object is sent to mission logic.

        '''
        raise NotImplementedError("This subclass must be implemented!")
