import process_manager
import libvision
import cv
import os
from fake_svr import FakeSVR

class Container(object):
    '''a blank container object'''

    def __repr__(self):
        return str(self.__dict__)

class VisionEntity(object):
    '''Defines an entity, or object that can be located.

    Subclasses must:
        - Implement a find() method.
    Subclasses should:
        - Implement a __repr__() method.

    '''

    # A human readable name for this entity
    name = "VisionEntity"

    # Camera to open when finding this entity.  Frames from this camera
    # will be passed to VisionEntity.find().  Subclasses MUST specify a camera.
    #
    # The camera name should be a string.
    camera_name = None

    def __init__(self, child_conn, camera_name, *args, **kwargs):

        #the line of communication down which info will be passed
        self.child_conn = child_conn

        #camera of interest
        self.svr = FakeSVR(camera_name)
        
        #handle debug
        self.debug = False
        if "debug" in kwargs and kwargs["debug"] == True:
            self.debug = True
        
        self.output = Container()

        #perform additional initialization steps
        self.init()

    def init(self):
        '''user-modified init class'''
        pass

    def run(self):
        '''handles running of this entity.  Interfaces with cameras, and manages
            connections. '''

        #open specified camera

        record_path = get_record_path()

        try:

            while(True):

                #check for a kill signal
                if self.child_conn.poll():
                   if isinstance(self.child_conn.recv(), process_manager.KillSignal):
                       self.svr.close()
                       return

                #check if a new frame has been captured
                frame = self.svr.get_frame()

                #process any new frame
                self.process_frame(frame)

                #return output
                self.child_conn.send(self.output)

                #wait for gui process
                if cv.WaitKey(10) == ord('q'):
                    self.svr.close()
                    return

        # Always close camera, even if an exception was raised
        finally:
           self.svr.close()
           self.child_conn.send(process_manager.KillSignal())


    def process_frame(self, frame, debug=True):
        ''' process this frame, then place output in self.output'''

        raise NotImplementedError("The find subclass must be implemented!")

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

class MultiCameraVisionEntity(VisionEntity):
    def __init__(self, child_conn, *args, **kwargs):
        '''TODO: initialize multiple cameras '''
        pass

def get_record_path():
    if not os.path.exists("capture"):
        os.mkdir("capture")
    # Find the next index inside capture/ that isn't taken
    i = 0
    while True:
        record_path = os.path.join("capture", str(i))
        if not os.path.exists(record_path):
            break
        i += 1
    return record_path
