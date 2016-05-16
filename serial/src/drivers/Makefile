
DRIVERS=imu.c imu_cont.c avr.c depth.c peripheral.c
OBJECTS=$(DRIVERS:%.c=%.o)
BINS=$(DRIVERS:%.c=../../$(BIN_DIR)/%)

SRCS_PY=$(wildcard *.py)
OUTPUT_PY=$(SRCS_PY:%.py=../../$(BIN_DIR)/%)

all: $(BINS) $(OUTPUT_PY)

../../$(BIN_DIR)/%: %.c
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

../../$(BIN_DIR)/%: %.py
	@echo "Copying" $< "to build dir"
	@echo "#!$(PYTHON_BIN)" > $@
	@cat $< > $@
	@chmod +x $@

clean:
	@for _f in $(BINS) $(OBJECTS); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
