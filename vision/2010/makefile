CC = gcc
CFLAGS= -g --std=c99 -Wall -Werror -pedantic -pedantic -Wmissing-prototypes

OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv)
SEAWOLF_FLAGS = -I../../libseawolf/include/ -lseawolf -L../../libseawolf/
VISION_LIB_FLAGS=-Ilib/include/ -Llib/ -lvision_lib
MISSION_FLAGS = $(CFLAGS) $(OPENCV_FLAGS) $(VISION_LIB_FLAGS)
ALL_FLAGS = $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) $(VISION_LIB_FLAGS)

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
