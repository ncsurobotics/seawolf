CC = gcc
CFLAGS=-g --std=c99
OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv)
SEAWOLF_FLAGS = -I../../libseawolf/include/ -lseawolf -L../../libseawolf/

MISSION_FLAGS = $(CFLAGS) $(OPENCV_FLAGS)
ALL_FLAGS = $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS)

MISSION_OBJS = $(patsubst missions/%.c, missions/bin/%.o, $(wildcard missions/*.c))

all: main

main: vision_lib $(MISSION_OBJS)
	$(CC) $(ALL_FLAGS) -c main.c

missions/bin:
	mkdir missions/bin

vision_lib:
	$(MAKE) -C lib

missions/bin/%.o: vision_lib missions/%.c missions/bin
	$(CC) $(MISSION_FLAGS) -c missions/$*.c -o missions/bin/$*.o
