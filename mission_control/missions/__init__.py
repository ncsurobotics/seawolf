from base import MissionControlReset

from base import MissionBase, SearchMission
from test import TestMission
from gate import GateMission
from path import PathMission
from buoy import BuoyMission
from hedge import HedgeMission
#from buoy_simple import SimpleBuoyMission
#from buoy_demo import BuoyDemoMission

mission_classes = {
    'test': TestMission,
    'search': SearchMission,
    'gate': GateMission,
    'path': PathMission,
    'buoy': BuoyMission,
    'hedge': HedgeMission
    #'buoy_simple': SimpleBuoyMission,
    #'buoy_demo':BuoyDemoMission,
}
