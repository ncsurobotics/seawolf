
import sys
from collections import deque
from time import sleep

from vision import ExitSignal
import sw3

try:
    import seawolf
except ImportError:
    raise ImportError('''\n
Error: Could not import library "seawolf".
    Make sure the libseawolf python bindings are installed.
''')

class MissionController(object):
    '''Orchestrates the execution of a queue of missions.'''

    def __init__(self, entity_searcher, wait_for_go=False):
        '''
        Arguments:

        entity_searcher - An EntitySearcher object.

        '''

        self.entity_searcher = entity_searcher
        self.wait_for_go = wait_for_go
        self.mission_queue = deque()
        self.current_mission = None
        self.last_mission = None

        # libseawolf init
        application_name = "Mission Control"
        if seawolf.getName() != application_name:  # Check if seawolf is already initialized
            seawolf.loadConfig("../conf/seawolf.conf")
            seawolf.init(application_name)
            seawolf.notify.filter(seawolf.FILTER_ACTION, "GO")

        # Zero Heading
        #TODO

        # Set Reference Angle
        self.reference_angle = None #TODO

    def kill(self):
        self.entity_searcher.start_search([])
        sw3.nav.do(sw3.NullRoutine())
    __del__ = kill

    def execute_all(self):
        '''Runs all missions in the queue.'''

        # Wait for go signal
        if self.wait_for_go:
            print "Waiting for GO signal..."
            while not seawolf.notify.available():
                seawolf.var.set("MissionReset", 0)
                sleep(0.1)
                self.entity_searcher.ping()
            action, param = seawolf.notify.get()

        # Run missions
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
        print "Starting mission:", self.current_mission
        self.current_mission.init()
        try:
            self.current_mission.execute()
            print "MISSION FINISHED"
        except ExitSignal:
            sys.exit(0)
        self.entity_searcher.start_search([])
        return True

