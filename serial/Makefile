
export SW_TOPDIR ?= $(PWD)/..
include $(SW_TOPDIR)/mk/common.mk

export CC= gcc
export CFLAGS= --std=c99 -Wall -Werror -pthread -pedantic -Wmissing-prototypes -I$(LIBSEAWOLF_INCLUDE_DIR) -g
export LDFLAGS= -L$(LIBSEAWOLF_LIB_DIR) -lseawolf -lm
export BIN_DIR= bin

all: $(BIN_DIR)
	$(MAKE) -C src

clean:
	$(MAKE) -C src clean

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

.PHONY: all clean
