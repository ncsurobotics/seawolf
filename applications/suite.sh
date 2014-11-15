#!/bin/sh
./bin/mixer &
./bin/yawpidpy &
./bin/depthpid &
./bin/pitchpidpy &
./bin/rollpidpy &

#./bin/rotpidpy &
