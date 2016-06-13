from __future__ import division
import seawolf
import math
import time

ACTIVE_REGION_SIZE = 10 #degrees
MAX_RANGE = 0.8


def dataOut(mv):
    out = in_range(-MAX_RANGE, mv, MAX_RANGE)
    seawolf.notify.send("THRUSTER_REQUEST", "Roll {}".format(out))


def in_range(a, x, b):
    if(x < a):
        return a
    elif(x > b):
        return b
    else:
        return x


def main():
    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Roll PID")

    seawolf.var.subscribe("RollPID.p")
    seawolf.var.subscribe("RollPID.i")
    seawolf.var.subscribe("RollPID.d")
    seawolf.var.subscribe("RollPID.Heading")
    seawolf.var.subscribe("RollPID.Paused")
    seawolf.var.subscribe("SEA.Roll")

    roll = seawolf.var.get("SEA.Roll")
    paused = seawolf.var.get("RollPID.Paused")
    pid = seawolf.PID(
        seawolf.var.get("RollPID.Heading"),
        seawolf.var.get("RollPID.p"),
        seawolf.var.get("RollPID.i"),
        seawolf.var.get("RollPID.d")
    )
    
    # set active region (region where response of the robot
    # is practically linear). Outside this region, thrusters
    # would be maxed out, and the ITerm would get staturated.
    # Outside this region, the we use PD control. Inside this
    # region, we use PID control.
    pid.setActiveRegion(ACTIVE_REGION_SIZE)

    dataOut(0.0)
    mv = 0.0

    while(True):
        seawolf.var.sync()

        if seawolf.var.stale("SEA.Roll"):
            roll = seawolf.var.get("SEA.Roll")

        if seawolf.var.poked("RollPID.Heading"):
            pid.setSetPoint(seawolf.var.get("RollPID.Heading"))

            if paused:
                seawolf.var.set("RollPID.Paused", 0.0)

        if (seawolf.var.stale("RollPID.p") or seawolf.var.stale("RollPID.i") or seawolf.var.stale("RollPID.d")):

            pid.setCoefficients(
                seawolf.var.get("RollPID.p"),
                seawolf.var.get("RollPID.i"),
                seawolf.var.get("RollPID.d")
            )
            pid.resetIntegral()  # init e dt

        if (seawolf.var.stale("RollPID.Paused")):
            paused = seawolf.var.get("RollPID.Paused")

            if paused:
                dataOut(0.0)
                seawolf.notify.send("PIDPAUSED", "Roll")
                pid.pause()

        if not paused:
            mv = pid.update(roll)
            dataOut(mv)

    seawolf.close()

if __name__ == "__main__":
    main()
