
import sys
if sys.version_info < (2, 6):
    raise RuntimeError("Python version 2.6 or greater required.")

import multiprocessing
from time import time

try:
    import cv
except ImportError:
    raise ImportError('''\n
Error: Could not import library "cv" (opencv).
    Make sure the new OpenCV Python interface is installed.  The path where it
    was installed must be inside sys.path, or else you will need to add the
    directory to the PYTHONPATH environment variable.
''')


from libvision import Camera

class EntitySearcher(object):
    '''
    Searches for entities through camera(s).

    The searcher will start by waiting for start_search() to be called.  After
    start_search() is called, get_entity() can be called to see if the searcher
    has found any entities.

    >>> searcher = EntitySearcher()
    >>> searcher.start_search(ExampleEntity())
    >>> while True:
    >>>     entity = searcher.get_entity()
    >>>     print "Found Entity:", entity

    EntitySearcher works by starting a subprocess that does the work.
    '''

    # Ping and panic intervals for the ProcessPinger objects.
    ping_interval = 1
    panic_interval = 3

    def __init__(self, **kwargs):
        '''

        Keyword Arguments:

        camera_indexes - A dictionary mapping camera names to camera indexes to
            be passed to the Camera class.

        is_graphical - If this evaluates to True, graphical windows will be
            displayed with debugging information.

        record - If this evaluates to True, all images grabbed from cameras
            will be recorded.

        delay - The delay between frames, in milliseconds.  If -1, it waits for
            a keypress between frames.
        '''

        # Setup Pipes
        parent_entity_connection, child_entity_connection = multiprocessing.Pipe()
        parent_ping_connection, child_ping_connection = multiprocessing.Pipe()
        self.entity_pipe = parent_entity_connection
        self.ping_pipe = parent_ping_connection

        # Set up ProcessPinger
        if "delay" in kwargs and \
           kwargs["delay"] > EntitySearcher.ping_interval*1000:
            raise ValueError("delay must be less than the ping interval.")
        self.pinger = ProcessPinger(self.ping_pipe,
            EntitySearcher.ping_interval, EntitySearcher.panic_interval)

        # Start Search Process
        self.subprocess = multiprocessing.Process(
            target = _search_forever_subprocess,
            args = (child_entity_connection, child_ping_connection),
            kwargs = kwargs,
        )
        self.subprocess.start()

    def start_search(self, entity_list):
        ''' Begins searching for the entities given in entity_list.

        Any previous entities that were being searched for are forgotten.

        '''
        self.entity_pipe.send(entity_list)

    def ping(self):
        '''Pings the subprocess.

        Either this or get_entity() must be called every ping_interval seconds,
        or the subprocess could think that this process has died.

        Returns True if the other process is ok, False otherwise.
        
        '''
        return self.pinger.ping()

    def get_entity(self, timeout=None):
        '''
        Returns an entity that has been found, if any has been found since
        the last call to get_entity.

        When an entity is found, it is queued up.  get_entity will pop an item
        from that queue, or return None if the queue is empty.

        Either this or get_entity() must be called every ping_interval seconds,
        or the subprocess could think that this process has died.

        Arguments:

        timeout - If None (default) then get_entity() blocks until an entity is
            available.  Otherwise timeout should be a number that specifies how
            many seconds to wait for an entity to be available.  If no entity
            is found, None is returned.

        '''

        if timeout is None:

            while True:
                if not self.ping() or not self.is_alive():
                    self.panic()
                if self.entity_pipe.poll(0.2):
                    return self.entity_pipe.recv()

        else:

            if not self.ping() or not self.is_alive():
                self.panic()

            #TODO: Must keep pinging if timeout > self.ping_interval.  This
            #      isn't a huge deal because get_entity isn't actually used
            #      like that.
            if self.entity_pipe.poll(timeout):
                return self.entity_pipe.recv()
            return None

    def is_alive(self):
        '''
        Returns False if the EntitySearcher's subprocess has died, True
        otherwise.

        get_entity() automatically checks this whenever it is called.
        '''
        return self.subprocess.is_alive()

    def panic(self):
        raise IOError("EntitySearcher superprocess lost connection with subprocess!")


def _search_forever_subprocess(entity_pipe, ping_pipe, camera_indexes={},
    is_graphical=True, record=True, delay=10):
    '''Searches for entities until killed.

    Positional Arguments:

    entity_pipe - A bidirectional pipe used to send entities:
        Recieve - A list of VisionEntity subclass objects are sent to
            this pipe.  Each time a list is sent, the objects that were
            previously being searched for are erased and replaced by the
            sent
            objects.
        Send - When one of the VisionEntity objects is found, it is sent
            into the pipe.  The VisionEntity object will be timestamped and
            information about the entity's sighting will be included.

    ping_pipe - TODO

    Keyword Arguments:
        All keyward arguments are passed straight from
        EntitySearcher.__init__().  They are documented in
        EntitySearcher.__init__'s documentation.
    '''

    entities = None

    cameras = _initialize_cameras(camera_indexes,
        is_graphical, record)

    pinger = ProcessPinger(ping_pipe, EntitySearcher.ping_interval,
        EntitySearcher.panic_interval)

    while True:
        if not pinger.ping():
            raise IOError("EntitySearcher subprocess lost connection with superprocess!")

        # Recieve entitiy list
        if entities:
            timeout = 0
        else:
            timeout = EntitySearcher.ping_interval
        if entity_pipe.poll(timeout):
            entities = entity_pipe.recv()

        # Get timestamp
        #TODO

        # Grab Frames
        frames = {} # Maps camera names to a frame from that camera
        for entity in entities:
            if entity.camera_name not in cameras:
                raise IndexError(
                    'Camera "%s" needed for entity "%s", but no camera '
                    'index specified.' % (entity.camera_name, entity))
            camera = cameras[entity.camera_name]
            frame = camera.get_frame()
            frames[entity.camera_name] = frame

        for entity in entities:

            if is_graphical:
                cv.NamedWindow("%s" %entity.name)
                frame = cv.CloneImage(frames[entity.camera_name])
            else:
                # No need to copy frame.  VisionEntity.find() is not
                # allowed to edit the frame if we give it debug=False.
                frame = frames[entity.camera_name]

            # Initialize nonpickleable if object is new
            if not hasattr(entity, "non_pickleable_initialized"):
                entity.initialize_non_pickleable(is_graphical)
                entity.non_pickleable_initialized = True

            # Search for each entity
            if entity.find(frame, debug=is_graphical):
                #TODO: Timestamp the object
                entity_pipe.send(entity)

            # Debug window for this entity
            if is_graphical:
                #TODO: Would be cleaner to not create the window every
                #      frame.
                #TODO: Destroy windows when entity list changes. (if we
                #      care)
                cv.ShowImage("%s" % entity.name, frame)

        key = cv.WaitKey(delay)
        if key == 27:
            break

def _initialize_cameras(camera_indexes, display, record):
    '''
    Returns a dictionary mapping camera names to libvision.Camera objects.

    Arguments:
        camera_indexes - A dictionary mapping camera names to camera
            identifiers
        display - If True, displays a window for each camera when a frame
            is grabbed.
        record - If True, records every frame grabbed from a camera.
    '''

    cameras = {}
    for name, index in camera_indexes.iteritems():
        cameras[name] = Camera(index, display=display,
            window_name=name, record=record)

        # This is specific to seawolf's IMI-Tech camera.  OpenCV sets the
        # capture mode to greyscale, and this line sets the mode back to
        # color if the camera index is firewire (indexes 300-400).
        cameras[name].open_capture()
        if isinstance(cameras[name].identifier, int) and \
           cameras[name].identifier >= 300 and \
           cameras[name].identifier < 400:

            cameras[name].open_capture()
            # The cap prop mode 67 comes from a libdc1394 enumeration.  You
            # can find a list of possible values inside the libdc1394
            # source code.  See file "dc1394/types.h" and enumeration
            # "dc1394video_mode_t" (version 2 of dc1394).  Remember that if
            # a number is not specified in an enumeration, ANSI C specifies
            # that it takes on the value of the previous value plus one.
            DC1394_VIDEO_MODE_640x480_YUV422 = 67
            cv.SetCaptureProperty(cameras[name].capture,
                cv.CV_CAP_PROP_MODE,
                DC1394_VIDEO_MODE_640x480_YUV422
            )

    return cameras


class ProcessPinger(object):
    '''
    Sends and receives pings to make sure the process on the other side of a
    pipe is alive.
    
    There should be one ProcessPinger object on each side of the pipe for this
    process to work.  Timestamps are sent through the pipe and if a timestamp
    is not received on one end of the pipe within panic_interval seconds of the
    last sent timestamp, ping() will return False.

    ping() assumes that the ping_interval of both sides is the same.  For this
    reason, it is probably better for both ProcessPingers to have the same
    ping_interval.  Having a consistent panic_interval however is not as
    important.
    
    '''

    def __init__(self, pipe, ping_interval, panic_interval):
        '''
        Arguments:

        pipe - The pipe which pings will be sent and received.
        ping_interval - Only ping this often (in seconds)
        panic_interval - If no pings have been received for this long (in
            seconds), ping() will return False.

        '''

        self.pipe = pipe
        self.ping_interval = ping_interval
        self.panic_interval = panic_interval

        t = time()
        self.last_ping_sent = t
        self.last_ping_received = t

        self.ping()

    def ping(self):
        '''Sends and receives a ping, but only if the ping_interval has passed.

        Returns True if the other end of the pipe is ok, False otherwise.

        This should be called about every ping_interval seconds or so.  If this
        function is not called every panic_interval seconds, the other end of
        the pipe may panic.

        '''
        t = time()

        # Send if ping_interval has passed
        if t - self.last_ping_sent > self.ping_interval:
            self.pipe.send(t)
            self.last_ping_sent = t

        # Receive if ping_interval has passed
        if t - self.last_ping_received > self.ping_interval:
            while self.pipe.poll():
                self.last_ping_received = self.pipe.recv()

            # Panic if panic_interval has passed
            if t - self.last_ping_received > self.panic_interval:
                return False

        return True
