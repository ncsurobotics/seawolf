#!/bin/sh
./bin/mixer &
./bin/yawpid &
./bin/depthpid &
./bin/pitchpid &

#./bin/rotpid &
#./bin/rollpid &
