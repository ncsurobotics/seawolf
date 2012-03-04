
#define F_CPU 2000000UL

#include <stdbool.h>

#include <avr/io.h>
#include <avr/wdt.h>
#include <util/delay.h>

void long_delay(float seconds) {
    unsigned int n = seconds * (1000 / 50);

    for(unsigned int i = 0; i < n; i++) {
        _delay_ms(50);
    }
}

int main(void) {
    /* Watchdog disabled by default (per fuse settings) */

    /* Lock clock. Default clock rate of 2Mhz */
    CLK.LOCK = 1;

    /* Set output pins */
    PORTA.DIR = 0xe0;

    while(true) {
        PORTA.OUTTGL = 0xE0;
        long_delay(1);
    }
}
