
from time import time

class MissionBase(object):
    '''A base class for missions.'''

    def register_mission_controller(self, mission_controller):
        ''' Called by the mission controller when the mission is added.'''
        self.mission_controller = mission_controller
        self.entity_searcher = mission_controller.entity_searcher

    def init(self):
        '''Called once right before the mission is executed.'''
        pass

    def set_entity_timeout(self, timout):
        '''Gives the time to wait for an entity before calling step() anyways.

        The execute function will look at the timeout given and call step(None)
        when the timeout has passed to indicate that no entity has been found
        in the past timeout seconds.  It will then continue to call step(None)
        every timeout seconds until an entity is seen.
        '''
        self._entity_timeout = timeout

    def execute(self):
        '''Runs the mission.

        This is a blocking call that returns when the mission completes.
        '''

        self._entity_timeout = getattr(self, "_entity_timout", None)
        self._mission_done = getattr(self, "_mission_done", False)
        time_since_last_entity = time()

        while not self._mission_done:
            entity = self.entity_searcher.get_entity()

            if entity:
                time_since_last_entity = time()
                self._mission_done = self.step(entity)

            elif time_since_last_entity > self._entity_timeout:
                time_since_last_entity = time()
                self._mission_done = self.step(None)

    def finish_mission(self, *args, **kwargs):
        '''Marks the mission complete so self.execute() will return.

        This is an asynchronous alternative to having self.step() return True.
        Any arguments are accepted, but all are ignored.  This allows you to
        register this function as a callback for anything, such as a nav
        routine.
        '''
        self._mission_done = True

    def step(self, entity_found):
        '''
        Called whenever an entity is found.

        This function is the brain of the mission object.  It receives an
        entity and processes it in order to navigate the robot.

        This is the only function that needs to be implemented in a subclass.
        '''
        raise NotImplementedError()
