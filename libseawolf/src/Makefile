
LIB_LDFLAGS= -lmysqlclient_r -lpthread --shared -fPIC
HUB_LDFLAGS=

INCLUDES=../include/seawolf/* ../include/seawolf.h

LIB_SRC= ardcomm.c logging.c main.c notify.c pid.c \
	seasql.c seasql_config.c seawolf_config.c \
	serial.c stack.c task.c timer.c util.c
LIB_OBJECTS= $(LIB_SRC:.c=.o)

HUB_SRC= hub/hub.c
HUB_OBJECTS= hub/hub.o

all: $(LIB_NAME) $(HUB_NAME)

$(LIB_NAME): $(LIB_OBJECTS) 
	$(CC) $(LIB_LDFLAGS) $(LIB_OBJECTS) -o $(LIB_NAME)

$(HUB_NAME): $(HUB_OBJECTS)
	$(CC) $(HUB_LDFLAGS) $(HUB_OBJECTS) -o $(HUB_NAME)

%.o: %.c $(INCLUDES) 
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@for _f in $(HUB_OBJECTS) $(LIB_OBJECTS) $(LIB_NAME) $(HUB_NAME); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
