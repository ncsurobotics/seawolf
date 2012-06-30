
#include <sw.h>

void init_solenoids(void) {
    /* Enable output pins */
    PORTA.DIRSET = 0xe0;
}

void set_solenoid(Solenoid solenoid, bool value) {
    int value_bit = 0;

    switch(solenoid) {
    case SOLENOID0:
        value_bit = 1 << 5;
        break;

    case SOLENOID1:
        value_bit = 1 << 6;
        break;

    case SOLENOID2:
        value_bit = 1 << 7;
        break;
    }

    if(value) {
        PORTA.OUTSET = value_bit;
    } else {
        PORTA.OUTCLR = value_bit;
    }
}
