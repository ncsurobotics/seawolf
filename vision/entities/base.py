
import os

import process_manager
import libvision
from fake_svr import FakeSVR

import cv

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

        #camera name
        self.camera_name = camera_name

        #camera of interest
        self.svr = FakeSVR(self.camera_name)

        if "waitforsync" in kwargs:
            self.waitforsync = kwargs["waitforsync"]
        else:
            self.waitforsync = False
        
        #handle debug
        self.debug = False
        if "debug" in kwargs and kwargs["debug"] == True:
            self.debug = True
            print "Base: self.debug = ",self.debug
        
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

                #if sync required, do not continue until we receive a message
                if self.waitforsync and self.child_conn.poll(None):   
                   signal = self.child_conn.recv()
                   if isinstance(signal, process_manager.KillSignal):
                        self.svr.close()
                        self.child_conn.send(process_manager.KillSignal())
                        return

                   elif isinstance(signal, CaptureFrameSignal):
                        #there's our signal
                        pass

                   else:
                        #passed signal at the wrong time 
                        raise ValueError("Expecting CaptureFrameSignal or KillSignal")

                #else, simply check for kill signal
                elif self.child_conn.poll():
                    signal = self.child_conn.recv()
                    if isinstance(signal, process_manager.KillSignal):
                        self.svr.close()
                        self.child_conn.send(process_manager.KillSignal())
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
                    self.child_conn.send(process_manager.KillSignal())
                    return

        # Always close camera, even if an exception was raised
        finally:
            self.child_conn.send(process_manager.KillSignal())
            self.svr.close()

    def send_message(self, data):
        self.child_conn.send(data)

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
    '''spawns and communicates with subprocess, each of which controls a camera'''
    subprocess = None
    
    def __init__(self, child_conn, *cameras, **kwargs):

        #Communication to the process manager 
        self.child_conn = child_conn

        #start a process manager to handle sub-processes 
        self.process_manager = process_manager.ProcessManager()

        #store the cameras.  Order will determine camera positions
        self.cameras = cameras

        #handle debug
        self.debug = False
        if "debug" in kwargs and kwargs["debug"] == True:
            self.debug = True
            print "Base: self.debug = ",self.debug

        #start a subprocess for every camera
        for camera_name in cameras:
            self.process_manager.start_process(self.subprocess,camera_name,camera_name,debug = self.debug)
        
        self.output = Container()

        #perform additional initialization steps
        self.init()
        pass

    def run(self):
        '''handles running of this entity.  Interfaces with subprocesses, and manages
            connections. '''

        try:

            while(True):

                #check for a kill signal from above
                if self.child_conn.poll():
                   if isinstance(self.child_conn.recv(), process_manager.KillSignal):
                       self.process_manager.kill()
                       break

                #walk workers through processing a frame
                self.manage_workers()

                #return output
                self.child_conn.send(self.output)

                #wait for gui process
                if cv.WaitKey(10) == ord('q'):
                    self.svr.close()
                    break

        # Always close camera, even if an exception was raised
        finally:
           self.process_manager.kill()
           self.child_conn.send(process_manager.KillSignal())
    
    def sync_capture(self):
        #send frame sync
        for process in self.process_manager.process_list.values():
            process.send_data(CaptureFrameSignal())

    def wait_for_workers(self):
        #wait for workers all workers to return data
        data = self.process_manager.get_data(force = True) 
        return data

    def manage_workers(self):
        raise NotImplementedError()

class CaptureFrameSignal():
    '''used to send frame sync signals to subprocesses'''
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
