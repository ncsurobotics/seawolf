#!/usr/bin/env python

'''Searches for entities until killed.  Mainly a test script for vision.

The entity argument is the name of the entity to search for.  The camera name
argument should be the name of an SVR stream.  If the -c option is used, the
camera is opened directly instead of using SVR.  Multiple cameras should be
given for binocular entities.

'''

import sys
import os.path

# Add repository root to sys.path
parent_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../.."
))
sys.path.append(parent_directory)

import entities
import process_manager
import argparse


def setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("entity",
                        type=str, help="The vision entity to run")

    parser.add_argument('streams', nargs="+",
                        type=str, help='an integer for the accumulator')

    parser.add_argument("-c", "--camera",
                        help="""Specifies the sorce of frames for the entity""",
                        type=str, dest="cameras", default=[], nargs=2, action="append",
                        metavar="<camera> <index/filename>")

    parser.add_argument("-d", "--delay",
                        help="Delay between frames, in milliseconds, or -1 to wait for keypress. Default is 10",
                        type=int, dest="delay", default=10)

    parser.add_argument("-ng", "--non-graphical",
                        help="Turns off debug mode so no graphical windows are displayed.",
                        dest="graphical", default=True, action="store_false")

    parser.add_argument("-s", "--single-process",
                        help="""Do not run a subprocess for vision processing. This is useful
                        for debugging, but it isn't the way which mission control interacts with vision""",
                        dest="single_process", default=False, action="store_true")

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    entity = args.entity                  # get the entity from the argparser
    streams = args.streams                # the video streams to feed to the entity
    cameras_list = args.cameras           # get the cameras from the argparser
    graphical = args.graphical            # whether or not to show the streams
    delay = args.delay                    # delay in between frames
    single_process = args.single_process  # whether to run it in a single process

    if len(cameras_list) < 1:
        # user must provide at least one camera
        parser.error("No camera given!")

    if entity not in entities.entity_classes:
        parser.error("'%s' is not a valid entity. Please check entities.entity_classes for valid names" % entity)

     # convert the camera list to a dictionary format
    cameras = {name: source for name, source in cameras_list}

    if single_process:
        class FakePipe(object):

            def poll(self):
                return None

            def send(self, data):
                print data

        process_manager.run_entity(
            FakePipe(),
            entities.entity_classes[entity],
            *streams,
            cameras=cameras,
            delay=delay,
            debug=graphical
        )

    else:
        # spawn a process manager
        pm = process_manager.ProcessManager(
            extra_kwargs={
                "cameras": cameras,
                "delay": delay,
                "debug": graphical,
            }
        )

        # start the requested vision entity
        pm.start_process(
            entities.entity_classes[entity],
            entity,
            *streams
        )

        try:
            while True:
                output = pm.get_data()
                # for debugging, print out entity output
                if output:
                    print output
        except process_manager.KillSignal:  # Exit if the subprocess tells us to
            pass
        except Exception:
            pm.kill()
            raise


if __name__ == "__main__":
    main()
