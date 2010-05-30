#!/bin/sh
C="gcc -g --std=c99 -pedantic -Wall -I../../libseawolf/include -L../../libseawolf/ -lcv -lhighgui -lseawolf -lrt -lm -o tunavision *.c"
#C="gcc -O2 --std=c99 -pedantic -Wall -I../../libseawolf/include -L../../libseawolf/ -lcv -lhighgui -lseawolf -lrt -lm -o tunavision *.c"
echo $C $CFLAGS 
exec $C $CFLAGS
