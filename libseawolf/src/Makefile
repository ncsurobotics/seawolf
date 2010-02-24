
LIB_LDFLAGS= -lrt -lpthread --shared -fPIC

INCLUDES=../include/seawolf/* ../include/seawolf.h

LIB_SRC= ardcomm.c logging.c main.c notify.c pid.c \
	var.c seawolf_config.c serial.c stack.c \
	task.c timer.c util.c dictionary.c list.c \
	queue.c comm.c
LIB_OBJECTS= $(LIB_SRC:.c=.o)

all: $(LIB_NAME) $(HUB_NAME)

$(LIB_NAME): $(LIB_OBJECTS) 
	$(CC) $(LIB_LDFLAGS) $(LIB_OBJECTS) -o $(LIB_NAME)

$(HUB_NAME): $(INCLUDES) hub/*.c hub/*.h
	$(MAKE) -C hub

%.o: %.c $(INCLUDES) 
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@for _f in $(LIB_OBJECTS) $(LIB_NAME); do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;
	$(MAKE) -C hub clean

.PHONY: all clean
