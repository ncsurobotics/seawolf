
from base import MissionBase
from test import TestMission
from path import PathMission
from gate import GateMission

mission_classes = {
    'test': TestMission,
    'path': PathMission,
    'gate': GateMission,
}
