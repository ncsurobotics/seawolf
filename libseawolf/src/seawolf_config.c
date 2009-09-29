
#include "seawolf.h"

#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LINE 512

static char* strlower(char* s) {
    for(int i = 0; s[i] != '\0'; i++) {
        if(isupper(s[i])) {
            s[i] = tolower(s[i]);
        }
    }
    return s;
}

static bool trueValue(const char* v) {
    char* copy = strlower(strdup(v));
    bool r = false;

    /* Check values */
    if(strcmp(copy, "true") == 0 || strcmp(copy, "t") == 0 ||
       strcmp(copy, "1") == 0 || strcmp(copy, "yes") == 0 ||
       strcmp(copy, "y") == 0) {
        r = true;
    }

    free(copy);
    return r;
}

/**
 * Load a configuration stored in a file
 */
void Seawolf_loadConfig(const char* filename) {
    FILE* config_file = fopen(filename, "r");
    char option[64], value[MAX_LINE - 64];
    int i, tmp = 0;
    char line[MAX_LINE];
    bool comment;

    /* Get a pointer to the configuration so we can update it */
    SeaSQL_config* seasql_config = SeaSQL_getConfig();

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
                fclose(config_file);
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
        if(strcmp(option, "SeaSQL_hostname") == 0) {
            strcpy(seasql_config->hostname, value);
        } else if(strcmp(option, "SeaSQL_username") == 0) {
            strcpy(seasql_config->username, value);
        } else if(strcmp(option, "SeaSQL_password") == 0) {
            strcpy(seasql_config->password, value);
        } else if(strcmp(option, "SeaSQL_database") == 0) {
            strcpy(seasql_config->database, value);
        } else if(strcmp(option, "SeaSQL_port") == 0) {
            seasql_config->port = atoi(value);
        } else if(strcmp(option, "Notify_method") == 0) {
            strlower(value);
            if(strcmp(value, "stdio") == 0) {
                Notify_setMode(NOTIFY_STDIO);
            } else if(strcmp(value, "net") == 0) {
                Notify_setMode(NOTIFY_NET);
            } else {
                fprintf(stderr, "Invalid value to option Notify_method\n");
            }
        } else if(strcmp(option, "Notify_server") == 0) {
            Notify_setServer(value);
        } else if(strcmp(option, "Logging_replicateStdio") == 0) {
            if(trueValue(value)) {
                Logging_replicateStdio(true);
            } else {
                Logging_replicateStdio(false);
            }
        } else if(strcmp(option, "Logging_threshold") == 0) {
            strlower(value);
            if(strcmp(value, "debug") == 0) {
                Logging_setThreshold(DEBUG);
            } else if(strcmp(value, "info") == 0) {
                Logging_setThreshold(INFO);
            } else if(strcmp(value, "normal") == 0) {
                Logging_setThreshold(NORMAL);
            } else if(strcmp(value, "warning") == 0) {
                Logging_setThreshold(WARNING);
            } else if(strcmp(value, "error") == 0) {
                Logging_setThreshold(ERROR);
            } else if(strcmp(value, "critical") == 0) {
                Logging_setThreshold(CRITICAL);
            } else {
                fprintf(stderr, "Invalid logging threshold value '%s'\n", value);
            }
        } else {
            fprintf(stderr, "Unknown configuration option '%s'\n", option);
        }
    }
}
