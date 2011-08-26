
import time
from multiprocessing import Process, Pipe

class ProcessManager(object):

    def __init__(self):
        #holds the list currently running processes
        self.process_list = []

    def start_process(self, proc_cls, name,  *args, **kwargs):
        '''Initiates a process of the class proc_cls.'''
        vision_process = VisionProcess(proc_cls, name)
        self.process_list.append(vision_process)
        vision_process.run(*args, **kwargs)
        return vision_process

    def get_data(self):
        '''get data from all running processes and
           package the output into a dictionary '''

        vision_data = {}

        for process in self.process_list:
            output = process.get_data()

            if output != None:
                #add this data to the dictionary
                vision_data[process.name] = output
                
        #if vision_data is empty, return None
        if vision_data: 
            return vision_data
        else:
            return None

    def ping(self):
        '''verify that all processes are alive'''
        pass

    def kill(self):
        ''' kill all running sub processes ''' 
        pass

class VisionProcess(object):

    def __init__(self, entity_cls, name):
        #assign the vision entity this process handles
        self.entity_cls = entity_cls
        self.name = name

    def get_data(self):
        '''check for incoming data from this process'''
        #return any new data from the queue
        if self.parent_conn.poll():
            return self.parent_conn.recv()

    def kill(self):
        '''kills this process'''
        self.parent_conn.send(KillSignal())
        pass

    def run(self, *args, **kwargs):
        '''runs this process'''
        parent_conn, child_conn = Pipe()
        self.parent_conn = parent_conn
        self.process = Process(target=run_entity, args = (child_conn, self.entity_cls) + args, kwargs = kwargs)
        self.process.start()

def run_entity(child_conn, entity_cls, *args, **kwargs):
    '''perpetually loops the vision class entity_cls, and outputs data
       through the child_conn pipe '''
    entity = entity_cls(child_conn, *args, **kwargs)
    entity.run()

class KillSignal(Exception):
    pass

