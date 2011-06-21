
CC = gcc
OPENCV_FLAGS = `pkg-config opencv --cflags`
OPENCV_LDFLAGS = `pkg-config opencv --libs`
CFLAGS = -fPIC --shared $(OPENCV_FLAGS)
LDFLAGS = $(OPENCV_LDFLAGS)

# For Debugging
CFLAGS += -g

SOURCES = $(wildcard src/*.c)
OBJECTS = $(SOURCES:%.c=%.o)
SHARED_OBJECTS = $(SOURCES:%.c=%.so)

all: $(SHARED_OBJECTS)

%.so: %.o Makefile
	$(CC) $(CFLAGS) $(shell cat $(<:%.o=%.flags) 2>/dev/null) $(LDFLAGS) $< -o $@

%.o: %.c Makefile
	$(CC) $(CFLAGS) $(shell cat $(<:%.c=%.flags) 2>/dev/null) -c $< -o $@

clean:
	-rm $(OBJECTS) $(SHARED_OBJECTS)
