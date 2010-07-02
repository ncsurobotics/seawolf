
#include <Wire.h>

/* 1 is for starboard/port y slave, 2 is for aft slave */
#define SLAVE 1

#define PWM1 9
#define PWM2 10

#define DIRECTION1 11
#define DIRECTION2 12

/* Thrusters */
#define PORT_X 0
#define STAR_X 1
#define PORT_Y 2
#define STAR_Y 3
#define AFT    4

#define GET_BIT(v, b) ((v) >> (b)) & 1)

unsigned byte data[2];
unsigned int thruster_id, dir, value;

void set_thrusters(int _n);

void setup(void) {
    /* Set pin modes */
    pinMode(PWM1, OUTPUT);
    pinMode(PWM2, OUTPUT);
    pinMode(DIRECTION1, OUTPUT);
    pinMode(DIRECTION2, OUTPUT);

    /* Configure PWM timers */
    TCCR1A = 0x00;      /* sets timer control bits to PWM Phase and Frequency Correct mode */
    TCCR1B = 0x12;      /* sets timer control bits to Prescaler N = 8 */
    ICR1 = 0x01F4;      /* 2Khz */

    /* Zero thrusters */
    analogWrite(PWM1, 0);
    analogWrite(PWM2, 0);
    digitalWrite(DIRECTION1, 0);
    digitalWrite(DIRECTION2, 0);
 
    /* Start I2C */
    Wire.begin(SLAVE);
    Wire.onReceive(set_thrusters);
}

void set_thrusters(int _n) {
    /* Read command bytes */
    data[0] = Wire.read();
    data[1] = Wire.read();
    
    thruster_id = data[0];
    dir = GET_BIT(data[1], 6);
    value = (data[1] & 0x3F) * 4; /* This was 8 in the old code, not sure why
                                     but keep it in mind if there are any
                                     problems */

    /* Set local thruster values or forward request over I2C */
    switch(thruster_id) {
#if SLAVE == 1
    case STAR_Y:
        analogWrite(PWM1, value);
        digitalWrite(DIRECTION1, dir);
        break;

    case PORT_Y:
        analogWrite(PWM2, value);
        digitalWrite(DIRECTION2, dir);
        break;
#endif

#if SLAVE == 2
    case AFT:
        analogWrite(PWM1, value);
        digitalWrite(DIRECTION1, dir);
        break;
#endif
    }
    
}

void loop() {
    /* Just chill */
    delay(1000);
}
