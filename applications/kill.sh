#!/bin/sh

killall mixer
killall depthpid
killall yawpid
killall pitchpid

pkill -f ".*pitchpidpy"
pkill -f ".*yawpidpy"
pkill -f ".*rollpidpy"

./bin/zerothrusters
