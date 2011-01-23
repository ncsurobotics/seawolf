
import threading
import time

import seawolf as sw

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

        self.on_done_callback = None
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
            if self.state == NavRoutine.CANCELED:
                self.__finished(NavRoutine.CANCELED)
            elif self.state == NavRoutine.RESET:
                self.state = NavRoutine.RUNNING
                if self.timeout_length > 0:
                    threading.Timer(self.timeout_length, self.timeout).start()
                self._start()
                if hasattr(self, "_poll"):
                    self.__start_poller()
            else:
                raise Exception("Routine state exception")

    def __poller(self):
        """ Polling thread. Will call self._poll every self.polling_interval
        seconds until self._poll indicates the routine has been completed """
        while not self.done_event.is_set():
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

            if self.on_done_callback:
                self.on_done_callback()

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

    def on_done(self, callback):
        self.on_done_callback = callback

class CompoundInterferenceException(Exception):
    pass

class CompoundRoutine(NavRoutine):
    """ Run multiple routines simultaneously """

    def __init__(self, routines, timeout=-1):
        super(CompoundRoutine, self).__init__(timeout)
        self.routines = routines

        interactions = [r.get_interactions() for r in routines]
        if not util.pairwise_disjoint(*interactions):
            raise CompoundInterferenceException("Illegal conflict in navigation routine interactions")

        self.interactions = set().union(*interactions)
        
    def _poll(self):
        # A CompoundRoutine is completed when all its constituent parts have
        # finished and it has not been canceled
        for routine in self.routines:
            routine.wait()

        if self.state == NavRoutine.RUNNING:
            return self.COMPLETED
        else:
            return self.state

    def _start(self):
        for routine in self.routines:
            routine.start()
            
    def _cleanup(self):
        for routine in self.routines:
            routine.cancel()

class NullRoutine(NavRoutine):
    """ The Null routine does nothing """
    pass

def HoldPosition():
    return CompoundRoutine((HoldDepth(), HoldYaw(), Forward(0), Strafe(0)))

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

    def __init__(self, amount, timeout=-1):
        super(RelativeDepth, self).__init__(timeout)
        self.amount = amount
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

class SetYaw(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, angle, timeout=-1, tolerance=5):
        super(SetYaw, self).__init__(timeout)
        self.angle = angle
        self.tolerance = tolerance

    def _poll(self):
        target_yaw = self.angle + 180
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
        pid.yaw.heading = self.angle

class RelativeYaw(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, amount, timeout=-1):
        super(RelativeYaw, self).__init__(timeout)
        self.amount = amount
        if amount > 180 or amount < -180:
            raise ValueError("Invalid relative yaw value of %.2f" % (amount,))
        
    def _poll(self):
        target_yaw = self.angle + 180
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

    def _cleanup(self):
        mixer.forward = 0.0

class Strafe(NavRoutine):
    interactions = ("Strafe",)
    
    def __init__(self, rate, timeout=-1):
        super(Strafe, self).__init__(timeout)
        self.rate = rate

    def _start(self):
        mixer.strafe = self.rate

    def _cleanup(self):
        mixer.strafe = 0.0

class EmergencyBreech(NavRoutine):
    def _start(self):
        # Pause the depth and pitch PIDs
        pid.depth.pause()
        pid.pitch.pause()

        time.sleep(0.5)

        # Instruct mixer to max out depth thrusters
        mixer.depth = 1.0

    def _stop(self):
        mixer.depth = 0.0;
