
from vision import entities
from missions.base import MissionBase

class TestMission(MissionBase):

    def __init__(self, entity_cls=None):
        if not entity_cls:
            # This is done instead of putting it as a default argument because
            # the simulator doesn't have a TestEntity.
            entity_cls = entities.TestEntity
        self.entity_cls = entity_cls

    def init(self):
        print "inititalizing TestEntity"
        self.process_manager.start_process(self.entity_cls, "test", "forward")

    def step(self, vision_data):
        if vision_data:
            print "vision data =", vision_data
