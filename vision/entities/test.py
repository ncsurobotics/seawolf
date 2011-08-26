import entities
import cv

class TestEntity(entities.VisionEntity):

 
    def process_frame(self, frame, debug=True):
        ''' process this frame, then place output in self.output'''

        if debug:
            #display frame
            cv.NamedWindow("Test")
            print frame
            cv.ShowImage("Test", frame)
            print "displaying frame"
            cv.WaitKey(1)
        
        self.output = "test data"

