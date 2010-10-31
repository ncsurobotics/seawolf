
try:
    from interface import *
except ImportError as e:
    print
    print "Error: Could not import the c interface."
    print "       Have you successfully built the c interface?"
    print '       Go into the libvision/c/ directory and run "scons".'
    print
    raise

try:
    from opencv import highgui 
except ImportError as e:
    print
    print "Error: Could not import opencv.highgui"
    print "       - Have you installed the OpenCV SWIG interface for python?"
    print "       - Have you added the OpenCV SWIG interface directory to"
    print "         the PYTHONPATH?"
    raise
