
'''
The main Seawolf mission control script.
'''

import sys
from optparse import OptionParser

try:
    import seawolf
except ImportError as e:
    print
    print 'Error: Could not import library "seawolf".'
    print "    Make sure the libseawolf python bindings are installed."

if __name__ == "__main__":

    # Parse Arguments
    opt_parser = OptionParser()
    opt_parser.add_option("-i", "--initial-mission", action="store", default=0,
        dest="initial_mission", help="Specifies a mission index to start at.")
    #opt_parser.add_option("-w", "--wait-for-go", action="store_true",
    options, args = opt_parser.parse_args(sys.argv)

    # Option Checking
    try:
        options.initial_mission = int(options.initial_mission)
    except ValueError:
        print "\nError: argument to --initial-mission must be an integer.\n"
        opt_parser.print_help()
        sys.exit(1)

    # libseawolf init
    seawolf.loadConfig("../../conf/seawolf.conf")
    seawolf.init("Vision")
    seawolf.notify.filter(seawolf.FILTER_ACTION, "GO")

    if options.graphical:
        highgui.cvNamedWindow("Heading", highgui.CV_WINDOW_AUTOSIZE)

    mission_index = options.initial_mission

    # Zero Heading
    #TODO

    # Set Reference Angle
    #TODO

    while True:

        if seawolf.var.get("VisionReset"):
            seawolf.var.set("VisionReset", 0.0)
            mission_index = options.initial_mission
            #TODO: Zero heading
            #TODO: Finish this

        if not mission_object:
            mission_object = None #TODO: Get mission object from mission list

        mission_object.step()

        #TODO
        #seawolf.logging.log("Theta=%s, Phi=%s, Rho=%s\n" % (theta, phi, rho))

        #TODO: Delay

    seawolf.close()
