
export CC= gcc
#export CFLAGS= --std=c99 -Wall -Werror -pedantic -Wmissing-prototypes -I$(PWD)/include -O2 -fPIC
#export CFLAGS= --std=c99 -Wall -Werror -pedantic -Wmissing-prototypes -I$(PWD)/include -Os -fPIC
export CFLAGS= --std=c99 -Wall -Werror -pedantic -Wmissing-prototypes -I$(PWD)/include -g -fPIC
export LIB_PATH=$(PWD)
export LIB_NAME=$(LIB_PATH)/libseawolf.so
export HUB_NAME=$(PWD)/hub

all:
	$(MAKE) -C src 

clean:
	$(MAKE) -C src clean
	rm -rf doc

doc:
	doxygen Doxyfile

%:
	$(MAKE) -C src $(PWD)/$@

.PHONY: all clean doc
