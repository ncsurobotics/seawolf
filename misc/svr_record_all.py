
from __future__ import division
from sys import argv
from time import time
import os.path
import cv
import cv2
import svr
svr.connect()

open_streams = {} # Map stream names to stream objects
stream_directories = {}  # Map stream names to recording directories
stream_framecounts = {}  # Map stream names to number of frames recorded
SOURCES_UPDATE_FREQUENCY = 5  # How many times per second to update sources
last_sources_update = 0  # Last time that the open_streams was updated

def get_next_dir(base_dir, prefix=""):
    '''Find the next directory base_dir+prefix+i that isn't taken.'''
    i=0
    while True:
        candidate = os.path.join(base_dir, prefix+str(i))
        if not os.path.exists(candidate):
            break
        i += 1
    os.mkdir(candidate)
    return candidate

if __name__ == "__main__":

    base_dir = argv[1]
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    capture_dir = get_next_dir(base_dir)

    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    while True:

        # Rate limit stream listing
        t = time()
        if t > last_sources_update + 1/SOURCES_UPDATE_FREQUENCY:
            last_sources_update = t

            # Add new streams to open_streams
            all_streams = svr.get_sources_list()
            for stream in all_streams:
                stream_name = stream.split(":")[1]
                if stream_name not in open_streams:
                    try:

                        # New stream
                        open_streams[stream_name] = svr.Stream(stream_name)
                        open_streams[stream_name].unpause()
                        stream_directories[stream_name] = get_next_dir(capture_dir, stream_name)
                        stream_framecounts[stream_name] = 0
                        print "Stream Opened:", stream_name

                    except svr.StreamException:

                        # Closed Stream
                        if stream_name in open_streams:
                            del open_streams[stream_name]
                            del stream_directories[stream_name]
                            del stream_framecounts[stream_name]
                            print "Stream Closed:", stream_name

        # Record streams
        for stream_name, stream in open_streams.items():  # Cannot be iter because
                                                        # dict is mutated in loop
            frame = None
            try:
                frame = stream.get_frame(False)
            except svr.OrphanStreamException:

                # Closed Stream
                del open_streams[stream_name]
                del stream_directories[stream_name]
                del stream_framecounts[stream_name]
                print "Stream Closed:", stream_name

            if frame:
                filename = os.path.join(
                    stream_directories[stream_name],
                    "%i.jpg" % stream_framecounts[stream_name]
                )
                cv.SaveImage(filename, frame)
                stream_framecounts[stream_name] += 1
