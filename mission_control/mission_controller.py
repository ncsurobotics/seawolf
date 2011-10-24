
import sys
from collections import deque
from time import sleep

from vision import KillSignal
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

    def __init__(self, process_manager, wait_for_go=False):
        '''
        Arguments:

        process_manager
        '''

        self.process_manager = process_manager
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



    def kill(self):
        self.process_manager.kill()
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
                self.process_manager.ping()
            action, param = seawolf.notify.get()

        try :
            # Run missions
            while self.execute_next():
                pass
        except Exception:
            self.process_manager.kill()
            raise 

    def append_mission(self, mission):
        '''Adds a mission to the queue.

        Arguments:

        mission - An instantiation of a subclass of MissionBase.  A list of
            missions can be found in the missions module.

        '''
        self.mission_queue.append(mission)
        if not isinstance(mission, sw3.NavRoutine):
            mission.register_mission_controller(self)

    def execute_next(self):
        '''Runs the next mission on the queue.'''
        self.last_mission = self.current_mission
        try:
            self.current_mission = self.mission_queue.popleft()
        except IndexError: # deque raises IndexError when it is empty
            return False
        print "Starting mission:", self.current_mission

        if isinstance(self.current_mission, sw3.NavRoutine):
            try:
                sw3.nav.do(self.current_mission)
                self.current_mission.wait()
                print "NAV ROUTINE FINISHED"
            except KillSignal:
                sys.exit(0)
        else:
            self.current_mission.init()
            try:
                self.current_mission.execute()
                print "MISSION FINISHED"
            except KillSignal:
                sys.exit(0)

        self.process_manager.kill()
        return True

