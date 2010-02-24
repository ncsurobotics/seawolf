
#include "seawolf.h"

#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include <mysql/mysql.h>

/* SQL expressions */
#define LOG_MYSQL_CREATE "CREATE TABLE IF NOT EXISTS log (id INT AUTO_INCREMENT UNIQUE PRIMARY KEY, time DATETIME, app VARCHAR(64), level CHAR(15), message VARCHAR(255));"
#define LOG_MYSQL_INSERT "INSERT INTO log VALUES(0, NOW(), '%s', '%s', '%s');"

/* Minimum log level and replicate to stdio */
static short min_log_level = NORMAL;
static bool log_stdio = true;
static bool connected = false;

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
    connected = true;
}

/**
 * Deinitialize logging
 */
void Logging_close(void) {
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
char* Logging_levelName(short log_level) {
    return level_names[log_level];
}

/**
 * Log message
 */
void Logging_log(short log_level, char* msg) {
    static char* namespace = "LOGGING";

    /* Only log messages with a log level at least as high as min_debug_leve */
    if(log_level >= min_log_level) {
        if(connected) {
            Comm_Message* log_message = Comm_Message_new();
            log_message->components = malloc(sizeof(char*) * 4);

            log_message->count = 4;
            log_message->components[0] = namespace;
            log_message->components[1] = Seawolf_getName();
            log_message->components[2] = strdup(Util_format("%d", log_level));
            log_message->components[3] = msg;

            Comm_sendMessage(log_message);

            free(log_message->components[2]);
            Comm_Message_destroy(log_message);
        }

        /* Replicate the message to standard output */
        if(log_stdio || !connected) {
            printf("[%s][%s] %s\n", Seawolf_getName(), level_names[log_level], msg);
        }
    }
}
