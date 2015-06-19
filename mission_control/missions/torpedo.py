from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3

TARGET_DEPTH = 6
TURN_SPEED = .3
TURN_ANGLE = 90
TURN_TIMER = 5
AIM_TIMER = 5
TARGET_1 = 'A'
TARGET_2 = 'B'
# need simulator entity to start testing
# vision: Distance, Center, Holes[] hole.center, hole.size/shape


class TorpedoMission(MissionBase):

    def init(self):
        self.process_manager.start_process(entities.TorpedoEntity, "torpedo", "forward", debug=True)
        self.states = [
            "aim",
            "fire",
            "findpath"
        ]
        self.state_num = 0
        self.state = self.states[self.state_num]
        self.fired = 0
        self.aimed = 0
        self.set_timer("torpedo_timeout", 45, self.fail_mission)

    def step(self, vision_data):
        if not vision_data:
            return
        torpedo_data = vision_data['torpedo']
        # holes[] = vision_data.holes    SYNTAX ERROR, fix this
        print torpedo_data
        current_depth = sw3.data.depth()
        if self.state == "aim":
            self.aim(torpedo_data)
        if self.state == "fire":
            self.fire(torpedo_data)
        if self.state == "findpath":
            self.findpath()

    def aim(self, target):

        # line up with target, see all four corners
        # change depth to specified color
        sw3.nav.do(sw3.SetDepth(TARGET_DEPTH))
        # go forward until only see color
        self.aimed += 1
        self.nextState()

    def fire(self, holes):
        # verify lined up
        # fire!
        self.fired += 1
        self.nextState()

    def findpath(self, holes):
        # swim around target?
        turn = sw3.CompoundRoutine(sw3.RelativeYaw(TURN_ANGLE), sw3.Forward(TURN_SPEED), timeout=TURN_TIMER)
        finish = sw3.CompoundRoutine(sw3.RelativeYaw(-TURN_ANGLE), sw3.Forward(TURN_SPEED), timeout=TURN_TIMER)
        sw3.nav.do(turn)
        sw3.nav.do(finish)
        self.finish_mission()

    def nextState(self):
        if self.fired == 1 and self.aimed == 1:
            self.state_num = 0
            self.state = self.states[self.state_num]
        else:
            self.state_num += 1
            self.state = self.states[self.state_num]
        print "State:", self.state
