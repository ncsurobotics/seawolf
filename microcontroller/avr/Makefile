
MCU= atxmega32a4
CC= avr-gcc
CFLAGS= -mmcu=$(MCU) -Wall -g -std=c99 -O2 -I.

OUTPUT= seawolf_avr
HEX_OUTPUT= $(OUTPUT).hex
SOURCES= ./main.c ./servo.c ./motor.c ./uart.c ./analog.c ./solenoid.c ./status.c ./scheduler.c
OBJS= $(SOURCES:%.c=%.o)

$(HEX_OUTPUT): $(OUTPUT)
	avr-objcopy -O ihex $< $@

$(OUTPUT): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

%.o: %.c sw.h
	$(CC) $(CFLAGS) -c $<

clean:
	rm $(OUTPUT) $(HEX_OUTPUT) $(OBJS)

erase:
	avrdude -p x32a4 -c avrispmkII -P usb -e

program: $(HEX_OUTPUT)
	avrdude -p x32a4 -c avrispmkII -P usb -U $(HEX_OUTPUT)

debug: program
	avarice --pdi --dragon 127.0.0.1:4242

.PHONY: erase clean program
