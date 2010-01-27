
DRIVERS=altimeter.c imu.c imu_cont.c
OBJECTS=$(DRIVERS:%.c=%.o)
BINS=$(DRIVERS:%.c=$(BIN_DIR)/%)

all: $(BINS)
	$(MAKE) -C ard

$(BIN_DIR)/%: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

clean:
	@for _f in $(BINS) $(OBJECTS); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;
	$(MAKE) -C ard clean

.PHONY: all clean
