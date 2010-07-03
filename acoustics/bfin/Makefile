
CC= bfin-linux-uclibc-gcc
CFLAGS= -g --std=gnu99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../../libseawolf/include
LDFLAGS= -L$(PWD)/../../libseawolf/ -lseawolf-bfin -lbfdsp -lm

#CC= bfin-uclinux-gcc
#CFLAGS= -static --std=gnu99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../../libseawolf/include -I$(PWD)/include
#LDFLAGS= -L$(PWD)/../../libseawolf -lbfdsp -lm -Wl,-elf2flt

# Enable the use of libseawolf (when not in testing)
#CFLAGS+= -DUSE_LIBSEAWOLF

BIN_DIR= $(PWD)/bin
BIN_NAME= acoustics-bfin

#SRCS= src/acoustics_math.c src/main.c
#INCLUDES= include/acoustics_math.h
SRCS= src/main.c src/routines.c
INCLUDES= src/acoustics.h

all: $(BIN_DIR)/$(BIN_NAME)

clean:
	@if [ -f $(BIN_DIR)/$(BIN_NAME) ]; then \
	  echo rm $(BIN_DIR)/$(BIN_NAME); \
	  rm $(BIN_DIR)/$(BIN_NAME); \
	fi;

bundle: $(BIN_DIR)/$(BIN_NAME)
	@./bundle.sh

bundle_push:
	scp acoustics.tar seawolf@10.17.0.2:acoustics_bundle/acoustics.tar

$(BIN_DIR)/$(BIN_NAME): $(BIN_DIR) $(SRCS) $(INCLUDES)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/$(BIN_NAME) $(SRCS) $(LDFLAGS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

.PHONY: all clean bundle bundle_push
