APPLICATION_NAME= <application name>

# -- end configuration -- #
CC= /usr/bin/gcc-4
CFLAGS= -Wall -pedantic --std=c99
OUTPUT_DIR= bin/
SRCS= src/*.c
INCLUDE_PATH= ../../libseawolf/include/
LIB_PATH= ../../libseawolf/

all:
	$(CC) $(CFLAGS) -I$(INCLUDE_PATH) -L$(LIB_PATH) \
	-o $(OUTPUT_DIR)$(APPLICATION_NAME) $(SRCS) -lseawolf

clean:
	-rm bin/*

.PHONY: all clean
