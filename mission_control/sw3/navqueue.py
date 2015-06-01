
import Queue as queue
import threading

# Navigational primitives that the mixer can handle
# interactions = ("Yaw",
#                 "Forward",
#                 "Depth",
#                 "Pitch",
#               TODO  "Strafe",
#               TODO  "Roll")

from routines import NullRoutine


class NavQueue(object):

    def __init__(self):
        self.current_routine = None

    def do(self, routine):
        """ Equivalent to a called to clear() followed by append() """
        if self.current_routine is not None:
            self.current_routine.cancel()
        self.current_routine = routine
        routine.start()

    def clear(self):
        """ Cancel the running routine """
        if self.current_routine:
            self.current_routine.cancel()
            self.current_routine = None
