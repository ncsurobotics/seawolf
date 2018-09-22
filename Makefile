
export SW_TOPDIR ?= $(PWD)

all:
	make -C serial/
	make -C applications/
#	make -C vision/libvision/
#	make -C acoustics/ppiadc/
#	make -C acoustics/bfin/

clean:
	make -C serial/ clean
	make -C applications/ clean
#	make -C vision/libvision/ clean
#	make -C acoustics/ppiadc/ clean
#	make -C acoustics/bfin/ clean

.PHONY: all clean
