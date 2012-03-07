
#include <sw.h>

void init_motors(void) {
    /* Set PD0 -> PD4 as output (these are the motor PWM outputs) */
    PORTD.DIRSET = 0x1f;

    /* Set PC1 -> PC5 as output (these are the motor direction outputs) */
    PORTC.DIRSET = 0x37;

    /* Clock divider of 1 (from 2MHz) */
    TCD0.CTRLA = 0x01;
    TCD1.CTRLA = 0x01;

    /* Enable all output compare OC0x pins and set waveform generation mode to
       single slope PWM */
    TCD0.CTRLB = 0xf3;
    TCD1.CTRLB = 0x13;

    /* Set period to 64 which at 2MHz gives an output clock of approximately
       31.25 KHz */
    TCD0.PER = 0x0040;
    TCD1.PER = 0x0040;

    /* Set duty cycle to 0 */
    TCD0.CCA = 0x0000;
    TCD0.CCB = 0x0000;
    TCD0.CCC = 0x0000;
    TCD0.CCD = 0x0000;
    TCD1.CCA = 0x0000;
}

/* Set speed of motor. Value is -64 to 64 */
void set_motor_speed(Motor motor, int speed) {
    unsigned int duty_cycle = speed < 0 ? -speed : speed;
    unsigned int dir_bit;

    switch(motor) {
    case MOTOR1:
        TCD0.CCA = duty_cycle;
        dir_bit = 1 << 1;
        break;

    case MOTOR2:
        TCD0.CCB = duty_cycle;
        dir_bit = 1 << 2;
        break;

    case MOTOR3:
        TCD0.CCC = duty_cycle;
        dir_bit = 1 << 3;
        break;

    case MOTOR4:
        TCD0.CCD = duty_cycle;
        dir_bit = 1 << 4;
        break;

    case MOTOR5:
        TCD1.CCA = duty_cycle;
        dir_bit = 1 << 5;
        break;
    }

    if(speed < 0) {
        PORTC.OUTCLR = dir_bit;
    } else {
        PORTC.OUTSET = dir_bit;
    }
}
