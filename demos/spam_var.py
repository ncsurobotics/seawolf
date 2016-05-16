import seawolf
import time

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("spam var")

VAR = 'SEA.Yaw'

i = 0
while 1:
    cmd = (VAR,(i % 100) / 100.0)
    print cmd
    seawolf.var.set(*cmd)
    time.sleep(0.1)
    i+=1
