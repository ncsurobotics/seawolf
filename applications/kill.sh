#!/bin/sh
killall mixer
#killall tracker
#killall trackerproxy
killall depthpidpy
killall yawpid
#killall rotpid
#killall rollpid
killall pitchpid
./bin/zerothrusters
