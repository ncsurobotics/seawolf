
import threading

import seawolf as sw

import pid
from mixer import mixer
from data import data

class NavRoutine(object):
    interactions = []

    def __init__(self, timeout=-1):
        self.cleared = False
        self.routine_lock = threading.Lock()
        self.running = False
        self.timeout = timeout
        self.on_cancel_callback = None
        
    def run(self):
        """ Provided by implementation """
        pass

    def stop(self):
        """ Provided by implementation """
        pass

    def start(self):
        with self.routine_lock:
            if self.cleared:
                return
            else:
                self.running = True
                if self.timeout > 0:
                    timer.Timer(self.timeout, self.cancel)
                self.run()

    def cancel(self):
        with self.routine_lock:
            if self.running:
                self.stop()
                if self.on_cancel_callback:
                    self.on_cancel_callback()
            self.cleared = True
            self.running = False

    def reset(self):
        with self.routine_lock:
            if self.running:
                self.cancel()
            self.cleared = False

    def get_interactions(self):
        return set(self.interactions)

    def on_cancel(self, callback):
        self.on_cancel_callback = callback

class CompoundInterferenceException(Exception):
    pass

class CompoundRoutine(NavRoutine):
    """ Run multiple routines simultaneously """

    def __init__(self, routines, timeout=-1):
        super(CompoundRoutine, self).__init__(timeout)
        self.routines = routines

        interactions = [r.get_interactions() for r in routines]
        if not pairwise_disjoint(*interactions):
            raise CompoundInterferenceException("Illegal conflict in navigation routine interactions")

        self.interactions = set().union(*interactions)

    def run(self):
        for routine in self.routines:
            routine.start()
            
    def stop(self):
        for routine in self.routines:
            routine.cancel()

def pairwise_disjoint(*args):
    for i in range(0, len(args) - 1):
        for e in args[i+1:]:
            if not e.isdisjoint(args[i]):
                return False
    return True

def HoldPosition():
    return CompoundRoutine((HoldDepth(), HoldYaw(), Forward(0), Strafe(0)))

class SetDepth(NavRoutine):
    interactions = ("Depth",)

    def __init__(self, depth, timeout=-1):
        super(SetDepth, self).__init__(timeout)
        self.depth = depth

    def start(self):
        pid.depth.heading = self.depth

class RelativeDepth(NavRoutine):
    interactions = ("Depth",)

    def __init__(self, amount, timeout=-1):
        super(RelativeDepth, self).__init__(timeout)
        self.amount = amount

    def start(self):
        pid.depth.heading = max(data.depth + self.amount, 0)

def HoldDepth():
    return RelativeDepth(0)

class SetYaw(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, angle, timeout=-1):
        super(SetYaw, self).__init__(timeout)
        self.angle = angle

    def start(self):
        pid.yaw.heading = self.angle

class RelativeYaw(NavRoutine):
    interactions = ("Yaw",)

    def __init__(self, amount, timeout=-1):
        super(RelativeYaw, self).__init__(timeout)
        self.amount = amount
        if amount > 180 or amount < -180:
            raise ValueError("Invalid relative yaw value of %.2f" % (amount,))
        
    def start(self):
        new_yaw = data.imu.yaw + self.amount
        if new_yaw > 180:
            new_yaw = (new_yaw - 360)
        elif new_yaw < -180:
            new_yaw = (new_yaw + 360)
        pid.yaw.heading = new_yaw

def HoldYaw():
    return RelativeYaw(0)

class Forward(NavRoutine):
    interactions = ("Forward",)
    
    def __init__(self, rate, timeout=-1):
        super(Forward, self).__init__(timeout)
        self.rate = rate

    def start(self):
        mixer.forward = self.rate

    def stop(self):
        mixer.forward = 0.0

class Strafe(NavRoutine):
    interactions = ("Strafe",)
    
    def __init__(self, rate, timeout=-1):
        super(Strafe, self).__init__(timeout)
        self.rate = rate

    def start(self):
        mixer.strafe = self.rate

    def stop(self):
        mixer.strafe = 0.0
