import os
import cv
import cv2
import svr


class Camera(object):

    '''An wrapper for OpenCV's camera functionality.

    Supports camera indexes, video files, and image files.

    '''

    def __init__(self, identifier, display=False, window_name=None,
                 record_path=False):
        '''
        Arguments:

        indentifier - This is a capture device indentifier suitable to be
            passed to cv.CaptureFromFile() (if indentifier is a string) or
            cv.CaptureFromCAM() (if indentifier is an int).  This argument
            should be a filename of a video file, an index of a camera, or a
            filename of an image.

        display - If True, a graphical window will display the images captured
            from this camera.  cv.WaitKey must be called at some point for the
            image to be displayed.

        window_name - Name of the window to be created if display=True.  If
            None, the identifier will be used.

        record_path - If False, nothing will be recorded.  Otherwise a path to a
            directory to record video in should be given.  Video will be
            recorded into jpg files in the following format:
            "<record_path>/%d.jpg".

        '''

        self.identifier = identifier
        self.display = display
        self.window_name = window_name
        self.record_path = record_path
        self.image = None  # Stored image, if identifier is an image filename
        self.capture = None  # Underlying opencv capture object
        self.frame_count = 0
        self.dc1394_capture = None

        if display:
            pass  # cv.NamedWindow(self.get_window_name())

    def get_window_name(self):
        if self.window_name:
            return "Camera: %s" % self.window_name
        else:
            return "Camera: %s" % self.identifier

    def get_frame(self):
        '''Gets a frame from the camera.'''
        self.frame_count += 1

        if not self.capture and not self.image and not self.dc1394_capture:
            self.open_capture()

        if self.image:
            return cv.CloneImage(self.image)

        if self.dc1394_capture:
            frame = self.dc1394_capture.get_frame()
        else:
            frame = cv.QueryFrame(self.capture)
        # If the capture device doesn't work, OpenCV might not complain, but
        # just returns None when grabbing a frame.  Here we check for errors,
        # and see if it was actualy an image, not a video that we're opening
        if not frame:

            # See if file is an image, not video
            if isinstance(self.identifier, basestring):
                try:
                    self.image = cv.LoadImage(self.identifier)
                except IOError:
                    if self.frame_count > 1:
                        raise self.CaptureError("The video has run out of frames.")
                    else:
                        raise self.CaptureError("Either a read error occured "
                                                "with the file, or the file is not a valid video "
                                                "or image file.")
                if self.image:
                    return cv.CloneImage(self.image)
                else:
                    raise self.CaptureError("This shouldn't happen.  Please "
                                            " report a bug!  Include this traceback!!")
            else:
                raise self.CaptureError("Could not capture frame from "
                                        'identifier "%s"' % self.identifier)

            # TODO: Weird GStreamer error occured when a folder is incorrectly
            #      specified as a video file, or when the user doesn't have
            #      permissions for the file.


        #TODO: doesn't work. svr.debug doesn't accept debug request?
        if self.display:
            #cv.ShowImage(self.get_window_name(), frame)
            svr.debug(self.get_window_name(), frame)

        if self.record_path:
            filename = os.path.join(self.record_path, "%s.jpg" % self.frame_count)
            cv.SaveImage(filename, frame)

        return frame

    def open_capture(self):
        '''Opens the underlying capture device.

        This need not be called explicitly.  get_frame() will call
        open_capture() if needed.

        '''
        try:
            self.identifier = int(self.identifier)
        except ValueError:
            pass
        if isinstance(self.identifier, basestring):
            self.capture = cv.CaptureFromFile(self.identifier)
            self.record_path = False  # Don't re-record avi files
        else:
            self.capture = cv.CaptureFromCAM(self.identifier)

        if self.record_path and not os.path.exists(self.record_path):
            os.mkdir(self.record_path)

    def close(self):
        '''Close the camera.

        The camera can be reopened by getting another frame.

        '''
        if self.capture:
            del self.capture
        self.capture = None
        if self.dc1394_capture:
            self.dc1394_capture.close()
            self.dc1394_capture = None

    __del__ = close

    class CaptureError(ValueError):

        '''Represents an error in capturing a frame.'''
        pass

    def __repr__(self):
        return "<Camera identifier=%s>" % self.identifier
