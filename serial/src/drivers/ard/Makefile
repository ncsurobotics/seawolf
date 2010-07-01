
DRIVERS=depth.c status.c thruster12-bin.c thruster3-bin.c thruster45-bin.c thruster_board.c

DEPS=ard.c
OBJECTS=$(DRIVERS:%.c=%.o) $(DEPS:%.c=%.o)
BINS=$(DRIVERS:%.c=$(BIN_DIR)/%)

all: $(BINS)

$(BIN_DIR)/%: %.o $(DEPS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(DEPS) $<

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	@for _f in $(BINS) $(OBJECTS); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
