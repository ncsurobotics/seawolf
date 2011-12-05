
import sys
import time
from multiprocessing import Process, Pipe

class ProcessManager(object):

    def __init__(self, extra_kwargs={}):
        '''
        :param extra_kwargs:
            Keyward args that are passed to each process started.
        '''
        #holds the list currently running processes
        self.extra_kwargs = extra_kwargs
        self.process_list = {}

    def start_process(self, proc_cls, name, *args, **kwargs):
        '''Initiates a process of the class proc_cls.'''
        vision_process = VisionProcess(proc_cls, name)
        self.process_list[name] = vision_process
        for key, value in self.extra_kwargs.iteritems():
            kwargs[key] = value
        vision_process.run(*args, **kwargs)
        return vision_process

    def get_data(self, *process_names, **kwargs):
        '''get data from all running processes and
           package the output into a dictionary '''

        vision_data = {}
        vision_data_empty = True
        force = kwargs.pop("force", False)

        if not process_names:
            process_names = self.process_list.keys()

        for process_name in process_names:
            if process_name in self.process_list.keys():
                process = self.process_list[process_name]

                if force:
                    output = process.get_data(None)
                else:
                    output = process.get_data()

                if output != None:
                    vision_data_empty = False

                vision_data[process.name] = output
            else:
                raise ValueError("Attempted to get data from a non-existant process")

        #if vision_data is empty, return None
        if vision_data_empty:
            return None
        else:
            return vision_data

    def send_data(self, message, *process_names):
        '''send data to the desired processes'''

        if not process_names:
            process_names = self.process_list.keys()

        for process_name in process_names:
            if process_name in self.process_list.keys():
                self.process_list[process_name].send_data(message)
            else:
                raise ValueError("Attempted to send data to non-existant process")

    def ping(self):
        '''verify that all processes are alive'''
        pass

    def kill(self):
        ''' kill all running sub processes '''
        for process in self.process_list.values():
            process.kill()

        self.process_list = {}

class VisionProcess(object):

    def __init__(self, entity_cls, name):
        #assign the vision entity this process handles
        self.entity_cls = entity_cls
        self.name = name

    def get_data(self, delay = 0):
        '''check for incoming data from this process''';
        #return any new data from the queue
        if self.parent_conn.poll(delay):
            data =  self.parent_conn.recv()
            #if isinstance(data,KillSignal):
            if data.__repr__() == KillSignal().__repr__():
                self.kill()
                sys.exit()
            else:
                return data

    def send_data(self, data):
        '''sends data down the conn'''
        self.parent_conn.send(data)

    def kill(self):
        '''kills this process'''
        self.parent_conn.send(KillSignal())

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
    print "running", entity
    entity.run()

class KillSignal(Exception):
    pass

