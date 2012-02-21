from base import MissionControlReset

from base import MissionBase
from test import TestMission
from gate import GateMission
from path import PathMission
from buoy import BuoyMission
from buoy_simple import SimpleBuoyMission
from buoy_demo import BuoyDemoMission

mission_classes = {
    'test': TestMission,
    'gate': GateMission,
    'path': PathMission,
    'buoy': BuoyMission,
    'buoy_simple': SimpleBuoyMission,
    'buoy_demo':BuoyDemoMission,
}
