
#ifndef __SEAWOLF_MICRO_AVR_H
#define __SEAWOLF_MICRO_AVR_H

/* CPU speed defined before inclusion of util/delay.h so the delay routines
   are with respect to the the actual clock rate */
#define F_CPU 2000000UL

#include <stdbool.h>

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>
#include <util/delay.h>

enum Commands {
    SW_RESET    = 0x72,  /* 'r' full reset */
    SW_NOP      = 0x00,
    SW_MOTOR    = 0x01,
    SW_SERVO    = 0x02,
    SW_STATUS   = 0x03,
    SW_DEPTH    = 0x04,
    SW_TEMP     = 0x05
};

typedef enum {
    SERVO1 = 0,
    SERVO2 = 1
} Servo;

typedef enum {
    BOW    = 0,
    STERN  = 1,
    STRAFE = 2,
    PORT   = 3,
    STAR   = 4
} Motor;

void init_servos(void);
void set_servo_position(Servo servo, unsigned int value);

void init_motors(void);
void set_motor_speed(Motor motor, int speed);

void init_serial(void);
void serial_send_byte(char c);
void serial_send_bytes(char* s, int n);
void serial_print(char* s);
int serial_available(void);
int serial_read_byte(void);
void serial_read_bytes(char* s, int n);

void init_analog(void);

#endif // #ifndef __SEAWOLF_MICRO_AVR_H
