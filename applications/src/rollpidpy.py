from __future__ import division
import seawolf
import math
import time


def dataOut(mv):
    out = in_range(-1.0, mv, 1.0)
    seawolf.notify.send("THRUSTER_REQUEST", "Roll {} {}".format(out, -out))


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

    dataOut(0.0)
    mv = 0.0

    while(True):
        seawolf.var.sync()

        if (seawolf.var.stale("SEA.Roll") and not paused):
            roll = seawolf.var.get("SEA.Roll")

        if (seawolf.var.stale("RollPID.p") or seawolf.var.stale("RollPID.i") or seawolf.var.stale("RollPID.d")):

            pid.setCoefficients(
                seawolf.var.get("RollPID.p"),
                seawolf.var.get("RollPID.i"),
                seawolf.var.get("RollPID.d")
            )
            pid.resetIntegral()  # init e dt

        if (seawolf.var.poked("RollPID.Heading")):
            pid.setSetPoint(seawolf.var.get("RollPID.Heading"))

            if paused:
                seawolf.var.set("RollPID.Paused", 0.0)

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
