
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

entity_classes = {
    "test": TestEntity,
    "binocular_test": BinocularTest,
    "gate": GateEntity,
    "path": PathEntity,
    "buoy": BuoyEntity,
    "buoytest": BuoyTestEntity,
}

