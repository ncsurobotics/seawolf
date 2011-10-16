
import time

class ProcessManager(object):

    def __init__(self):
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
        vision_data_empty = True

        for process in self.process_list:
            output = process.get_data()

            if output != None:
                vision_data_empty = False

            #add this data to the dictionary
            vision_data[process.name] = output

        #if vision_data is empty, return None
        if vision_data_empty:
            return None
        else:
            return vision_data

    def ping(self):
        '''verify that all processes are alive'''
        return True

    def kill(self):
        ''' kill all running sub processes '''
        for process in self.process_list:
            process.kill()

        self.process_list = []

class VisionProcess(object):

    def __init__(self, entity_cls, name):
        #assign the vision entity this process handles
        self.entity_cls = entity_cls
        self.name = name

    def get_data(self):
        '''check for incoming data from this process'''
        #return any new data from the queue
        self.entity.get_data()

    def kill(self):
        '''kills this process'''
        pass

    def run(self, *args, **kwargs):
        '''runs this process'''
        # Simulator doesn't need to actually create a new process
        self.entity = self.entity_cls(*args, **kwargs)

