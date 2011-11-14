from base import MissionControlReset

from base import MissionBase
from test import TestMission
from gate import GateMission
from path import PathMission
from buoy import BuoyMission

mission_classes = {
    'test': TestMission,
    'gate': GateMission,
    'path': PathMission,
    'buoy': BuoyMission,
}
