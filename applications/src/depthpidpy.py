from __future__ import division
import seawolf
import math
import time

thruster_cap = 1.0
panic_depth = 12.0
panic_time = 8.0
init_downward_force = .1

def initial_e_dt(integral):
    if(math.fabs(integral) < .00001):
        return 0
    else:
        return init_downward_force / integral

def dataOut(mv):
    out = in_range(-1.0, mv, 1.0)

    seawolf.notify.send("THRUSTER_REQUEST", "Depth {}".format(out))

def in_range(a,x,b):
    if( x < a ):
        return a
    elif( x > b ):
        return b
    else:
        return x 

def main():
    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Depth PID")

    seawolf.var.subscribe("DepthPID.p")
    seawolf.var.subscribe("DepthPID.i")
    seawolf.var.subscribe("DepthPID.d")
    seawolf.var.subscribe("DepthPID.Heading")
    seawolf.var.subscribe("DepthPID.Paused")
    seawolf.var.subscribe("Depth")

    depth = seawolf.var.get("Depth")
    paused = seawolf.var.get("DepthPID.Paused")

    pid = seawolf.PID( seawolf.var.get("DepthPID.Heading"), seawolf.var.get("DepthPID.p"), seawolf.var.get("DepthPID.i"), seawolf.var.get("DepthPID.d"))

    e_dt = initial_e_dt( seawolf.var.get("DepthPID.i") )
    dataOut(0.0)

    while(True):
        seawolf.var.sync()

        if(seawolf.var.stale("Depth")):
            depth = seawolf.var.get("Depth")

        if(seawolf.var.stale("DepthPID.p") or seawolf.var.stale("DepthPID.i") or seawolf.var.stale("DepthPID.d")):
            pid.setCoefficients(seawolf.var.get("DepthPID.p"), seawolf.var.get("DepthPID.i"), seawolf.var.get("DepthPID.d"))

            e_dt = initial_e_dt( seawolf.var.get("DepthPID.i") )

        if(seawolf.var.poked("DepthPID.Heading")):
            pid.setSetPoint(seawolf.var.get("DepthPID.Heading"))
            if(paused):
                seawolf.var.set("DepthPID.Paused", 0.0)
                seawolf.var.set("PitchPID.Paused", 0.0)

        if(seawolf.var.stale("DepthPID.Paused")):
            paused = seawolf.var.get("DepthPID.Paused")
            if(paused):
                dataOut(0.0)
                seawolf.notify.send("PIDPAUSED", "Depth")
                pid.pause()
                e_dt = initial_e_dt( seawolf.var.get("DepthPID.i") )

        if(depth > panic_depth):
            seawolf.logging.log(seawolf.CRITICAL, "Depth: {}\n".format(depth))
            seawolf.logging.log(seawolf.CRITICAL, "I'm too deep! Rising full force!\n")

            dataOut(-1.0)
            time.sleep(panic_time)
        elif(paused == False):
            mv = pid.update(depth)
            mv = in_range(-thruster_cap, mv, thruster_cap)
            dataOut(mv)

    seawolf.close();

if __name__ == "__main__":
    main()
