
CC= bfin-linux-uclibc-gcc
CFLAGS= -O2 --std=gnu99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../../libseawolf/include -I$(PWD)/include
LDFLAGS= -L$(PWD)/../../libseawolf/ -lseawolf-bfin -lbfdsp -lm

#CC= bfin-uclinux-gcc
#CFLAGS= -static --std=gnu99 -Wall -pedantic -Wmissing-prototypes -I$(PWD)/../../libseawolf/include -I$(PWD)/include
#LDFLAGS= -L$(PWD)/../../libseawolf -lseawolf-bfin -lbfdsp -lm -Wl,-elf2flt

BIN_DIR= $(PWD)/bin
BIN_NAME= acoustics-bfin

SRCS= src/acoustics_math.c src/csv_io.c src/main.c
INCLUDES= include/acoustics_math.h include/csv_io.h

all: $(BIN_DIR)/$(BIN_NAME)

clean:
	@if [ -f $(BIN_DIR)/$(BIN_NAME) ]; then \
	  echo rm $(BIN_DIR)/$(BIN_NAME); \
	  rm $(BIN_DIR)/$(BIN_NAME); \
	fi;

bundle: $(BIN_DIR)/$(BIN_NAME)
	@if [ -d acoustics ]; then \
	  echo "The acoustics directory already exists. I need that as a temporary directory"; \
	else \
	  echo -n "Generating bundle..."; \
	  mkdir acoustics; \
	  mkdir acoustics/coefs; \
	  cp $(BIN_DIR)/$(BIN_NAME) $(PWD)/../../libseawolf/libseawolf-bfin.so acoustics/; \
	  echo "Comm_server = 10.17.0.2" > acoustics/seawolf.conf; \
	  echo "Comm_password = " >> acoustics/seawolf.conf; \
	  echo "#!/bin/sh" > acoustics/update; \
	  echo "cd .. && wget http://10.17.0.2:8080/acoustics.tar -O - | tar -xf - && cd acoustics" >> acoustics/update; \
	  chmod +x acoustics/update; \
	  for _f in $(PWD)/../fir_coef/*.fcf; do \
	    python $(PWD)/../fir_coef/convert.py < $$_f > acoustics/coefs/`basename $$_f .fcf`.cof; \
	  done; \
	  tar -cf acoustics_bundle.tar acoustics; \
	  rm -rf acoustics; \
	  echo "done."; \
	fi;

bundle_push:
	scp acoustics_bundle.tar seawolf@10.17.0.2:acoustics_bundle/acoustics.tar

$(BIN_DIR)/$(BIN_NAME): $(BIN_DIR) $(SRCS) $(INCLUDES)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/$(BIN_NAME) $(SRCS) $(LDFLAGS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

.PHONY: all clean bundle bundle_push
