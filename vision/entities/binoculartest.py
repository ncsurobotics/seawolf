
from base import VisionEntity, MultiCameraVisionEntity
import cv

class BinocularTestWorker(VisionEntity):

    def init(self):
        cv.NamedWindow(self.camera_name)

    def process_frame(self,frame):

        if self.debug:

            #return that we have finished processing
            self.send_message("Finished")

            #wait for further information from parent
            self.wait_for_parent(None)

            print 'worker has recieved data'

            #display frame
            cv.ShowImage(self.camera_name, frame)
            print "displaying frame from worker", self.camera_name

class BinocularTest(MultiCameraVisionEntity):
    subprocess = BinocularTestWorker

    def manage_workers(self):
        ''' walk workers through processing this frame'''

        #send capture singals to workers
        self.sync_capture()

        #wait for response from all workers
        worker_data = self.wait_for_workers()

        #process data from workers
        for key in worker_data.keys():
            process = self.process_manager.process_list[key]
            process.send_data(ManagerData())

        print worker_data

class WorkerData(object):
    ''' used to pass data from worker to manager '''
    def __init__(self):
        pass

class ManagerData(object):
    ''' used to pass data from a manager to a class '''
    def __init__(self):
        pass
