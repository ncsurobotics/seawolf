SHELL = /bin/sh
CC=gcc
CFLAGS=-g --std=c99 -pedantic -Wmissing-prototypes -fPIC
CFLAGS+=-Wall -Werror -Wno-unused -fPIC
OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv) \
             -DCV_NO_BACKWARD_COMPATIBILITY
LIB_FLAGS=$(CFLAGS) --shared $(OPENCV_FLAGS)

LIB_OBJECTS = $(patsubst src/%.c, bin/%.o, $(wildcard src/*.c))
LIB_NAME = libvision.so
BIN_DIR = $(PWD)/bin
CFLAGS += $(VISION_LIB_FLAGS) # Inherited from an upper level makefile

$(shell mkdir -p $(BIN_DIR))

all: $(LIB_NAME)

$(LIB_NAME): $(LIB_OBJECTS)
	$(CC) $(LIB_FLAGS) $(LIB_OBJECTS) -o $(LIB_NAME)

bin/%.o: src/%.c
	$(CC) $(OPENCV_FLAGS) $(CFLAGS) -Iinclude/ -c src/$*.c -o bin/$*.o

doc: Doxyfile src/* include/* include/*/*
	doxygen Doxyfile

clean:
	-rm bin/*.o
	-rm $(LIB_NAME)
