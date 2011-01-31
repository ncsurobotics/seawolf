'''
Provides the subprocess framework for searching for vision entities.

When run as a script, a simple searching loop is entered.  For more informaion,
use the --help option.

This module provides the search_forever() function, which is started as a
subprocess in order to run the vision system.
'''

import sys

if sys.version_info < (2, 6):
    raise RuntimeError("Python version 2.6 or greater required.")

import multiprocessing
import time
from optparse import OptionParser

try:
    import cv
except ImportError:
    raise ImportError('''\n
Error: Could not import library "cv" (opencv).
    Make sure the new OpenCV Python interface is installed (not the old SWIG
    interface).
''')

import entities
from libvision import Camera


def search_forever(pipe, camera_indexes={}, is_graphical=True, record=True, delay=10):
    '''Searches for entities until killed.

    This is meant to be used via the python multiprocessing module.
    When a list of VisionEntity subclass objects is recieved through
    the pipe, this process starts searching for those entities.

    Arguments:

    camera_indexes - A dictionary mapping camera names to camera indexes to be
        passed to the Camera class.

    pipe - A bidirectional pipe.  The pipe is used to recieve and send:
        Recieve - A list of VisionEntity subclass objects are sent to
            this pipe.  Each time a list is sent, the objects that were
            previously being searched for are erased and replaced by the sent
            objects.
        Send - When one of the VisionEntity objects is found, it is sent into
            the pipe.  The VisionEntity object will be timestamped and
            information about the entity's sighting will be included.

    is_graphical - If this evaluates to True, graphical windows will be
        displayed with debugging information.

    record - If this evaluates to True, all images grabbed from cameras will be
        recorded.

    delay - The delay between frames, in milliseconds.  If -1, it waits for a
        keypress between frames.

    '''

    entities = None

    # Initialize all cameras
    cameras = {}
    for name, index in camera_indexes.iteritems():
        cameras[name] = Camera(index, display=is_graphical, window_name=name,
                               record=record)

        # This is specific to seawolf's IMI-Tech camera.  OpenCV sets the
        # capture mode to greyscale, and this line sets the mode back to color
        # if the camera index is firewire (indexes 300-400).
        cameras[name].open_capture()
        if isinstance(cameras[name].identifier, int) and \
           cameras[name].identifier >= 300 and cameras[name].identifier < 400:

            cameras[name].open_capture()
            # The cap prop mode 67 comes from a libdc1394 enumeration.  You can
            # find a list of possible values inside the libdc1394 source code.
            # See file "dc1394/types.h" and enumeration "dc1394video_mode_t"
            # (version 2 of dc1394).  Remember that if a number is not
            # specified in an enumeration, ANSI C specifies that it takes on
            # the value of the previous value plus one.
            DC1394_VIDEO_MODE_640x480_YUV422 = 67
            cv.SetCaptureProperty(cameras[name].capture, cv.CV_CAP_PROP_MODE,
                DC1394_VIDEO_MODE_640x480_YUV422
            )

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
                raise IndexError('Camera "%s" needed for entity "%s", but no '
                'camera index specified.' % (entity.camera_name, entity))
            camera = cameras[entity.camera_name]
            frame = camera.get_frame()
            frames[entity.camera_name] = frame

        for entity in entities:

            if is_graphical:
                cv.NamedWindow("%s" %entity.name)
                frame = cv.CloneImage(frames[entity.camera_name])
            else:
                # No need to copy frame.  VisionEntity.find() is not allowed to
                # edit the frame if we give it debug=False.
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
                #TODO: Would be cleaner to not create the window every frame.
                #TODO: Destroy windows when entity list changes. (if we care)
                cv.ShowImage("%s" % entity.name, frame)

        key = cv.WaitKey(delay)
        if key == 27:
            break

def start_search_forever_subprocess(**kwargs):
    '''A helper function to run search_forever() in a subprocess.

    There are no positional arguments.  Keyward arguments are passed through to
    search_forever().

    Returns a tuple containing the process object and a bidirectional pipe to
    communicate with the created subprocess.

    '''

    # Setup Pipe
    parent_connection, child_connection = multiprocessing.Pipe()

    # Start Search Process
    process = multiprocessing.Process(
        target = search_forever,
        args = (child_connection,),
        kwargs = kwargs,
    )
    process.start()

    return process, parent_connection

def main():
    '''A simple look for interacting with a search_forever() process.

    This is a good simple example of how to use search_forever() and
    start_search_forever_subprocess().

    '''

    # Parse Arguments
    #TODO: Convert optparse to argparse?
    opt_parser = OptionParser(
        usage="%prog [options] entity[, ...]",
        description="Searches for the entities that are given until killed.  "
        "Multiple entities may be given.  Entities must be one of: %s" %
        entities.entity_classes.keys(),
    )
    opt_parser.add_option("-g", "--graphical", action="store_true",
        dest="graphical",
        help="Indicates that graphical windows can be displayed.")
    opt_parser.add_option("-G", "--non-graphical", action="store_false",
        default="true", dest="graphical",
        help="Indicates that no graphical windows will be displayed.")
    opt_parser.add_option("-r", "--record", action="store_true",
        default="true", dest="record",
        help="All images captured from cameras will be recorded.")
    opt_parser.add_option("-R", "--not-record", action="store_false",
        dest="record",
        help="Images captured from cameras will not be recorded.")
    opt_parser.add_option("-c", "--camera", nargs=2, action="append",
        type="string", metavar="<camera> <index/filename>",
        dest="cameras", default=[],
        help="Specifies that the camera given should use the given index or "
            "file to capture its frames.  Camera names should be one of: %s" %
            entities.get_all_used_cameras())
    opt_parser.add_option("-d", "--delay", type="int",
        dest="delay", default=10,
        help="Delay between frames, in milliseconds, or -1 to wait for "
            "keypress")

    options, args = opt_parser.parse_args()
    if len(args) < 1:
        opt_parser.error("At least one entity must be specified.")
    if not options.cameras:
        opt_parser.error("Use the -c option to specify at least one camera.")

    # Get entities to search for
    entities_to_search_for = []
    for arg in args:
        if arg not in entities.entity_classes.keys():
            opt_parser.error('Given entity "%s" is not one of the defined '
                    'entities: %s' % (arg, entities.entity_classes.keys()))
        EntityClass = entities.entity_classes[arg]
        entities_to_search_for.append(EntityClass())

    # Put camera option into dictionary format
    camera_dict = {}
    for camera_name, camera_index in options.cameras:
        camera_dict[camera_name] = camera_index

    # Start subprocess
    process, pipe = start_search_forever_subprocess(
        camera_indexes=camera_dict,
        is_graphical=options.graphical,
        record=options.record,
        delay=options.delay,
    )

    # Send a list of entities for search_forever() to look for
    pipe.send(entities_to_search_for)

    # Print entity when subprocess sees it
    while True:
        if pipe.poll(0.1):
            entity = pipe.recv()
            print "Found Entity:", entity
        elif not process.is_alive(): # See if subprocess is alive every 0.1s
            break

if __name__ == "__main__":
    main()
