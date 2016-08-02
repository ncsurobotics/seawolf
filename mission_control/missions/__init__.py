from base import MissionControlReset

from base import MissionBase, SearchMission
from test import TestMission
from gate import GateMission
from path import PathMission
from buoy2 import BuoyMission
from buoy_simple import SimpleBuoyMission
from buoy_simpleYellow import SimpleYellowBuoyMission
from buoy_simpleYellowPull import SimpleYellowPullBuoyMission
from new_buoy import NewBuoyMission
from hedge import HedgeMission
from hedge180 import HedgeMission180
from reverse_hedge import ReverseHedgeMission
from bins import BinsMission
from acoustics import AcousticsMission
from acoustics1 import AcousticsMission1
from new_bins import NewBinsMission
from fakepizza import FakePizzaMission
from strafetest import StrafeMission
#from buoy_simple import SimpleBuoyMission
#from buoy_demo import BuoyDemoMission

mission_classes = {
    'strafetest': StrafeMission,
    'test': TestMission,
    'search': SearchMission,
    'gate': GateMission,
    'path': PathMission,
#    'buoy': BuoyMission,
    'buoysimple': SimpleBuoyMission,
    'buoyyellow': SimpleYellowBuoyMission,
    'buoyyellowpull': SimpleYellowPullBuoyMission,
    'new_buoy': NewBuoyMission,
    'hedge': HedgeMission,
    'hedge180': HedgeMission180,
    'reverse_hedge': ReverseHedgeMission,
    'bins': BinsMission,
    'new_bins': NewBinsMission,
    'fakepizza': FakePizzaMission,
    'strafetest': StrafeMission,
    'acoustics': AcousticsMission,
    'acoustics1': AcousticsMission1,
}
