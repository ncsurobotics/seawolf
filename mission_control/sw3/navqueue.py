
import Queue as queue
import threading

# Navigational primitives that the mixer can handle
# interactions = ("Yaw",
#                 "Forward",
#                 "Depth",
#                 "Pitch",
#                 "Strafe")

from routines import NullRoutine

class NavQueue(object):
    def __init__(self):
        self.current_routine = None

    def do(self, routine):
        """ Equivalent to a called to clear() followed by append() """
        if self.current_routine != None:
            self.current_routine.cancel()
        self.current_routine = routine
        routine.start()

    def clear(self):
        """ Cancel the running routine """
        if self.current_routine:
            self.current_routine.cancel()
            self.current_routine = None

    ###########  Removed Functionality  ###########

    def append(self, routine):
        """ Append a routine to the navigation queue. As one routine finishes the
        next one in line is called until the queue is exhausted. After exhausting
        the queue the robot will idle """
        raise NotImplementedError("Functionality removed!")

    def __next_routine(self, prev_routine_state):
        """ Start the next routine on the navigation queue. This function is
        registered with each routine to be run on completion """
        raise NotImplementedError("Functionality removed!")

    def idle(self):
        """ Clear the queue and run the idle routine """
        raise NotImplementedError("Functionality removed!")

