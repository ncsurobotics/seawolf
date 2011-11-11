
import threading
import time
import collections

import seawolf as sw

import sw3
import pid
import util
from mixer import mixer
from data import data

class NavRoutine(object):
    RESET = 0
    RUNNING = 1
    CANCELED = 2
    COMPLETED = 3
    TIMEDOUT = 4

    interactions = ()

    def __init__(self, timeout=-1):
        self.state = NavRoutine.RESET
        self.timeout_length = timeout

        self.routine_lock = threading.RLock()

        self.on_done_callbacks = []
        self.done_event = threading.Event()

        self.polling_thread = None
        self.polling_interval = 0.1

    def _start(self):
        """ Start the routine """
        pass

    def _cleanup(self):
        """ Perform any cleanup needed after the routine has finished """
        pass

    def start(self):
        with self.routine_lock:
            self.done_event.clear()
            self.state = NavRoutine.RUNNING
            if self.timeout_length > 0:
                threading.Timer(self.timeout_length, self.timeout).start()
            self._start()
            if hasattr(self, "_poll"):
                self.__start_poller()

    def __poller(self):
        """ Polling thread. Will call self._poll every self.polling_interval
        seconds until self._poll indicates the routine has been completed """
        while not self.done_event.is_set() and self.state == self.RUNNING:
            new_state = self._poll()

            if new_state == NavRoutine.COMPLETED:
                self.completed()
            elif new_state == NavRoutine.CANCELED:
                self.cancel()
            self.done_event.wait(self.polling_interval)

    def __start_poller(self):
        """ Start the polling thread """
        self.polling_thread = threading.Thread(target=self.__poller)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def __finished(self, new_state):
        with self.routine_lock:
            if self.state == NavRoutine.RUNNING:
                self._cleanup()

                self.state = new_state
                for callback in self.on_done_callbacks:
                    callback(new_state)

                self.state = new_state
                self.done_event.set()

    def cancel(self):
        self.__finished(NavRoutine.CANCELED)

    def completed(self):
        self.__finished(NavRoutine.COMPLETED)

    def timeout(self):
        self.__finished(NavRoutine.TIMEDOUT)

    def reset(self):
        with self.routine_lock:
            if self.state == NavRoutine.RUNNING:
                self.cancel()

            self.state = NavRoutine.RESET
            self.done_event.clear()

    def get_interactions(self):
        return set(self.interactions)

    def is_running(self):
        return (self.state == NavRoutine.RUNNING)

    def wait(self):
        self.done_event.wait()

    def on_done(self, action):

        # NavRoutine
        if isinstance(action, NavRoutine):
            def callback(state):
                if state == NavRoutine.COMPLETED or state == NavRoutine.TIMEDOUT:
                    sw3.nav.do(action)

        # Callback Function
        elif callable(action):
            callback = action

        else:
            raise ValueError("Argument must be a nav routine or a callable accepting one argument")

        self.on_done_callbacks.append(callback)

    def on_done_clear_callbacks(self):
        self.on_done_callbacks = []

class CompoundInterferenceException(Exception):
    pass

class CompoundRoutine(NavRoutine):
    """ Run multiple routines simultaneously """

    def __init__(self, *args, **kwargs):
        timeout = kwargs.pop("timeout", -1)
        if kwargs != {}:
            raise ValueError("Unexpected keyward arguments: %s" % kwargs)
        super(CompoundRoutine, self).__init__(timeout)

        # If there is only one argument and it is iterable, assume that the
        # user passed in a list of routines.  Otherwise assume that *args is a
        # list of routines.
        if len(args) == 0:
            raise ValueError("CompoundRoutine requires at least one argument.")
        elif len(args) == 1 and isinstance(args[0], collections.Iterable):
            self.routines = args[0]
        else:
            self.routines = args

        interactions = [r.get_interactions() for r in self.routines]
        if not util.pairwise_disjoint(*interactions):
            raise CompoundInterferenceException("Illegal conflict in navigation routine interactions")

        self.interactions = set().union(*interactions)

    def _poll(self):
        # A CompoundRoutine is completed when all its constituent parts have
        # finished and it has not been canceled
        for routine in self.routines:
            if routine.state == NavRoutine.RUNNING:
                return self.state

        if self.state == NavRoutine.RUNNING:
            return self.COMPLETED
        else:
            return self.state

    def _start(self):
        for routine in self.routines:
            routine.start()

    def _cleanup(self):
        for routine in self.routines:
            routine.reset()

class NullRoutine(NavRoutine):
    """ The Null routine does nothing """
    pass

def HoldPosition():
    return CompoundRoutine((Forward(0), Strafe(0)))

class ZeroThrusters(NavRoutine):
    interactions = ("Depth", "Yaw", "Stafe", "Forward")

    def _start(self):
        # Pause the PIDs
        pid.yaw.pause()
        pid.rotate.pause()
        pid.pitch.pause()
        pid.depth.pause()

        # Zero the mixer
        mixer.depth = 0
        mixer.pitch = 0
        mixer.yaw = 0
        mixer.forward = 0
        mixer.strafe = 0

        # Zero the thrusters
        for v in ("Port", "Star", "Bow", "Stern", "Strafe"):
            sw.var.set(v, 0)

class SetDepth(NavRoutine):
    interactions = ("Depth",)

    def __init__(self, depth, timeout=-1, tolerance=0.5):
        super(SetDepth, self).__init__(timeout)
        self.tolerance = tolerance
        self.depth = depth

    def _poll(self):
        if abs(self.depth - data.depth) <= self.tolerance:
            return NavRoutine.COMPLETED
        return NavRoutine.RUNNING

    def _start(self):
        pid.depth.heading = self.depth

class RelativeDepth(NavRoutine):
    interactions = ("Depth",)

    def __init__(self, amount, timeout=-1, tolerance=0.5):
        super(RelativeDepth, self).__init__(timeout)
        self.amount = amount
        self.tolerance = tolerance
        self.target_depth = None

    def _poll(self):
        if abs(self.target_depth - data.depth) <= self.tolerance:
            return NavRoutine.COMPLETED
        return NavRoutine.RUNNING

    def _start(self):
        self.target_depth = max(data.depth + self.amount, 0)
        pid.depth.heading = self.target_depth

class HoldDepth(RelativeDepth):
    def __init__(self, timeout=-1):
        super(HoldDepth, self).__init__(0, timeout)

    def _poll(self):
        self.wait()

class SetRotate(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, rate, timeout=-1):
        super(SetRotate, self).__init__(timeout)
        self.rate = rate

    def _start(self):
        # lol, this doesn't really work
        #pid.rotate.heading = self.rate
        pid.yaw.pause()
        sw.notify.send("THRUSTER_REQUEST", "Yaw %.2f" % (self.rate,))

class SetYaw(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, angle, timeout=-1, tolerance=5):
        super(SetYaw, self).__init__(timeout)
        self.angle = angle
        self.tolerance = tolerance
        self.i = 0

    def _poll(self):
        target_yaw = self.angle + 180
        current_yaw = data.imu.yaw + 180

        diff = abs(target_yaw - current_yaw)
        if diff > 180:
            target_yaw = (target_yaw + 180) % 360
            current_yaw = (current_yaw + 180) % 360
            diff = abs(target_yaw - current_yaw)

        if diff <= self.tolerance:
            self.i += 1
        else:
            self.i = 0

        if self.i >= 15:
            return NavRoutine.COMPLETED
        return NavRoutine.RUNNING

    def _start(self):
        pid.yaw.heading = self.angle

class RelativeYaw(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, amount, timeout=-1, tolerance=5):
        super(RelativeYaw, self).__init__(timeout)
        self.amount = amount
        self.tolerance = tolerance
        if amount > 180 or amount < -180:
            raise ValueError("Invalid relative yaw value of %.2f" % (amount,))

    def _poll(self):
        target_yaw = self.target_yaw + 180
        current_yaw = data.imu.yaw + 180

        diff = abs(target_yaw - current_yaw)
        if diff > 180:
            target_yaw = (target_yaw + 180) % 360
            current_yaw = (current_yaw + 180) % 360
            diff = abs(target_yaw - current_yaw)

        if diff <= self.tolerance:
            return NavRoutine.COMPLETED
        return NavRoutine.RUNNING

    def _start(self):
        self.target_yaw = data.imu.yaw + self.amount
        if self.target_yaw > 180:
            self.target_yaw = (self.target_yaw - 360)
        elif self.target_yaw < -180:
            self.target_yaw = (self.target_yaw + 360)
        pid.yaw.heading = self.target_yaw

class HoldYaw(RelativeYaw):
    def __init__(self, timeout=-1):
        super(HoldYaw, self).__init__(0, timeout)

    def _poll(self):
        self.wait()

def TurnRight():
    return RelativeYaw(90)

def TurnLeft():
    return RelativeYaw(-90)

class Forward(NavRoutine):
    interactions = ("Forward",)

    def __init__(self, rate, timeout=-1):
        super(Forward, self).__init__(timeout)
        self.rate = rate

    def _start(self):
        mixer.forward = self.rate

class Strafe(NavRoutine):
    interactions = ("Strafe",)

    def __init__(self, rate, timeout=-1):
        super(Strafe, self).__init__(timeout)
        self.rate = rate

    def _start(self):
        mixer.strafe = self.rate

    def _cleanup(self):
        mixer.strafe = 0.0

class EmergencyBreech(ZeroThrusters):
    def _start(self):
        # Zero the thrusters by calling to the super class
        super(EmergencyBreech, self)._start()
        mixer.depth = -1.0

    def _poll(self):
        # Set the mixer depth value each time polled incase a rogue program puts
        # it back
        mixer.depth = -1.0
        return NavRoutine.RUNNING

    def _stop(self):
        # Zero depth thrusters
        mixer.depth = 0.0;

def sequence_routines(*routines):
    """ Chains the given routines together with on_done callbacks such that
    they run one after the other.

    Return the first routine in the sequence.

    """
    for i in xrange(1, len(routines)-1):
        routines[i-1].on_done(routines[i])
    return routines[0]


def loop_routines(*routines):
    """ Chains the given routines together with on_done callbacks such that
    they run one after the other and loop infinitely.

    Return the first routine in the sequence.

    """
    for i in xrange(len(routines)):
        routines[i-1].on_done(routines[i])
    return routines[0]

class LoopRoutine(NavRoutine):
    """ Routine that executes the given routines in order then repeats. """

    def __init__(self, *args, **kwargs):
        timeout = kwargs.pop("timeout", -1)
        if kwargs != {}:
            raise ValueError("Unexpected keyward arguments: %s" % kwargs)
        super(LoopRoutine, self).__init__(timeout)

        self.routine_counter = 0

        # If there is only one argument and it is iterable, assume that the
        # user passed in a list of routines.  Otherwise assume that *args is a
        # list of routines.
        if len(args) == 0:
            raise ValueError("LoopRoutine requires at least one argument.")
        elif len(args) == 1 and isinstance(args[0], collections.Iterable):
            self.routines = args[0]
        else:
            self.routines = args

        # Calculate interactions
        interactions = [r.get_interactions() for r in self.routines]
        self.interactions = set().union(*interactions)

    def _poll(self):

        current_routine = self.routines[self.routine_counter]
        if hasattr(current_routine, "_poll"):
            new_state = current_routine._poll()
        else:
            new_state = current_routine.state

        if new_state == NavRoutine.COMPLETED or new_state == NavRoutine.TIMEDOUT:
            # Move to next routine
            self.routine_counter = (self.routine_counter+1) % len(self.routines)
            new_routine = self.routines[self.routine_counter]
            new_routine.start()

        elif new_state == NavRoutine.CANCELED:
            self.cancel()

        return self.state

    def _start(self):
        self.routines[self.routine_counter].start()

    def _cleanup(self):
        for routine in self.routines:
            routine.reset()

class SequentialRoutine(NavRoutine):
    """ Routine that executes the given routines in order then exits. """

    def __init__(self, *args, **kwargs):
        timeout = kwargs.pop("timeout", -1)
        if kwargs != {}:
            raise ValueError("Unexpected keyward arguments: %s" % kwargs)
        super(SequentialRoutine, self).__init__(timeout)

        self.routine_counter = 0

        # If there is only one argument and it is iterable, assume that the
        # user passed in a list of routines.  Otherwise assume that *args is a
        # list of routines.
        if len(args) == 0:
            raise ValueError("SequentialRoutine requires at least one argument.")
        elif len(args) == 1 and isinstance(args[0], collections.Iterable):
            self.routines = args[0]
        else:
            self.routines = args

        # Calculate interactions
        interactions = [r.get_interactions() for r in self.routines]
        self.interactions = set().union(*interactions)

    def _poll(self):

        current_routine = self.routines[self.routine_counter]
        if hasattr(current_routine, "_poll"):
            new_state = current_routine._poll()
        else:
            new_state = current_routine.state

        if new_state == NavRoutine.COMPLETED or new_state == NavRoutine.TIMEDOUT:
            # Move to next routine
            self.routine_counter += 1
            if self.routine_counter == len(self.routines):
                return NavRoutine.COMPLETED
            new_routine = self.routines[self.routine_counter]
            new_routine.start()

        elif new_state == NavRoutine.CANCELED:
            self.cancel()

        return self.state

    def _start(self):
        self.routines[self.routine_counter].start()

    def _cleanup(self):
        for routine in self.routines:
            routine.reset()
