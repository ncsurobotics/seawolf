import process_manager
import libvision
import cv
import os

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

    def __init__(self, child_conn, camera_index, *args, **kwargs):

        #the line of communication down which info will be passed
        self.child_conn = child_conn

        #camera of interest
        self.camera_index = camera_index

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
        camera = libvision.Camera(self.camera_index, record_path=record_path, display=True)
        camera.open_capture()
        if isinstance(camera.identifier, int) and camera.identifier < 300:
            # Logitech Quickcam Pro 4000
            # These settings should be persistent on the Logitechs, but they
            # might occasionally need to be reset.
            cv.SetCaptureProperty(camera.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320);
            cv.SetCaptureProperty(camera.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240);

        try:

            while(True):

                #check for a kill signal
                if self.child_conn.poll():
                   if isinstance(self.child_conn.recv(), process_manager.KillSignal):
                       camera.close()
                       return

                #check if a new frame has been captured
                frame = camera.get_frame()

                #process any new frame
                self.process_frame(frame)

                #return output
                self.child_conn.send(self.output)

        # Always close camera, even if an exception was raised
        finally:
           camera.close()


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
