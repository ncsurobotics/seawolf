
export CC= gcc
#export CFLAGS= --std=c99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../libseawolf/include -O2
#export CFLAGS= --std=c99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../libseawolf/include -Os
export CFLAGS= --std=c99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../libseawolf/include -I$(PWD)/../include -g
export BIN_DIR= $(PWD)/bin
export LDFLAGS= -L$(PWD)/../libseawolf/ -lseawolf 

all: $(BIN_DIR)
	$(MAKE) -C src

clean:
	$(MAKE) -C src clean

$(BIN_DIR):
	mkdir $(BIN_DIR)

.PHONY: all clean
