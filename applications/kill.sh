#!/bin/sh

killall mixer
killall depthpidpy
killall yawpidpy
killall pitchpidpy

#pkill -f ".*pitchpidpy"
#pkill -f ".*yawpidpy"
#pkill -f ".*rollpidpy"
#pkill -f ".*depthpidpy"

./bin/zerothrusters

