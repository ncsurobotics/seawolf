# this is the template for mission control, shouldnt be ran

from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3


STRAFE_SPEED = 0.3


class StrafeMission(MissionBase):

    def __init__(self):
        self.gate_seen = 0
        self.gate_lost = 0

    def init(self):
        self.process_manager.start_process(entities.GateEntity, "gate", "forward", debug=True)
        sw3.nav.do(sw3.CompoundRoutine(
            sw3.Strafe(STRAFE_SPEED),
            sw3.SetDepth(2),
            sw3.HoldYaw(),
        ))

    def step(self):
        if not self.vision_data:
            return

        gate_data = self.vision_data['gate']

        if not gate_data:
            return

        print gate_data
