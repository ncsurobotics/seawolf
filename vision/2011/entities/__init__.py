
from base import VisionEntity

# Entities
from path import Path
from test import Test

entity_classes = {
    "path": Path,
    "test": Test,
}

def get_all_used_cameras():
    '''Returns a list of all camera names that are used by entities.'''

    camera_list = []
    for entity_name, entity_class in entity_classes.iteritems():
        if entity_class.camera_name not in camera_list:
            camera_list.append(entity_class.camera_name)
    return camera_list
