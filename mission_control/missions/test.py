
import entities
from missions.base import MissionBase

class TestMission(MissionBase):
    
    def init(self):
        print "inititalizing TestEntity"
        self.process_manager.start_process(entities.TestEntity, "test", 1)

    def step(self, vision_data):
        print "vision data =", vision_data
