SHELL = /bin/sh
CC=gcc
CFLAGS=-g --std=c99 -pedantic -Wmissing-prototypes -fPIC
CFLAGS+=-Wall -Werror -Wno-unused
OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv) \
             -DCV_NO_BACKWARD_COMPATIBILITY
LIB_FLAGS=$(CFLAGS) --shared

LIB_OBJECTS = $(patsubst src/%.c, bin/%.o, $(wildcard src/*.c))
LIB_NAME = vision_lib.o
BIN_DIR = $(PWD)/bin
CFLAGS += $(VISION_LIB_FLAGS) # Inherited from an upper level makefile


all: $(BIN_DIR) $(LIB_NAME) 

$(LIB_NAME): $(LIB_OBJECTS)
	$(CC) $(LIB_FLAGS)  $(LIB_OBJECTS) -o $(LIB_NAME)

$(BIN_DIR):
	-mkdir $(BIN_DIR)

bin/%.o: src/%.c
	$(CC) $(OPENCV_FLAGS) $(CFLAGS) -Iinclude/ -c src/$*.c -o bin/$*.o

clean:
	rm bin/*.o
	rm $(LIB_NAME)
