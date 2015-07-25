from base import MissionControlReset

from base import MissionBase, SearchMission
from test import TestMission
from gate import GateMission
from path import PathMission
#from buoy import BuoyMission
#from buoy_simple import SimpleBuoyMission
from new_buoy import NewBuoyMission
from hedge import HedgeMission
from bins import BinsMission
#from acoustics import AcousticsMission
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
#    'buoysimple': SimpleBuoyMission,
    'new_buoy': NewBuoyMission,
    'hedge': HedgeMission,
    'bins': BinsMission,
    'new_bins': NewBinsMission,
    'fakepizza': FakePizzaMission,
    'strafetest': StrafeMission,
    #'acoustics': AcousticsMission
}
