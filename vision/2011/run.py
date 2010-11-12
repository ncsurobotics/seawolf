
import sys
from optparse import OptionParser

from opencv import highgui
import seawolf

# Parse Arguments
opt_parser = OptionParser()
opt_parser.add_option("-n", "--non-graphical", action="store_false",
    default="true", dest="graphical",
    help="Indicates that no graphical windows will be displayed.  This is "
    "needed if you want to disconnect and let the robot run autonomously.")
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
print options

# libseawolf init
'''
seawolf.loadConfig("../../conf/seawolf.conf")
seawolf.init("Vision")
seawolf.notify.filter(seawolf.FILTER_ACTION, "GO")
'''

# Setup Cameras
#TODO

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

    #TODO
    #seawolf.logging.log("Theta=%s, Phi=%s, Rho=%s\n" % (theta, phi, rho))

seawolf.close()
