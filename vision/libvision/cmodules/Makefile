
CC = gcc


OPENCV_FLAGS = $(shell pkg-config opencv --cflags)
OPENCV_LDFLAGS = $(shell pkg-config opencv --libs)

CFLAGS = -fPIC $(OPENCV_FLAGS)
LDFLAGS = --shared $(OPENCV_LDFLAGS)

# For Debugging
CFLAGS += -g
CFLAGS += -std=c99

SOURCES = $(wildcard src/*.c)
SHARED_OBJECTS = $(SOURCES:%.c=%.so)

all: $(SHARED_OBJECTS)

%.so: %.c Makefile
	$(CC) $(CFLAGS) $< $(LDFLAGS) $(shell cat $(<:%.c=%.flags) 2>/dev/null) -o $@

clean:
	rm $(SHARED_OBJECTS)

.PHONY: all clean
