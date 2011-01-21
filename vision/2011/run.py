
import sys

if sys.version_info < (2, 6):
    raise RuntimeError("Python version 2.6 or greater required.")

import multiprocessing
import time
from optparse import OptionParser

try:
    import cv
except ImportError:
    print '''
Error: Could not import library "cv" (opencv).
    Make sure the new OpenCV Python interface is installed.
    The package may not be installed in the PYTHONPATH by default.
'''
    raise

try:
    import seawolf
except ImportError:
    print '''
Error: Could not import library "seawolf".
    Make sure the libseawolf python bindings are installed.
'''
    raise

import objects


def search_forever(pipe):
    '''Searches for entities until killed.

    This is meant to be used via the python multiprocessing module.
    When a list of VisionEntity subclass objects is recieved through
    the pipe, this process starts searching for those entities.

    Arguments:
    pipe - A bidirectional pipe.
        Recieve - A list of VisionEntity subclass objects are sent to
            this pipe.  The 
        Send - The VisionEntity

    '''

    entities = None

    while True:

        # Recieve entitiy list
        if pipe.poll():
            entities = pipe.recv()
        
        if not entities:
            pipe.poll(None) # Wait for entity list
            continue

        # Get timestamp
        #TODO

        # Grab Frames
        #TODO

        for entity in entities:

            if entity.find(None):
                #TODO: Timestamp the object
                pipe.send(entity)

def main():

    # Parse Arguments
    opt_parser = OptionParser()
    opt_parser.add_option("-n", "--non-graphical", action="store_false",
        default="true", dest="graphical",
        help="Indicates that no graphical windows will be displayed.  This is "
        "needed if you want to disconnect and let the robot run autonomously.")
    #TODO: Finish argument parsing.
    #TODO: Convert optparse to argparse?

    # Get entity to search for
    entities = [objects.Path()] #TODO

    # Setup Pipe
    pipe, child_connection = multiprocessing.Pipe()
    pipe.send(entities)

    # Start Search Process
    search_process = multiprocessing.Process(
        target=search_forever,
        args=(child_connection,),
    )
    search_process.start()

    # Print entity when subprocess sees it
    while True:

        pipe.poll(None) # Wait for object
        entity = pipe.recv()
        print "Found Entity:", entity

if __name__ == "__main__":
    main()
