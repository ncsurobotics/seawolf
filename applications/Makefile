
export CC= gcc
export CFLAGS= --std=c99 -Wall -Werror -pedantic -Wmissing-prototypes -I$(PWD)/../libseawolf/include -O2
export BIN_DIR= $(PWD)/bin
export LDFLAGS= -lncurses -lrt -lseawolf -lpthread -L$(PWD)/../libseawolf/

all: $(BIN_DIR)
	$(MAKE) -C src

clean:
	$(MAKE) -C src clean

$(BIN_DIR):
	mkdir $(BIN_DIR)

.PHONY: all clean
