
import entities
import cv

class BinocularTestWorker(entities.VisionEntity):
    
    def process_frame(self,frame):
        
        if self.debug:
            #display frame
            cv.NamedWindow(self.camera_name)
            print frame
            cv.ShowImage("Test", frame)
            print "displaying frame from worker", self.camera_name
            cv.WaitKey(10)

            #return that we have finished processing 
            self.send_message("Finished")

class BinocularTest(entities.MultiCameraVisionEntity):
    subprocess = BinocularTestWorker
    
    def manage_workers(self):
        ''' walk workers through processing this frame'''

        #send capture singals to workers 
        self.sync_capture()

        #wait for response from all workers
        worker_data = self.wait_for_workers()
    
        print worker_data
        
        self.output = worker_data

