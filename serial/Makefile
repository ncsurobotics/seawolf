
export CC= gcc
export CFLAGS= --std=c99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../libseawolf/include/ -g
export LDFLAGS= -L$(PWD)/../libseawolf/ -lseawolf -lrt
export BIN_DIR= $(PWD)/bin

all: $(BIN_DIR)
	$(MAKE) -C src

clean:
	$(MAKE) -C src clean

$(BIN_DIR):
	mkdir $(BIN_DIR)

.PHONY: all clean
