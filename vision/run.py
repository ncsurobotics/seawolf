#!/usr/bin/env python

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

from optparse import OptionParser

import entities
from entity_searcher import EntitySearcher, ExitSignal


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
        entity_class = entities.entity_classes[arg]
        entities_to_search_for.append(entity_class())

    # Put camera option into dictionary format
    camera_dict = {}
    for camera_name, camera_index in options.cameras:
        camera_dict[camera_name] = camera_index

    # Start searcher
    entity_searcher = EntitySearcher(
        camera_indexes=camera_dict,
        is_graphical=options.graphical,
        record=options.record,
        delay=options.delay,
    )

    # Send a list of entities for search_forever() to look for
    entity_searcher.start_search(entities_to_search_for)

    # Print entity when subprocess sees it
    try:
        while True:
            entity = entity_searcher.get_entity()
            if entity:
                print "Found Entity:", entity
    except ExitSignal:
        pass

if __name__ == "__main__":
    main()
