import cv
import os

import libvision

CONFIG_FILE = "../cameras.conf"

class FakeSVR(object):
    def __init__(self, camera_name):

        # Read config file to find camera index of this camera.
        # The config file is a standard python file that defines variables
        # which are passed into the local dictionary, defined here as
        # camera_indexes.  After execfile() runs camera_indexes will be a
        # dictionary mapping camera names to camera indexes.
        camera_indexes = {}
        if os.path.exists(CONFIG_FILE):
            execfile(CONFIG_FILE, {}, camera_indexes)
            camera_index = camera_indexes[camera_name]
        else:
            raise IOError("Could not find config file (%s) in current directory" % CONFIG_FILE)

        # Open Camera
        self.camera = libvision.Camera(camera_index)

        if isinstance(self.camera.identifier, int) and self.camera.identifier < 300:
            # Logitech Quickcam Pro 4000
            # These settings should be persistent on the Logitechs, but they
            # might occasionally need to be reset.
            self.camera.open_capture()
            cv.SetCaptureProperty(self.camera.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
            cv.SetCaptureProperty(self.camera.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    def get_frame(self):
        return self.camera.get_frame()

    def close(self):
        return self.camera.close()
    __del__ = close

def debug(name, frame):
    cv.NamedWindow(name)
    cv.ShowImage(name, frame)
