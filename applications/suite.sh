#!/bin/sh
./bin/mixer &
./bin/yawpid &
./bin/depthpidpy &
./bin/pitchpid &

#./bin/rotpid &
#./bin/rollpid &
