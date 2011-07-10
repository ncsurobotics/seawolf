
from base import MissionControlReset

from base import MissionBase
from test import TestMission
from path import PathMission
from gate import GateMission
from buoys import BuoysMission
from bins import BinsMission
from lovelane import LoveLaneMission

mission_classes = {
    'test': TestMission,
    'path': PathMission,
    'gate': GateMission,
    'buoys': BuoysMission,
    'bins': BinsMission,
    'lovelane': LoveLaneMission,
}
