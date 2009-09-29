
#include "seawolf.h"

#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

/* This is the SeaSQL configuration. These values can be changed with an
   appropriate call to on of the SeaSQL_config* functions */
static SeaSQL_config seasql_config = { "localhost",  /* System MySQL is running on */
                                       "root",       /* MySQL user */
                                       "",           /* Password corresponding with the username */
                                       "seasql",     /* Default database name */
                                       3306 };       /* Default MySQL port, should not change */

/**
 * Read a line from standard input 
 */
static void readline(char* s) {
    while((*s = getchar()) != '\n') s++;
    *s = '\0';
}

/**
 * Load a configuration stored in a file
 */
void SeaSQL_configFile(char* filename) {
    FILE* config_file = fopen(filename, "r");
    char option[64], value[64];
    int i, tmp = 0;
    char line[256];
    bool comment;

    /* Configuration file opened alright? */
    if(config_file == NULL) {
        fprintf(stderr, "Error opening configuration file: %s\n", filename);
        return;
    }
    
    /* Read in line by line until EOF to get each configuration option */
    while(true) {
        line[0] = '\0';

        /* Read until we find a non empty line */
        while(strcmp(line, "") == 0) {
            i = 0;
            comment = false;

            /* Read line */
            while(i < 255) {
                tmp = fgetc(config_file);

                /* End of input/line */
                if(tmp == EOF || tmp == '\n') {
                    break;
                }

                /* Start of a comment */
                if(tmp == '#') {
                    comment = true;
                }

                /* We are in a comment so discard characters */
                if(! comment) {
                    line[i++] = tmp;
                }
            }
            line[i] = '\0';

            /* Strip white space from entire line */
            Util_strip(line);

            /* If the line is empty and we have reached the end of file then
               return */
            if(tmp == EOF && strcmp(line, "") == 0) {
                return;
            }
        }
        
        /* Split the line */
        if(Util_split(line, '=', option, value) == 1) {
            /* Didn't find '=' */
            fprintf(stderr, "Error parsing config file at '%s'\n", line);
            continue;
        }
        
        /* Strip spaces from components */
        Util_strip(option);
        Util_strip(value);

        /* Check against configuration option */
        if(strcmp(option, "hostname") == 0) {
            strcpy(seasql_config.hostname, value);
        } else if(strcmp(option, "username") == 0) {
            strcpy(seasql_config.username, value);
        } else if(strcmp(option, "password") == 0) {
            strcpy(seasql_config.password, value);
        } else if(strcmp(option, "database") == 0) {
            strcpy(seasql_config.database, value);
        } else if(strcmp(option, "port") == 0) {
            seasql_config.port = atoi(value);
        } else {
            fprintf(stderr, "Unknown configuration option '%s'\n", option);
        }
    }
}

/**
 * Loads a SeaSQL configuration by prompting for values on standard input
 */
void SeaSQL_configPrompt(void) {
    char value[64];
    
    printf("Hostname (probably 'localhost')? ");
    readline(value);
    strcpy(seasql_config.hostname, value);

    printf("Port (probably 3306)? ");
    readline(value);
    seasql_config.port = atoi(value);

    printf("Username? ");
    readline(value);
    strcpy(seasql_config.username, value);

    printf("Password? ");
    readline(value);
    strcpy(seasql_config.password, value);

    printf("Database? ");
    readline(value);
    strcpy(seasql_config.database, value);
}

/**
 * Retreive the SeaSQL configuration structure
 */
SeaSQL_config* SeaSQL_getConfig(void) {
    return &seasql_config;
}
