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

try:
    import seawolf
except ImportError:
    raise ImportError('''\n
Error: Could not import library "seawolf".
    Make sure the libseawolf python bindings are installed.
''')

import entities
from camera import Camera


def search_forever(pipe, camera_indexes={}, is_graphical=True, record=True):
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

    '''

    entities = None

    # Initialize all cameras
    cameras = {}
    for name, index in camera_indexes.iteritems():
        cameras[name] = Camera(index, display=is_graphical, record=record)

    while True:

        # Recieve entitiy list
        if pipe.poll():
            entities = pipe.recv()
        
        if not entities:
            pipe.poll(None) # Wait for entity list
            continue

        # Get timestamp
        #TODO

        # Grab Frame
        frames = {} # Maps camera names to a frame from that camera
        for entity in entities:
            if entity.camera_name not in cameras:
                raise IndexError('Camera "%s" needed for entity "%s", but no '
                'camera index specified.' % (entity.camera_name, entity))
            camera = cameras[entity.camera_name]
            frame = camera.get_frame()
            frames[entity.camera_name] = frame

        # Search for each entity
        for entity in entities:
            if entity.find(frames[entity.camera_name]):
                #TODO: Timestamp the object
                pipe.send(entity)

        key = cv.WaitKey(10)
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
    options, args = opt_parser.parse_args()
    if len(args) < 1:
        opt_parser.error("At least one entity must be specified.")

    # Get entities to search for
    entities_to_search_for = []
    for arg in args:
        if arg not in entities.entity_classes.keys():
            opt_parser.error('Given entity "%s" is not one of: %s' %
            (arg, entities.entity_classes.keys()))
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
