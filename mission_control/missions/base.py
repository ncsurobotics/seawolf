
class MissionBase(object):
    '''A base class for missions.'''

    def __repr__(self):
        pass #TODO: Maybe some introspection to get the class name here?

    def register_mission_controller(self, mission_controller):
        self.mission_controller = mission_controller
        self.entity_searcher = mission_controller.entity_searcher

    def execute(self):
        mission_done = False
        while not mission_done:
            entity = self.entity_searcher.get_entity()
            if entity:
                mission_done = self.step(entity)

    def step(self, object_found):
        raise NotImplementedError()
