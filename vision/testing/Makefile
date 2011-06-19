
CFLAGS= -g --std=c99 -Wall

all:
	gcc $(CFLAGS) `pkg-config --cflags --libs opencv` -lseawolf newblob.c ../libvision/cmodules/src/blob.c -o newblob

.PHONY: all
