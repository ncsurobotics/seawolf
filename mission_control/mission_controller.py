
from collections import deque

from vision import ExitSignal

try:
    import seawolf
except ImportError:
    raise ImportError('''\n
Error: Could not import library "seawolf".
    Make sure the libseawolf python bindings are installed.
''')

class MissionController(object):
    '''Orchestrates the execution of a queue of missions.'''

    def __init__(self, entity_searcher):
        '''
        Arguments:

        entity_searcher - An EntitySearcher object.

        '''

        self.entity_searcher = entity_searcher
        self.mission_queue = deque()
        self.current_mission = None
        self.last_mission = None

        # libseawolf init
        seawolf.loadConfig("../conf/seawolf.conf")
        seawolf.init("Mission Control")
        seawolf.notify.filter(seawolf.FILTER_ACTION, "GO")

        # Zero Heading
        #TODO

        # Set Reference Angle
        self.reference_angle = None #TODO

    def __del__(self):
        seawolf.close()

    def execute_all(self):
        '''Runs all missions in the queue.'''
        while self.execute_next():
            pass

    def append_mission(self, mission):
        '''Adds a mission to the queue.

        Arguments:

        mission - An instantiation of a subclass of MissionBase.  A list of
            missions can be found in the missions module.

        '''
        self.mission_queue.append(mission)
        mission.register_mission_controller(self)

    def execute_next(self):
        '''Runs the next mission on the queue.'''
        self.last_mission = self.current_mission
        try:
            self.current_mission = self.mission_queue.popleft()
        except IndexError: # deque raises IndexError when it is empty
            return False
        #print "Starting mission:", self.current_mission.__name__
        self.current_mission.init()
        try:
            self.current_mission.execute()
        except ExitSignal:
            return False
        return True
