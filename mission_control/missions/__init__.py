
from base import MissionBase
from test import TestMission
from path import PathMission
from gate import GateMission
from buoys import BuoysMission

mission_classes = {
    'test': TestMission,
    'path': PathMission,
    'gate': GateMission,
    'buoys': BuoysMission,
}
