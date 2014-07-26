#!/bin/sh
./bin/mixer &
./bin/yawpidpy &
./bin/depthpidpy &
./bin/pitchpidpy &
./bin/rollpidpy &

#./bin/rotpidpy &
