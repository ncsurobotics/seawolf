
DRIVERS=imu.c imu_cont.c avr.c depth.c
OBJECTS=$(DRIVERS:%.c=%.o)
BINS=$(DRIVERS:%.c=../../$(BIN_DIR)/%)

all: $(BINS)

../../$(BIN_DIR)/%: %.c
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

clean:
	@for _f in $(BINS) $(OBJECTS); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
