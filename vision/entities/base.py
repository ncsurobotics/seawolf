
import os

import libvision
import vision
import svr

import cv


class Container(object):
    """ a blank container object """

    def __repr__(self):
        return str(self.__dict__)


class VisionEntity(object):
    """
    Defines an entity, an object that can be located.

    Subclasses must:
        - Implement a find() method.
    Subclasses should:
        - Implement a __repr__() method.

    """

    # A human readable name for this entity
    name = "VisionEntity"

    def __init__(self, child_conn, camera_name, *args, **kwargs):

        self.cameras = kwargs.pop('cameras', {})
        self.debug = kwargs.pop('debug', False)
        self.delay = kwargs.pop('delay', 0)
        self.waitforsync = kwargs.pop('waitforsync', False)
        self.binocular_child = kwargs.pop('binocularworker', False)

        # Line of communication to mission control
        self.child_conn = child_conn

        # Open camera
        self.camera_name = camera_name
        if self.camera_name in self.cameras:
            self.capture = libvision.Camera(self.cameras[self.camera_name], display=self.debug)
        else:
            self.capture = svr.Stream(self.camera_name)
            self.capture.unpause()

        self.output = Container()

        # Initialization for subclass
        self.init()

    def init(self):
        """ subclass-modified init class """
        pass

    def run(self):
        """ handles running of this entity.  Interfaces with cameras, and manages
            connections.  """

        record_path = get_record_path()

        try:

            while(True):

                #if sync required, do not continue until we receive a message
                if self.waitforsync:
                    signal = self.wait_for_parent(None)

                    if isinstance(signal, CaptureFrameSignal):
                        #there's our signal
                        pass
                    else:
                        #passed signal at the wrong time
                        raise ValueError("Expecting CaptureFrameSignal or KillSignal")

                #else, simply check for kill signal
                elif self.child_conn.poll():
                    signal = self.child_conn.recv()
                    if isinstance(signal, vision.process_manager.KillSignal):
                        self.close()
                        return

                # Tell mission control we are capturing a frame, and it should capture sensor data
                if not self.binocular_child:
                    self.child_conn.send(vision.process_manager.SensorCapture())

                #check if a new frame has been captured
                frame = self.capture.get_frame()

                #process any new frame
                self.process_frame(frame)

                #wait for gui process
                if self.delay != 0 and cv.WaitKey(self.delay) == ord('q'):
                    self.close()
                    return

        # Always close camera, even if an exception was raised
        finally:
            self.close()

    def return_output(self):
        #return output
        self.child_conn.send(self.output)

    def wait_for_parent(self, timeout):
        if self.child_conn.poll(timeout):
            signal = self.child_conn.recv()
        else:
            signal = None

        #check if signal passed was kill signal
        if isinstance(signal, vision.process_manager.KillSignal):
            self.close()
            raise signal

        return signal

    def close(self):
        self.child_conn.send(vision.process_manager.KillSignal())
        self.capture = None

    def send_message(self, data):
        self.child_conn.send(data)

    def process_frame(self, frame, debug=True):
        """ process this frame, then place output in self.output """

        raise NotImplementedError("The find subclass must be implemented!")

    def create_trackbar(self, var, max=255):
        """ Function to create trackbar for a variable.

        Arguments:
            var - The variable name to create a trackbar for.  The variable
                name must be already defined as self.<variable name> and
                initialized to some value.
            max - The maximum value the trackbar can slide to.  Min is always
                zero.

        """
        cv.CreateTrackbar("%s" % var, self.name, getattr(self, var), max,
            lambda value: setattr(self, var, value))


class MultiCameraVisionEntity(VisionEntity):
    """ spawns and communicates with subprocess, each of which controls a camera """
    subprocess = None

    def __init__(self, child_conn, *cameras_to_use, **kwargs):

        self.cameras = kwargs.pop('cameras', {})  # Camera index dict
        self.debug = kwargs.pop('debug', False)
        self.delay = kwargs.pop('delay', 0)

        #Communication to the process manager
        self.child_conn = child_conn

        #start a process manager to handle sub-processes
        self.process_manager = vision.process_manager.ProcessManager()

        #store the cameras.  Order will determine camera positions First is left, second is right
        self.cameras_to_use = cameras_to_use

        #start a subprocess for every camera
        for camera_name in cameras_to_use:
            self.process_manager.start_process(
                            self.subprocess,
                            camera_name,
                            camera_name,
                            debug=self.debug,
                            delay=self.delay,
                            cameras=self.cameras,
                            waitforsync=True,
                            binocularworker=True,
            )

        self.output = Container()

        #perform additional initialization steps
        self.init()
        pass

    def run(self):
        """ handles running of this entity.  Interfaces with subprocesses, and manages
            connections. """

        try:

            while(True):

                #check for a kill signal from above
                if self.child_conn.poll():
                    if isinstance(self.child_conn.recv(), vision.process_manager.KillSignal):
                        self.process_manager.kill()
                        break

                #walk workers through processing a frame
                self.manage_workers()

                # Tell mission control we are capturing a frame, and it should capture sensor data
                self.child_conn.send(vision.process_manager.SensorCapture())

                self.child_conn.send(self.output)

        # Always close camera, even if an exception was raised
        finally:
            self.process_manager.kill()
            self.child_conn.send(vision.process_manager.KillSignal())

    def sync_capture(self):
        #send frame sync
        for process in self.process_manager.process_list.values():
            process.send_data(CaptureFrameSignal())

    def wait_for_workers(self):
        #wait for workers all workers to return data
        try:
            data = self.process_manager.get_data(force=True)
        except vision.process_manager.KillSignal:
            self.child_conn.send(vision.process_manager.KillSignal())
            raise
        return data

    def manage_workers(self):
        raise NotImplementedError()

class CaptureFrameSignal():
    """ used to send frame sync signals to subprocesses """
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
