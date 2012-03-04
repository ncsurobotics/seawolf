
MCU= atxmega32a4
CC= avr-gcc
CFLAGS= -mmcu=$(MCU) -std=c99 -O2

seawolf_avr.elf: main.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm seawolf_avr.elf

erase:
	avarice --pdi --dragon --erase

program: seawolf_avr.elf
	avarice --pdi --dragon --erase --program --file $<

debug: seawolf_avr.elf
	avarice --pdi --dragon --erase --program --file $< 127.0.0.1:4242

.PHONY: erase clean program
