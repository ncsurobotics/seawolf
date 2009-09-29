
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
static bool log_stdio = false;

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
    /* Create logging table if not existing */
    SeaSQL_execute(LOG_MYSQL_CREATE);
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
 * Log message
 */
void Logging_log(short log_level, char* msg) {
    /* Only log messages with a log level at least as high as min_debug_leve */
    if(log_level >= min_log_level) {
        char* escaped_str = malloc(strlen(msg)*2 + 1);

        /* Escape string and build total buffer size */
        int message_length = mysql_escape_string(escaped_str, msg, strlen(msg));
        int total_length = strlen(LOG_MYSQL_INSERT) + strlen(Seawolf_getName()) + strlen(level_names[log_level]) + message_length + 500;

        /* Command space */
        char* command = malloc(sizeof(char) * total_length);
        
        /* Clear memory and format SQL command */
        memset(command, 0, total_length);
        snprintf(command, total_length, LOG_MYSQL_INSERT, Seawolf_getName(), level_names[log_level], escaped_str);

        /* Execute */
        SeaSQL_execute(command);

        /* Replicate the message to standard output */
        if(log_stdio) {
            printf("[%s][%s] %s\n", Seawolf_getName(), level_names[log_level], msg);
        }

        /* Free allocated memory */
        free(command);
        free(escaped_str);
    }
}
