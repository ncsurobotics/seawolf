#!/bin/sh
./bin/mixer &
./bin/yawpidpy &
./bin/depthpid &
./bin/pitchpid &

#./bin/rotpid &
#./bin/rollpid &
