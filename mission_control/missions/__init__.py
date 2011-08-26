from base import MissionControlReset

from base import MissionBase
from test import TestMission
from gate import GateMission

mission_classes = {
    'test': TestMission,
    'gate': GateMission,
}
