
export SW_TOPDIR=$(PWD)/../..
include $(SW_TOPDIR)/mk/common.mk

SHELL = /bin/sh
CC=gcc
CFLAGS=-g --std=c99 -pedantic -Wmissing-prototypes
CFLAGS+=-Wall -Werror -Wno-unused
CFLAGS +=-I../../include/ -I./ -lutil

# Handle debug.mk
$(shell cp -u debug.mk.default debug.mk)
include debug.mk
export VISION_LIB_FLAGS=$(DEBUG_FLAGS)
CFLAGS +=$(DEBUG_FLAGS)

OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv) \
             -DCV_NO_BACKWARD_COMPATIBILITY
SEAWOLF_FLAGS=-I$(LIBSEAWOLF_INCLUDE_DIR) -lseawolf -L$(LIBSEAWOLF_LIB_DIR)
VISION_LIB_IFLAGS=-Ilib/include/
MISSION_FLAGS=$(CFLAGS) $(OPENCV_FLAGS) $(VISION_LIB_IFLAGS) $(DEBUG_FLAGS) $(SEAWOLF_FLAGS)
ALL_FLAGS=$(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) $(VISION_LIB_IFLAGS) \
          $(DEBUG_FLAGS)
MISSION_OBJS=$(patsubst missions/%.c, \
                        missions/bin/%.o, \
                        $(wildcard missions/*.c) \
              )

$(shell mkdir -p $(PWD)/bin)
$(shell mkdir -p $(PWD)/missions/bin)

all: vision_lib main 
main: $(MISSION_OBJS) bin/control.o bin/util.o bin/main.o
	$(CC) $(ALL_FLAGS) bin/*.o lib/vision_lib.o $(MISSION_OBJS) -o main

#switcher: $(MISSION_OBJS) bin/switcher.o
#	$(CC) $(ALL_FLAGS) lib/vision_lib.o bin/switcher.o -o switcher

vision_lib:
	$(MAKE) -C lib

missions/bin/%.o: missions/%.c
	$(CC) $(MISSION_FLAGS) -c missions/$*.c -o missions/bin/$*.o

bin/%.o: %.c
	$(CC) $(ALL_FLAGS) -c $*.c -o bin/$*.o

clean:
	-rm missions/bin/*.o
	-rm main
	-rm bin/*.o
	$(MAKE) -C lib clean
