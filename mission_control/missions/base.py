
class MissionBase(object):
    '''A base class for missions.'''

    def __repr__(self):
        pass #TODO: Maybe some introspection to get the class name here?

    def register_mission_controller(self, mission_controller):
        ''' Called by the mission controller when the mission is added.'''
        self.mission_controller = mission_controller
        self.entity_searcher = mission_controller.entity_searcher

    def init(self):
        '''Called once right before the mission is executed.'''
        pass

    def execute(self):
        '''Runs the mission.

        This is a blocking call that returns when the mission completes.
        '''
        mission_done = False
        while not mission_done:
            entity = self.entity_searcher.get_entity()
            if entity:
                mission_done = self.step(entity)

    def step(self, object_found):
        '''
        Called whenever an object is found.

        This function is the brain of the mission object.  It receives an
        object and processes it in order to navigate the robot.
        '''
        raise NotImplementedError()
