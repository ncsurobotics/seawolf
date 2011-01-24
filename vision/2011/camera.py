
import cv

class Camera(object):
    '''An wrapper for OpenCV's camera functionality.

    Supports camera indexes, video files, and image files.

    '''

    def __init__(self, identifier, display=True, record=True):
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

        record - If True, all images captured will be recorded.  If the
            identifier given is a filename, this is overwritten to false.

        '''

        self.identifier = identifier
        self.display = display
        self.record = record
        self.image = None # Stored image, if identifier is an image filename
        self.capture = None # Underlying opencv capture object

        if display:
            cv.NamedWindow("Camera %s" % identifier)

    def get_frame(self):
        '''Gets a frame from the camera.'''

        if not self.capture and not self.image:
            self.open_capture()

        if self.image:
            return cv.CloneImage(self.image)

        if self.record:
            pass #TODO

        frame = cv.QueryFrame(self.capture)
        if self.display:
            cv.ShowImage("Camera %s" % self.identifier, frame)

        if not frame:

            # See if file is an image, not video
            self.image = cv.LoadImage(self.identifier)
            if self.image: return cv.CloneImage(self.image)

            raise self.CaptureError('Could not capture frame from identifier '
                '"%s"' % self.identifier)

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
            self.record = False
        else:
            self.capture = cv.CaptureFromCAM(self.identifier)

    def close(self):
        '''Close the camera.

        The camera can be reopened by getting another frame.

        '''
        if self.capture:
            del self.capture
        self.capture = None

    __del__ = close

    class CaptureError(ValueError):
        '''Represents an error in capturing a frame.'''
        pass

    def __repr__(self):
        return "<Camera identifier=%s>" % self.identifier
