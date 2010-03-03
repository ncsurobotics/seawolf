/**
 * \file
 */

#ifndef __SEAWOLF_LOGGING_INCLUDE_H
#define __SEAWOLF_LOGGING_INCLUDE_H

#include <stdbool.h>

/**
 * \addtogroup Logging
 * \{
 */

/**
 * Debug log-level
 */
#define DEBUG     0x00

/**
 * Info log-level
 */
#define INFO      0x01

/**
 * Normal log-level
 */
#define NORMAL    0x02

/**
 * Warning log-level
 */
#define WARNING   0x03

/**
 * Error log-level
 */
#define ERROR     0x04

/**
 * Critical log-level
 */
#define CRITICAL  0x05

/** \} */

void Logging_init(void);
void Logging_close(void);
void Logging_setThreshold(short level);
void Logging_replicateStdio(bool do_replicate);
char* Logging_getLevelName(short log_level);
void Logging_log(short level, char* message);

#endif // #ifndef __SEAWOLF_LOGGING_INCLUDE_H
