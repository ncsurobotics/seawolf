'''Show all SVR streams, and show any new streams that appear.'''

from __future__ import division
from time import time

import cv

import svr

svr.connect()

open_streams = {} # Map stream names to stream objects
last_sources_update = 0  # Last time that the open_streams was updated
SOURCES_UPDATE_FREQUENCY = 5  # How many times per second to update sources

if __name__ == "__main__":

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

                        # New Stream
                        open_streams[stream_name] = svr.Stream(stream_name)
                        open_streams[stream_name].unpause()
                        cv.NamedWindow(stream_name)
                        print "Stream Opened:", stream_name
                    except svr.StreamException:

                        # Closed Stream
                        if stream_name in open_streams:
                            del open_streams[stream_name]
                            print "Stream Closed:", stream_name

        # Show streams
        for stream_name, stream in open_streams.items():  # Cannot be iter because
                                                        # dict is mutated in loop
            frame = None
            try:
                frame = stream.get_frame()
            except svr.OrphanStreamException:

                # Closed Stream
                del open_streams[stream_name]
                cv.DestroyWindow(stream_name)
                print "Stream Closed:", stream_name

            if frame:
                cv.ShowImage(stream_name, frame)

        key = cv.WaitKey(10)
        if key == ord('q'):
            break
