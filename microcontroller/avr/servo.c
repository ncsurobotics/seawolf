
#include <sw.h>

ISR(TCE0_CCA_vect) {
    /* Clear PA3 (SER1) */
    PORTA.OUTCLR = 0x08;
}

ISR(TCE0_CCB_vect) {
    /* Clear PA4 (SER2) */
    PORTA.OUTCLR = 0x10;
}

ISR(TCE0_OVF_vect) {
    /* Turn on both servo outputs */
    PORTA.OUTSET = 0x18;
}

/* Initialize servo control. Since the servo outputs are not on compare output
   pins we use the unused timer on port E and interrupt routines to toggle the
   port A pins the lines are actually on. In rev 2 boards these pins will be
   moved to proper timer output pins on port E */
void init_servos(void) {
    /* Enable output pins */
    PORTA.DIRSET = 0x18;

    /* Set clock divider of 64 from input of 32MHz for a timer input clock of
       500Khz */
    TCE0.CTRLA = TC_CLKSEL_DIV64_gc;

    /* Set single slope PWM mode */
    TCE0.CTRLB = 0x03;

    /* Period of 1000 for PWM output clock of 500 Hz */
    TCE0.PER = 1000;

    /* Enable interrupts to toggle pins */
    TCE0.INTCTRLA = 0x01;
    TCE0.INTCTRLB = 0x05;

    /* Set initial duty cycle of 50% on both compare registers */
    TCE0.CCA = 500;
    TCE0.CCB = 500;
}

/* Set servo position between 0 and 1000 */
void set_servo_position(Servo servo, unsigned int value) {
    switch(servo) {
    case SERVO1:
        TCE0.CCA = value;
        break;

    case SERVO2:
        TCE0.CCB = value;
        break;
    }
}
