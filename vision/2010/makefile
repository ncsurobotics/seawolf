CC=gcc
CFLAGS=-g --std=c99 -pedantic -Wmissing-prototypes
#CFLAGS+=-Wall -Werror

#OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv) -DCV_NO_BACKWARD_COMPATIBILITY
OPENCV_FLAGS=-I/usr/local/include/opencv -lcxcore -lcv -lhighgui -lcvaux -lml -DCV_NO_BACKWARD_COMPATIBILITY
SEAWOLF_FLAGS=-I../../libseawolf/include/ -lseawolf -L../../libseawolf/
VISION_LIB_FLAGS=-Ilib/include/
MISSION_FLAGS=$(CFLAGS) $(OPENCV_FLAGS) $(VISION_LIB_FLAGS)
ALL_FLAGS=$(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) $(VISION_LIB_FLAGS)

MISSION_OBJS=$(patsubst missions/%.c, missions/bin/%.o, $(wildcard missions/*.c))

all: main bin/ missions/bin/

main: vision_lib $(MISSION_OBJS) bin/main.o
	$(CC) $(ALL_FLAGS) bin/main.o lib/vision_lib.o missions/bin/*.o -o main

missions/bin/:
	@mkdir missions/bin/

bin/:
	@mkdir bin/

vision_lib:
	$(MAKE) -C lib

missions/bin/%.o: vision_lib missions/%.c missions/bin
	$(CC) $(MISSION_FLAGS) -c missions/$*.c -o missions/bin/$*.o

bin/%.o:
	$(CC) $(ALL_FLAGS) -c $*.c -o bin/$*.o

clean:
	rm missions/bin/*.o
	rm main 
	rm bin/*.o
