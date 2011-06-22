
CC = gcc

OPENCV_FLAGS = $(shell pkg-config opencv --cflags)
OPENCV_LDFLAGS = $(shell pkg-config opencv --libs)

CFLAGS = -fPIC $(OPENCV_FLAGS)
LDFLAGS = --shared $(OPENCV_LDFLAGS)

# For Debugging
CFLAGS += -g

SOURCES = $(wildcard src/*.c)
SHARED_OBJECTS = $(SOURCES:%.c=%.so)

all: $(SHARED_OBJECTS)

%.so: %.c Makefile
	$(CC) $(LDFLAGS) $(CFLAGS) $(shell cat $(<:%.c=%.flags) 2>/dev/null) -o $@ $<

clean:
	rm $(SHARED_OBJECTS)

.PHONY: all clean
