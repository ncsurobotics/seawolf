
CC= bfin-linux-uclibc-gcc
CFLAGS= --std=gnu99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../../libseawolf/include -I$(PWD)/include
LDFLAGS= -L$(PWD)/../../libseawolf/ -lseawolf-bfin -lbfdsp -lm

#CC= bfin-uclinux-gcc
#CFLAGS= --std=gnu99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../../libseawolf/include -I$(PWD)/include
#LDFLAGS= -L$(PWD)/../../libseawolf/ -lseawolf-bfin -lbfdsp -lm -Wl,-elf2flt

BIN_DIR= $(PWD)/bin
BIN_NAME= acoustics-bfin

SRCS= src/acoustics_math.c src/csv_io.c src/main.c
INCLUDES= include/acoustics_math.h include/csv_io.h

all: $(BIN_DIR)/$(BIN_NAME)

clean:
	@if [ -f $(BIN_DIR)/$(BIN_NAME) ]; then \
	  echo rm $(BIN_DIR)/$(BIN_NAME); \
	  rm $(BIN_DIR)/$(BIN_NAME); \
	fi;

$(BIN_DIR)/$(BIN_NAME): $(BIN_DIR) $(SRCS) $(INCLUDES)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/$(BIN_NAME) $(SRCS) $(LDFLAGS)

$(BIN_DIR):
	mkdir $(BIN_DIR)

.PHONY: all clean
