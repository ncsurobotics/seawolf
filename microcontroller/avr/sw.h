
#ifndef __SEAWOLF_MICRO_AVR_H
#define __SEAWOLF_MICRO_AVR_H

/* CPU speed defined before inclusion of util/delay.h so the delay routines
   are with respect to the the actual clock rate */
#define F_CPU 32000000UL

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
    SW_TEMP     = 0x05,
    SW_SOLENOID = 0x06,
    SW_BATTERY  = 0x07,
    SW_KILL     = 0x08,
    SW_REALIGN  = 0x09,
    SW_ERROR    = 0xaa,
    SW_MARKER   = 0xbb
};

typedef enum {
    SERVO1 = 0,
    SERVO2 = 1
} Servo;

typedef enum {
    SOLENOID0 = 0,
    SOLENOID1 = 1,
    SOLENOID2 = 2
} Solenoid;

typedef enum {
    BOW    = 0,
    STERN  = 1,
    STRAFE = 2,
    PORT   = 3,
    STAR   = 4
} Motor;

typedef enum {
    SLA1 = 0,
    SLA2 = 1,
    LIPO = 2
} Battery;

typedef enum {
    KILLED = 0,
    NOT_KILLED = 1
} KillStatus;

typedef enum {
    INVALID_REQUEST = 0,
    SERIAL_ERROR = 1,
    TWI_ERROR = 2,
    SYNC_ERROR = 3
} Error;

void init_servos(void);
void set_servo_position(Servo servo, unsigned int value);

void init_solenoids(void);
void set_solenoid(Solenoid solenoid, bool value);

void init_motors(void);
void set_motor_speed(Motor motor, int speed);

void init_serial(void);
void realign_buffer(void);
void serial_send_byte(char c);
void serial_send_bytes(char* s, int n);
void serial_print(char* s);
int serial_available(void);
int serial_read_byte(void);
void serial_read_bytes(char* s, int n);

void init_analog(void);
void start_depth_reading(void);

void init_status(void);
void update_status(int counter);
void set_status(int value);

void init_scheduler(void);

void check_kill(void);
void check_batteries(void);

#endif // #ifndef __SEAWOLF_MICRO_AVR_H
