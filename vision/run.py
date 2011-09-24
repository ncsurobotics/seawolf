'''A script to test vision entities.

This script opens vision entities in the same way that mission control does (so
things are tested properly), but also has the option to open the entity in the
same process (just for debugging).

Run this script as such:

python run.py ENTITY_NAME CAMERA_NAME [CAMERA_NAME ...]

'''

import sys
import process_manager
import entities
import time

#spawn a process manager, and start the correct vision process

if __name__ == "__main__":
    entity_name = sys.argv[1]
    camera_names = sys.argv[2:]

    #spawn a process manager
    pm = process_manager.ProcessManager()

    #start the requested vision entity
    pm.start_process(entities.entity_classes[entity_name], entity_name, *camera_names, debug = True )

    try:
        while True:
            #for debugging, print out entity output
            output = pm.get_data()
            if output: 
                print output

    except process_manager.KillSignal:
        # Exit if the subprocess tells us to
        pass
    except Exception:
        pm.kill()
        raise
