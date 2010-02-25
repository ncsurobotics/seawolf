
#include "seawolf.h"

#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/* Minimum log level and replicate to stdio */
static bool initialized = false;
static short min_log_level = DEBUG;
static bool log_stdio = true;

/* Log string names */
static char* level_names[] = {"DEBUG",
                              "INFO",
                              "NORMAL",
                              "WARNING",
                              "ERROR",
                              "CRITICAL"};

/**
 * Initialize logging 
 */
void Logging_init(void) {
    /* Logging can be used before a connection to the comm server, but only
       locally */
    initialized = true;
}

/**
 * Deinitialize logging
 */
void Logging_close(void) {
    if(!initialized) {
        return;
    }

    /* nothing to do */
}

/**
 * Set the threshold for logging to the given level
 */
void Logging_setThreshold(short level) {
    min_log_level = level;
}

/**
 * Replicate logging to standard output
 */
void Logging_replicateStdio(bool do_replicate) {
    log_stdio = do_replicate;
}

/**
 * Return the string representation of a log level
 */
char* Logging_getLevelName(short log_level) {
    return level_names[log_level];
}

/**
 * Log message
 */
void Logging_log(short log_level, char* msg) {
    static char* namespace = "LOG";

    /* Only log messages with a log level at least as high as min_debug_leve */
    if(log_level >= min_log_level) {
        if(initialized) {
            Comm_Message* log_message = Comm_Message_new(4);

            log_message->components[0] = namespace;
            log_message->components[1] = Seawolf_getName();
            log_message->components[2] = strdup(__Util_format("%d", log_level));
            log_message->components[3] = msg;

            Comm_sendMessage(log_message);
            free(log_message->components[2]);
            Comm_Message_destroy(log_message);
        }

        /* Replicate the message to standard output */
        if(log_stdio || !initialized) {
            printf("[%s][%s] %s\n", Seawolf_getName(), level_names[log_level], msg);
        }
    }
}
