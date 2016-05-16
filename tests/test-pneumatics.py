#!/usr/bin/env python
import seawolf
from time import sleep

SLEEP_TIME = 2

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("TEST-Pneumatics")

print("Issuing pneumatic fire requests:")
sleep(SLEEP_TIME)

#fire actuators 1 through 6
for i in range(1,7):
    cmd = ("PNEUMATICS_REQUEST","fire %d" % i)
    print("  %s: %s" % cmd)
    seawolf.notify.send(*cmd)
    sleep(SLEEP_TIME)
