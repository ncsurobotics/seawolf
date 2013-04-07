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
    paused = seawolf.var.get("PitchPID.Paused")
    seawolf.notify.filter(seawolf.FILTER_MATCH, "UPDATED PitchPID.Coeffcients")
    seawolf.notify.filter(seawolf.FILTER_MATCH, "UPDATED PitchPID.Heading")
    seawolf.notify.filter(seawolf.FILTER_MATCH, "UPDATED PitchPID.Paused")
    seawolf.notify.filter(seawolf.FILTER_MATCH, "UPDATED IMU")

    pid = seawolf.PID( seawolf.var.get("DepthPID.Heading"), seawolf.var.get("DepthPID.p"), seawolf.var.get("DepthPID.i"), seawolf.var.get("DepthPID.d"))

    dataOut(0.0)

    while(True):		
        data = seawolf.notify.get()
        pitch = seawolf.var.get("SEA.Pitch")
        if( data == "PitchPID.Coefficients"):
            pid.setCoefficients( seawolf.var.get("PitchPID.p"), seawolf.var.get("PitchPID.i"), seawolf.var.get("PitchPID.d"))
            pid.resetIntegral() 
        elif( data == "PitchPID.Heading"):
            pid.setSetPoint(seawolf.var.get("PitchPID.Heading"))
            mv = pid.update(pitch)
            if(paused):
                seawolf.var.set("PitchPID.Paused", 0.0)
        elif( data == "PitchPID.Paused"):
            p = seawolf.var.get("PitchPID.Paused")
            if(p == paused):
                continue
            paused = p
            if(paused):
                dataOut(0.0)
                seawolf.notify.send("PIDPAUSED", "Pitch")        
        elif( data == "IMU" and paused == False):
            mv = pid.update(pitch);
        
        if(paused == False):
            dataOut(mv)

    seawolf.close()

if __name__ == "__main__":
	main()
