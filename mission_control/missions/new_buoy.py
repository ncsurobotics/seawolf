from __future__ import division

from vision import entities
from missions.base import MissionBase

import sw3

class NewBuoyMission(MissionBase):

    def init(self):
        self.process_manager.start_process(entities.BuoyHoughEntity, "buoy", "forward", debug=True)
        sw3.nav.do(sw3.SetDepth(6))
        self.bumped = 0

    def step(self, vision_data):
        buoys = []
        if vision_data is not None:
            buoys = vision_data['buoy'].buoys

        if len(buoys) > 0:
            looking_for = 'red'
            if self.bumped == 1:
                looking_for = 'green'
        

            selected = None
            for buoy in buoys:
                if buoy.color == looking_for:
                    selected = buoy

            if selected is not None:
                sw3.nav.do(sw3.CompoundRoutine(
                    sw3.SetDepth(7),
                    sw3.RelativeYaw(selected.theta),
                    sw3.Forward(.2, 6),
                ))
                self.bumped += 1
                sw3.nav.do(sw3.Forward(-.2, 6))

            if self.bumped == 2: 
                self.finish_mission()
        
