#!/bin/sh
g++ -L/usr/local/lib/active -L`pwd`/../libseawolf/ -I`pwd`/../libseawolf/include/ -I/usr/local/include/active -lseawolf -lcxutils -ljauscore -ljausextras -ljausmobility -ltinyxml jaus.cpp -o jaus
