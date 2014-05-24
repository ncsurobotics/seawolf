
#include <sw.h>

void init_motors(void) {
    /* Set PD0 -> PD5 as output (these are the motor PWM outputs) */
    PORTD.DIRSET = 0x3f;

    /* Set PC0 -> PC5 as output (these are the motor direction outputs) */
    PORTC.DIRSET = 0x3f;

    /* Clock divider of 8 (from 2MHz) */
    TCD0.CTRLA = TC_CLKSEL_DIV8_gc;
    TCD1.CTRLA = TC_CLKSEL_DIV8_gc;

    /* Enable all output compare OC0x pins and set waveform generation mode to
       single slope PWM */
    TCD0.CTRLB = 0xf3;
    TCD1.CTRLB = 0x33;

    /* Set period to 128 which at 2MHz/8 gives an output clock of approximately
       2 KHz */
    TCD0.PER = 0x0080;
    TCD1.PER = 0x0080;

    /* Set duty cycle to 0 */
    TCD0.CCA = 0x0000;
    TCD0.CCB = 0x0000;
    TCD0.CCC = 0x0000;
    TCD0.CCD = 0x0000;
    TCD1.CCA = 0x0000;
    TCD1.CCB = 0x0000;
}

/* Set speed of motor. Value is -128 to 128 */
void set_motor_speed(Motor motor, int speed) {
    unsigned int duty_cycle = speed < 0 ? -speed : speed;
    unsigned int dir_bit;

    switch(motor) {
    case BOW:
        TCD0.CCA = duty_cycle;
        dir_bit = 1 << 1;
        break;

    case STERN:
        TCD0.CCB = duty_cycle;
        dir_bit = 1 << 2;
        break;

    case PORT:
        TCD0.CCC = duty_cycle;
        dir_bit = 1 << 3;
        break;

    case STAR:
        TCD0.CCD = duty_cycle;
        dir_bit = 1 << 4;
        break;
    
    case STRAFET:
        TCD1.CCA = duty_cycle;
        dir_bit = 1 << 5;
        break;

    case STRAFEB:
        TCD1.CCB = duty_cycle;
        dir_bit = 1 << 0;
        break;

            
    default:
        return;
    }

    if(speed < 0) {
        PORTC.OUTCLR = dir_bit;
    } else {
        PORTC.OUTSET = dir_bit;
    }
}
