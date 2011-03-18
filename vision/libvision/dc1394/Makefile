
CC = gcc
OPENCV_FLAGS = `pkg-config opencv --cflags`
OPENCV_LDFLAGS = `pkg-config opencv --libs`
CFLAGS = -fPIC --shared $(OPENCV_FLAGS)
LDFLAGS = -ldc1394 $(OPENCV_LDFLAGS)

# For Debugging
CFLAGS += -g

all: dc1394.so

dc1394.so: dc1394.o Makefile
	$(CC) $(CFLAGS) $(LDFLAGS) dc1394.o -o dc1394.so

dc1394.o: dc1394.c Makefile
	$(CC) $(CFLAGS) -c dc1394.c -o dc1394.o

clean:
	-rm dc1394.so
	-rm dc1394.o
