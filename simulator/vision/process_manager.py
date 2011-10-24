
import time
from multiprocessing.connection import Client

class ProcessManager(object):

    def __init__(self):

        # Maps entity class name -> (entity class, process name)
        self.processes = {}

        # Initialize pipe to simulator
        self.simulator_pipe = Client(("localhost", 3829))

    def start_process(self, entity_class, name,  *args, **kwargs):
        '''Initiates a process of the class proc_cls.'''
        self.processes[entity_class.__name__] = (entity_class, name)
        self.simulator_pipe.send(
            map(lambda x: x[0], self.processes.itervalues())
        )

    def get_data(self):
        '''get data from all running processes and
           package the output into a dictionary '''

        vision_data = {}
        if self.simulator_pipe.poll():
            for entity_cls, data in self.simulator_pipe.recv():
                entity_cls, process_name = self.processes[entity_cls.__name__]
                vision_data[process_name] = data

        if vision_data:
            for entity_cls_name, process_name in self.processes.itervalues():
                if process_name not in vision_data:
                    vision_data[process_name] = None
            return vision_data
        else:
            return None

    def ping(self):
        '''verify that all processes are alive'''
        return True

    def kill(self):
        ''' kill all running sub processes '''
        self.simulator_pipe.send([])

class KillSignal(Exception):
    pass
