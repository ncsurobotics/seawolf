
from base import MissionControlReset

from base import MissionBase
from test import TestMission
from path import PathMission
from gate import GateMission
from buoys import BuoysMission
from bins import BinsMission
from lovelane import LoveLaneMission
from doublepath import DoublePathMission
from buoybump import BuoyBumpMission
from anglechange import AngleChangeMission
from depthchange import DepthChangeMission
from finishhedge import FinishHedgeMission
from depthchange2 import DepthChangeMission2

mission_classes = {
    'test': TestMission,
    'path': PathMission,
    'gate': GateMission,
    'buoys': BuoysMission,
    'buoybump': BuoyBumpMission,
    'bins': BinsMission,
    'lovelane': LoveLaneMission,
    'doublepath': DoublePathMission,
    'anglechange': AngleChangeMission,
    'finishhedge': FinishHedgeMission,
    'depthchange': DepthChangeMission,
    'depthchange2': DepthChangeMission2,

}
