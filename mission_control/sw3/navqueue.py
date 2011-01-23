
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
    def __init__(self, idle_routine=NullRoutine):
        self.current_routine = None
        self.nav_queue = queue.Queue()
        self.nav_lock = threading.RLock()
        
        # The idle routine is run when NavStackManager.idle() is called and is
        # also called any time the navigation queue is exhausted
        self.idle_routine = idle_routine

    def __next_routine(self):
        """ Start the next routine on the navigation queue. This function is
        registered with each routine to be run on completion """
        with self.nav_lock:
            if not self.nav_queue.empty():
                # Disable idle if running
                self.idle_routine.reset()

                self.current_routine = self.nav_queue.get()
                self.current_routine.on_done(self.__next_routine)
                self.current_routine.start()
            else:
                self.current_routine = None
                self.idle_routine.start()

    def idle(self):
        """ Clear the queue and run the idle routine """
        if self.idle_routine:
            self.idle_routine.reset()
            self.idle_routine.start()        

    def do(self, routine):
        """ Equivalent to a called to clear() followed by append() """
        self.clear()
        return self.append(routine)

    def append(self, routine):
        """ Append a routine to the navigation queue. As one routine finishes the
        next one in line is called until the queue is exhausted. After exhausting
        the queue the robot will idle """
        with self.nav_lock:
            self.nav_queue.put(routine)
            if self.current_routine == None:
                self.__next_routine()
        return routine

    def clear(self):
        """ Clear the navigation queue and cancel any running routine """
        with self.nav_lock:
            self.nav_queue = queue.Queue()
            if self.current_routine != None:
                self.current_routine.on_done(None)
                self.current_routine.cancel()
                self.current_routine = None
