'''A fake vision package.

This package simulates searching for vision entities, but instead it queries
the simulator for locations of objects, and returns information about them in
the same way that the vision system normally would.

'''

from process_manager import ProcessManager, KillSignal
import entities
