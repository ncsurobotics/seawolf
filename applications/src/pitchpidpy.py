from __future__ import division
import seawolf
import math
import time

def dataOut(mv):
    out = in_range(-1.0, mv, 1.0)
    seawolf.notify.send("THRUSTER_REQUEST", "Pitch {}".format(out))

def in_range(a,x,b):
    if( x < a ):
        return a
    elif( x > b ):
        return b
    else:
        return x

def main():
    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Pitch PID")
    
    seawolf.var.subscribe("PitchPID.p")
    seawolf.var.subscribe("PitchPID.i")
    seawolf.var.subscribe("PitchPID.d")
    seawolf.var.subscribe("PitchPID.Heading")
    seawolf.var.subscribe("PitchPID.Paused")
    seawolf.var.subscribe("SEA.Pitch")

    pitch = seawolf.var.get("SEA.Pitch")
    paused = seawolf.var.get("PitchPID.Paused")
    pid = seawolf.PID( seawolf.var.get("PitchPID.Heading"), seawolf.var.get("PitchPID.p"), seawolf.var.get("PitchPID.i"), seawolf.var.get("PitchPID.d"))

    dataOut(0.0)
    mv = 0.0

    while(True):
        seawolf.var.sync()
        if( seawolf.var.stale("SEA.Pitch") and paused == False):
            pitch = seawolf.var.get("SEA.Pitch")
            mv = pid.update(pitch)
        elif( seawolf.var.stale("PitchPID.p") or seawolf.var.stale("PitchPID.i") or seawolf.var.stale("PitchPID.d") ):
            pid.setCoefficients( seawolf.var.get("PitchPID.p"), seawolf.var.get("PitchPID.i"), seawolf.var.get("PitchPID.d"))
            pid.resetIntegral() #init e dt
        elif( seawolf.var.poked("PitchPID.Heading") ):
            pid.setSetPoint(seawolf.var.get("PitchPID.Heading"))
            mv = pid.update( seawolf.var.get("SEA.Pitch") )
            if(paused):
                seawolf.var.set("PitchPID.Paused", 0.0)
        elif( seawolf.var.stale("PitchPID.Paused")  ):
            p = seawolf.var.get("PitchPID.Paused")
            if(p == paused):
                continue
            
            paused = p
            if(paused):
                dataOut(0.0)
                seawolf.notify.send("PIDPAUSED", "Pitch")
                pid.pause()
        
        if(paused == False):
            dataOut(mv)

    seawolf.close()

if __name__ == "__main__":
    main()
