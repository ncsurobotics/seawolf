
#include <Wire.h>

/* 0x10 is for bow/stern slave, 0x20 is for strafe slave */
#define SLAVE 0x10

#define PWM1 9
#define PWM2 10

#define DIRECTION1 11
#define DIRECTION2 12

/* Thrusters */
#define PORT   0
#define STAR   1
#define BOW    2
#define STERN  3
#define STRAFE 4

#define GET_BIT(v, b) (((v) >> (b)) & 1)

/* Optoisolation inverts the duty cycle and direction so we flip it before
   sending it out */
#define CONV_DIR(d) (1 - (d))
#define CONV_PWM(v) (0x200 - (v))

byte data[2];
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
    analogWrite(PWM1, CONV_PWM(0));
    analogWrite(PWM2, CONV_PWM(0));
    digitalWrite(DIRECTION1, CONV_DIR(0));
    digitalWrite(DIRECTION2, CONV_DIR(0));
 
    /* Start I2C */
    Wire.begin(SLAVE);
    Wire.onReceive(set_thrusters);
}

void set_thrusters(int _n) {
    /* Read command bytes */
    data[0] = Wire.receive();
    data[1] = Wire.receive();

    thruster_id = data[0];
    dir = GET_BIT(data[1], 6);
    value = (data[1] & 0x3F) * 8;

    /* Set local thruster values or forward request over I2C */
    switch(thruster_id) {
#if SLAVE == 0x10
    case BOW:
        analogWrite(PWM1, CONV_PWM(value));
        digitalWrite(DIRECTION1, CONV_DIR(dir));
        break;

    case STERN:
        analogWrite(PWM2, CONV_PWM(value));
        digitalWrite(DIRECTION2, CONV_DIR(dir));
        break;
#endif

#if SLAVE == 0x20
    case STRAFE:
        analogWrite(PWM1, CONV_PWM(value));
        digitalWrite(DIRECTION1, CONV_DIR(dir));
        break;
#endif
    }

    
}

void loop() {
    /* Just chill */
    delay(1000);
}
