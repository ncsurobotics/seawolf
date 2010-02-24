
HUB_LDFLAGS= -L$(LIB_PATH) -lsqlite3 -lseawolf

INCLUDES= ../../include/seawolf/* ../../include/seawolf.h seawolf_hub.h

HUB_SRC= config.c db.c hub.c logging.c netloop.c process.c var.c
HUB_OBJECTS= $(HUB_SRC:.c=.o)

all: $(HUB_NAME)

$(HUB_NAME): $(HUB_OBJECTS)
	$(CC) $(HUB_LDFLAGS) $(HUB_OBJECTS) -o $(HUB_NAME)

%.o: %.c $(INCLUDES)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@for _f in $(HUB_OBJECTS) $(HUB_NAME); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
