
SERIALAPP=../$(BIN_DIR)/serialapp

all: $(SERIALAPP)
	$(MAKE) -C drivers

$(SERIALAPP): serialapp.c
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

clean:
	@for _f in $(SERIALAPP); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;
	$(MAKE) -C drivers clean

.PHONY: all clean
