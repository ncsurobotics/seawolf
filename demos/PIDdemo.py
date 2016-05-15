import seawolf

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("PID")

#YAW
seawolf.var.subscribe("YawPID.p")
seawolf.var.subscribe("YawPID.i")
seawolf.var.subscribe("YawPID.d")
seawolf.var.subscribe("YawPID.Heading")
seawolf.var.subscribe("YawPID.Paused")
seawolf.var.subscribe("SEA.Yaw")

#DEPTH
seawolf.var.subscribe("DepthPID.p")
seawolf.var.subscribe("DepthPID.i")
seawolf.var.subscribe("DepthPID.d")
seawolf.var.subscribe("DepthPID.Heading")
seawolf.var.subscribe("DepthPID.Paused")
seawolf.var.subscribe("Depth")

#subscribe to PITCH PID
seawolf.var.subscribe("PitchPID.p")
seawolf.var.subscribe("PitchPID.i")
seawolf.var.subscribe("PitchPID.d")
seawolf.var.subscribe("PitchPID.Heading")
seawolf.var.subscribe("PitchPID.Paused")
seawolf.var.subscribe("SEA.Pitch")

class PID:
    def __init__(self):
        pass
        

    def setPID(self, PID, val, param):
        cmd = "{}PID.{}".format(PID, param)
        seawolf.var.set(cmd, val)

    def printPID(self,PID, param):
        seawolf.var.sync()
        cmd = "{}PID.{}".format(PID, param)
        val = seawolf.var.get(cmd)
        print val
        

pid = PID()
