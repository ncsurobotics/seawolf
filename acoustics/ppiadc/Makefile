obj-m := ppiadc.o

KERNEL_SRC ?= ../blackfin-linux-dist/linux-2.6.x/

all:
	make -C $(KERNEL_SRC) SUBDIRS=$(PWD) modules

clean:
	make -C $(KERNEL_SRC) SUBDIRS=$(PWD) clean

.PHONY: all clean
