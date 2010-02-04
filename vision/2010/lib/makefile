#TODO: Make sure this is an independant makefile, but also make sure some
#      options are inherited when it's run with "../"'s makefile
CC=gcc
CFLAGS=-g --std=c99 -pedantic -Wmissing-prototypes -fPIC
#CFLAGS+=-Wall -Werror
OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv) -DCV_NO_BACKWARD_COMPATIBILITY
LIB_FLAGS=$(CFLAGS) --shared

LIB_OBJECTS = $(patsubst src/%.c, bin/%.o, $(wildcard src/*.c))

LIB_NAME = vision_lib.o
BIN_DIR = $(PWD)/bin

all: $(LIB_NAME) $(BIN_DIR)

$(LIB_NAME): $(LIB_OBJECTS)
	$(CC) $(LIB_FLAGS)  $(LIB_OBJECTS) -o $(LIB_NAME)

$(BIN_DIR):
	mkdir $(BIN_DIR)

bin/%.o: src/%.c
	$(CC) $(OPENCV_FLAGS) $(CFLAGS) -Iinclude/ -c src/$*.c -o bin/$*.o

clean:
	rm bin/*.o
	rm $(LIB_NAME)
