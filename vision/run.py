'''Searches for entities until killed.  Mainly a test script for vision.

The entity argument is the name of the entity to search for.  The camera name
argument should be the name of an SVR stream.  If the -c option is used, the
camera is opened directly instead of using SVR.  Multiple cameras should be
given for binocular entities.

'''

import sys
if sys.version_info < (2, 6):
    raise RuntimeError("Python version 2.6 or greater required.")
from optparse import OptionParser

import entities
import process_manager

#spawn a process manager, and start the correct vision process

if __name__ == "__main__":

    opt_parser = OptionParser(
        usage="%prog [options] entity camera_name",
        description=__doc__,
    )
    opt_parser.add_option("-s", "--single-process", action="store_true",
        dest="single_process", default=False,
        help="Do not run a subprocess for vision processing.  This is useful "
            "for debugging, but it isn't the way which mission control "
            "interacts with vision.")
    opt_parser.add_option("-c", "--camera", nargs=2, action="append",
        type="string", metavar="<camera> <index/filename>",
        dest="cameras", default=[],
        help="Specifies that the camera given should use the given index or "
            "file to capture its frames.  If this option is not given for a "
            "camera, SVR is used.")
    opt_parser.add_option("-d", "--delay", type="int",
        dest="delay", default=10,
        help="Delay between frames, in milliseconds, or -1 to wait for "
            "keypress.  Default is 10.")
    opt_parser.add_option("-G", "--non-graphical", action="store_false",
        dest="graphical", default=True,
        help="Turns off debug mode so no graphical windows are displayed.")

    options, args = opt_parser.parse_args()
    if len(args) == 0:
        opt_parser.error("No entity given!  Valid entities are: "+str(entities.entity_classes.keys()))
    elif len(args) == 1:
        opt_parser.error("No camera given!")
    if options.single_process:
        opt_parser.error("Single process has not been implemented! ):")
    entity_name = args[0]
    camera_names = args[1:]

    # Put camera option into dictionary format
    cameras_dict = {}
    for name, index in options.cameras:
        cameras_dict[name] = index

    #spawn a process manager
    pm = process_manager.ProcessManager(extra_kwargs={
        "cameras": cameras_dict,
        "delay": options.delay,
        "debug": options.graphical,
    })

    #start the requested vision entity
    pm.start_process(
        entities.entity_classes[entity_name],
        entity_name,
        *camera_names
    )

    try:
        while True:
            #for debugging, print out entity output
            output = pm.get_data()
            if output:
                print output

    except process_manager.KillSignal:
        # Exit if the subprocess tells us to
        pass
    except Exception:
        pm.kill()
        raise
