
SRCS=$(wildcard *.c)
OUTPUT=$(SRCS:%.c=$(BIN_DIR)/%)

all: $(OUTPUT)

$(BIN_DIR)/%: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

clean:
	@for _f in $(OUTPUT); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
