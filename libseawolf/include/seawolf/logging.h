
#ifndef __SEAWOLF_LOGGING_INCLUDE_H
#define __SEAWOLF_LOGGING_INCLUDE_H

#include <stdbool.h>

#define DEBUG     0x00
#define INFO      0x01
#define NORMAL    0x02
#define WARNING   0x03
#define ERROR     0x04
#define CRITICAL  0x05

void Logging_init(void);
void Logging_close(void);
void Logging_setThreshold(short level);
void Logging_replicateStdio(bool do_replicate);
void Logging_log(short level, char* message);

#endif // #ifndef __SEAWOLF_LOGGING_INCLUDE_H
