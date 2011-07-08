#!/bin/sh
killall mixer
#killall tracker
#killall trackerproxy
killall depthpid
killall yawpid
#killall rotpid
#killall rollpid
#killall pitchpid
./bin/zerothrusters
