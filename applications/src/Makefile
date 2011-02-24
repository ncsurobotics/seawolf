
SRCS=$(wildcard *.c)
SRCS_PY=$(wildcard *.py)
OUTPUT=$(SRCS:%.c=$(BIN_DIR)/%)
OUTPUT_PY=$(SRCS_PY:%.py=$(BIN_DIR)/%)

all: $(OUTPUT) $(OUTPUT_PY)

$(BIN_DIR)/%: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) $(shell cat $(<:%.c=%.flags) 2>/dev/null) -o $@ $<

$(BIN_DIR)/%: %.py
	@echo "Copying" $< "to build dir"
	@echo "#!$(PYTHON_BIN)" > $@
	@cat $< >> $@
	@chmod +x $@

clean:
	@for _f in $(OUTPUT) $(OUTPUT_PY); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
