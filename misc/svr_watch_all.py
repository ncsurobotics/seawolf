'''Show all svr streams, and show any new streams that appear.'''

import cv

import svr

svr.connect()
open_streams = {} # Map stream names to stream objects

while True:

    # Get new streams
    all_streams = svr.get_sources_list()
    for stream in all_streams:
        stream_name = stream.split(":")[1]
        if stream_name not in open_streams:
            open_streams[stream_name] = svr.Stream(stream_name)
            open_streams[stream_name].unpause()
            cv.NamedWindow(stream_name)
            print "Stream Opened:", stream_name

    # Show streams
    for stream_name, stream in open_streams.items():  # Cannot be iter because
                                                      # dict is mutated in loop
        frame = None
        try:
            frame = stream.get_frame()
        except svr.OrphanStreamException:
            del open_streams[stream_name]
            cv.DestroyWindow(stream_name)
            print "Stream Closed:", stream_name

        if frame:
            cv.ShowImage(stream_name, frame)

    key = cv.WaitKey(10)
    if key == ord('q'):
        break
