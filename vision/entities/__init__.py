
import sys
import os
mission_control_directory = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    "../../../mission_control/"
))
sys.path.append(mission_control_directory)

from base import VisionEntity, MultiCameraVisionEntity

# Entities
from test import TestEntity
from gate import GateEntity, GATE_BLACK, GATE_WHITE
from binoculartest import BinocularTest
from path import PathEntity
from buoy import BuoyEntity
from buoytest import BuoyTestEntity
from buoynew import BuoyNewEntity
from binocularbuoy import BinocularBuoy
from weapons import WeaponsEntity 
from buoy2011 import Buoy2011Entity
from doublepath import DoublePathEntity
from hedge import HedgeEntity
from bins import BinsEntity
from binscorner import BinscornerEntity

entity_classes = {
    "test": TestEntity,
    "binoculartest": BinocularTest,
    "binocularbuoy": BinocularBuoy,
    "gate": GateEntity,
    "path": PathEntity,
    "buoy": BuoyEntity,
    "buoynew": BuoyNewEntity,
    "buoytest": BuoyTestEntity,
    "buoy2011": Buoy2011Entity,
    "hedge": HedgeEntity,
    "weapons": WeaponsEntity,
    "doublepath": DoublePathEntity,
    "bins": BinsEntity,
    "binscorner": BinscornerEntity
}

