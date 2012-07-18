
import sys
import time
import traceback
from multiprocessing import Process, Pipe

import svr

import sw3

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
        vision_process = VisionProcess(self, proc_cls, name)
        self.process_list[name] = vision_process
        for key, value in self.extra_kwargs.iteritems():
            kwargs[key] = value
        vision_process.run(*args, **kwargs)
        return vision_process

    def get_data(self, *process_names, **kwargs):
        '''get data from all running processes and
           package the output into a dictionary blah blah'''

        vision_data = {}
        vision_data_empty = True
        force = kwargs.pop("force", False)
        delay = kwargs.pop("delay", 0)
        if force:
            delay = None

        if not process_names:
            process_names = self.process_list.keys()

        for process_name in process_names:
            if process_name in self.process_list.keys():
                process = self.process_list[process_name]

                output = process.get_data(delay)

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

    def __init__(self, process_manager, entity_cls, name):
        #assign the vision entity this process handles
        self.process_manager = process_manager
        self.entity_cls = entity_cls
        self.name = name

    def get_data(self, delay=0):
        '''check for incoming data from this process'''
        #return any new data from the queue
        if self.downstream_conn.poll(delay):
            data =  self.downstream_conn.recv()
            if isinstance(data, KillSignal):
                self.process_manager.kill()
                raise data
            #elif str(data.__class__) == str(SensorCapture):
            elif isinstance(data, SensorCapture):
                sw3.data.freeze(self.name)
            else:
                #print "Data:", data
                #print str(data.__class__), str(SensorCapture)
                return data

    def send_data(self, data):
        '''sends data down the conn'''
        self.downstream_conn.send(data)

    def kill(self):
        '''kills this process'''
        self.downstream_conn.send(KillSignal())

    def run(self, *args, **kwargs):
        '''runs this process'''
        parent_conn, child_conn = Pipe()
        self.downstream_conn = parent_conn
        self.process = Process(target=run_entity, args = (child_conn, self.entity_cls) + args, kwargs = kwargs)
        self.process.start()

def run_entity(upstream_conn, entity_cls, *args, **kwargs):
    '''perpetually loops the vision class entity_cls, and outputs data
       through the upstream_conn pipe '''
    try:
        svr.connect()
        entity = entity_cls(upstream_conn, *args, **kwargs)
        print "running", entity
        entity.run()
    except Exception as e:
        upstream_conn.send(KillSignal())
        traceback.print_exc()
        sys.exit()

class KillSignal(Exception):
    pass

class SensorCapture(object):
    '''Sent to entity's parent process when it is capturing a frame.'''
    pass

