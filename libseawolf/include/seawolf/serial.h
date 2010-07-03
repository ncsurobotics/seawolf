/**
 * \file
 */

#ifndef __SEAWOLF_SERIAL_INCLUDE_H
#define __SEAWOLF_SERIAL_INCLUDE_H

#include <stdbool.h>

/**
 * Serial port handler
 */
typedef int SerialPort;

/* Initialization/shutdown */
void Serial_init(void);
void Serial_close(void);

/* Open/close ports */
SerialPort Serial_openVTY(void);
SerialPort Serial_open(const char* device_path);
int Serial_closePort(SerialPort sp);

/* Set options/state */
void Serial_setBlocking(SerialPort sp);
void Serial_setNonBlocking(SerialPort sp);
void Serial_setBaud(SerialPort sp, int baud);
bool Serial_isReady(SerialPort sp);
void Serial_flush(SerialPort sp);

/* IO commands */
int Serial_getByte(SerialPort sp);
int Serial_getLine(SerialPort sp, char* buffer);
int Serial_get(SerialPort sp, void* buffer, size_t count);

int Serial_sendByte(SerialPort sp, unsigned char b);
int Serial_send(SerialPort sp, void* buffer, size_t count);

void Serial_setDTR(SerialPort sp, int value);
int Serial_available(SerialPort sp);

#endif // #ifndef __SEAWOLF_SERIAL_INCLUDE_H
