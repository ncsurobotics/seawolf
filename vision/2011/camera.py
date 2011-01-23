
import cv

class Camera(object):
    '''An wrapper for OpenCV's camera functionality.'''

    def __init__(self, index, display=True, record=True):
        '''
        Arguments:

        index - This is a capture device indentifier suitable to be passed to
            cv.CaptureFromFile() (if index is a string) or cv.CaptureFromCAM()
            (if index is an int).  Typically this argument should be a filename
            of a video file, or an index of a camera.

        display - If True, a graphical window will display the images captured
            from this camera.  cv.WaitKey must be called at some point for the
            image to be displayed.

        record - If True, all images captured will be recorded.  If the index
            given is a filename, this is overwritten to false.

        '''

        self.index = index
        self.display = display
        self.record = record
        self.capture = None # Underlying opencv capture object

        if display:
            cv.NamedWindow("Camera %s" % index)

    def get_frame(self):
        '''Gets a frame from the camera.'''

        if self.record:
            pass #TODO

        if not self.capture:
            self.open_capture()

        frame = cv.QueryFrame(self.capture)
        if self.display:
            cv.ShowImage("Camera %s" % self.index, frame)

        if not frame:
            raise self.CaptureError('Could not capture frame from index "%s"'
                % self.index)

        return frame

    def open_capture(self):
        '''Opens the underlying capture device.

        This need not be called explicitly.  get_frame() will call
        open_capture() if needed.

        '''
        try:
            self.index = int(self.index)
        except ValueError:
            pass
        if isinstance(self.index, basestring):
            self.capture = cv.CaptureFromFile(self.index)
            self.record = False
        else:
            self.capture = cv.CaptureFromCAM(self.index)
        return self.capture

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
        return "<Camera index=%s>" % self.index
