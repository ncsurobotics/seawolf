
import multiprocessing

try:
    import cv
except ImportError:
    raise ImportError('''\n
Error: Could not import library "cv" (opencv).
    Make sure the new OpenCV Python interface is installed (not the old SWIG
    interface).
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
    >>> while searcher.is_alive():
    >>>     entity = searcher.get_entity()
    >>>     if entity:
    >>>         print "Found Entity:", entity

    EntitySearcher works by starting a subprocess that does the work.  Note
    that in the example, is_alive is called periodically to make sure the
    subprocess is still alive.

    '''

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

        # Setup Pipe
        parent_connection, child_connection = multiprocessing.Pipe()

        # Start Search Process
        subprocess = multiprocessing.Process(
            target = EntitySearcher._search_forever_subprocess,
            args = (child_connection,),
            kwargs = kwargs,
        )
        subprocess.start()

        self.pipe = parent_connection
        self.subprocess = subprocess

    def start_search(self, entity_list):
        ''' Begins searching for the entities given in entity_list.

        Any previous entities that were being searched for are forgotten.

        '''
        self.pipe.send(entity_list)

    def get_entity(self, timeout=0):
        '''
        Returns an entity that has been found, if any has been found since
        the last call to get_entity.

        When an entity is found, it is queued up.  get_entity will pop an item
        from that queue, or return None if the queue is empty.

        '''
        if self.pipe.poll(timeout):
            return self.pipe.recv()
        return None

    def is_alive(self):
        '''
        Returns False if the EntitySearcher's subprocess has died, True
        otherwise.

        This should be called periodically if you want to make sure work is
        still being done.
        '''
        return self.subprocess.is_alive()

    @staticmethod
    def _search_forever_subprocess(pipe, camera_indexes={}, is_graphical=True,
        record=True, delay=10):
        '''Searches for entities until killed.

        Positional Arguments:

        pipe - A bidirectional pipe.  The pipe is used to recieve and send:
            Recieve - A list of VisionEntity subclass objects are sent to
                this pipe.  Each time a list is sent, the objects that were
                previously being searched for are erased and replaced by the
                sent
                objects.
            Send - When one of the VisionEntity objects is found, it is sent
                into the pipe.  The VisionEntity object will be timestamped and
                information about the entity's sighting will be included.

        Keyword Arguments:
            All keyward arguments are passed straight from __init__().  They
            are documented in __init__'s documentation.
        '''

        entities = None

        cameras = EntitySearcher._initialize_cameras(camera_indexes,
            is_graphical, record)

        while True:

            # Recieve entitiy list
            if pipe.poll():
                entities = pipe.recv()

            if not entities:
                pipe.poll(None) # Wait for entity list
                continue

            # Get timestamp
            #TODO

            frames = {} # Maps camera names to a frame from that camera
            for entity in entities:

                # Grab Frames
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
                    pipe.send(entity)

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

    @staticmethod
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
