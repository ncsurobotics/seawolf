
export CC= gcc
export CFLAGS= --std=c99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/include -g
export LIB_NAME=$(PWD)/libseawolf.so
export HUB_NAME=$(PWD)/hub

all:
	$(MAKE) -C src 

clean:
	$(MAKE) -C src clean

%:
	$(MAKE) -C src $(PWD)/$@

.PHONY: all clean
