
import Queue as queue
import threading

# Import navigation routines
from routines import *

# Navigational primitives that the mixer can handle
interactions = ("Yaw",
                "Forward",
                "Depth",
                "Pitch",
                "Strafe")

current_routine = None
nav_queue = queue.Queue()
nav_lock = threading.RLock()

# Idle when not given anything else to do
idle = False
idle_routine = HoldPosition()

def next_routine():
    with nav_lock:
        if not nav_queue.empty():
            # Disable idle if running
            if idle:
                set_idle(False)
            current_routine = nav_queue.get()
            current_routine.on_done(next_routine)
            current_routine.start()
        else:
            set_idle(True)
            current_routine = None

def set_idle(do_idle):
    global idle

    if do_idle:
        idle = True
        idle_routine.reset()
        idle_routine.start()
    else:
        idle = False
        idle_routine.cancel()

def init():
    """ Initialze navigation by having the robot idle """
    set_idle(True)

def do(routine):
    """ Clear the nav queue and begin executing the given routine """
    with nav_lock:
        nav_queue = queue.Queue()
        if current_routine != None:
            current_routine.cancel()
    return append(routine)

def append(routine):
    """ Append a routine to the navigation queue. As one routine finishes the
    next one in line is called until the queue is exhausted. After exhausting
    the queue the robot will idle """
    with nav_lock:
        nav_queue.put(routine)
        next_routine()
    return routine

def clear():
    """ Clear the navigation queue and set the robot to idle """
    with nav_lock:
        nav_queue = queue.Queue()
        if current_routine != None:
            current_routine.cancel()
        set_idle(True)
