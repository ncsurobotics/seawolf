
import sys
import os
mission_control_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../../../mission_control/"
))
sys.path.append(mission_control_directory)

# Entities
from .test import TestEntity
from .gate import GateEntity, GATE_BLACK, GATE_WHITE
#from .binoculartest import BinocularTest
from .path import PathEntity
#from .buoy import BuoyEntity
from .buoytest import BuoyTestEntity
from .buoynew import BuoyNewEntity
#from .binocularbuoy import BinocularBuoy
from .weapons import WeaponsEntity
#from .buoy2011 import Buoy2011Entity
from .doublepath import DoublePathEntity
from .doublepath2 import DoublePath2Entity
from .hedge import HedgeEntity
# from .bins import BinsEntity
# from .binscorner import BinsCornerEntity
from .binscontour import BinsContourEntity
# from .binshough import BinsHoughEntity
#from .binshough2 import BinsHough2Entity
#from .pizza import PizzaEntity
#from .pizzacorner import PizzaCornerEntity
from .blobtesting import BlobTesting
from .paths import PathsEntity
from .hedgeR import HedgeREntity
from .hedgeY import HedgeYEntity
from .hedgetesting import HedgeTestingEntity
# from .oldhedge import OldHedgeEntity
from .buoycontour import BuoyContourEntity
from .buoycontours2 import BuoyContour2Entity
from .buoyhough import BuoyHoughEntity

entity_classes = {
    "test": TestEntity,
    "hedgetesting": HedgeTestingEntity,
    #"binoculartest": BinocularTest,
    #"binocularbuoy": BinocularBuoy,
    "gate": GateEntity,
    "path": PathEntity,
    #"buoy": BuoyEntity,
    "buoynew": BuoyNewEntity,
    "buoytest": BuoyTestEntity,
    #"buoy2011": Buoy2011Entity,
    "buoycontour": BuoyContourEntity,
    "buoycontour2": BuoyContour2Entity,
    "buoyhough": BuoyHoughEntity,
    "hedge": HedgeEntity,
    "weapons": WeaponsEntity,
    "doublepath": DoublePathEntity,
    # "bins": BinsEntity,
    # "binscorner": BinsCornerEntity,
    "binscontour": BinsContourEntity,
    # "binshough": BinsHoughEntity,
    #"binshough2": BinsHough2Entity,
    "doublepath2": DoublePath2Entity,
    #"pizza": PizzaEntity,
    #"pizzacorner": PizzaCornerEntity,
    "paths": PathsEntity,
    "blobtesting": BlobTesting,
    "hedgeR": HedgeREntity,
    "hedgeY": HedgeYEntity,
    # "oldhedge": OldHedgeEntity
}
