/**
 * \file
 * \brief Configuration file loading
 */

#include "seawolf.h"

#include <ctype.h>

/**
 * Maximum length of a line in the configuration file
 */
#define MAX_LINE 512

static char* strlower(char* s);
static bool trueValue(const char* v);

/**
 * \brief Convert a string to lower case
 *
 * Convert all the characters in a string to lower case. This is done in place
 *
 * \param s The string to lowercase
 * \return \a s
 */
static char* strlower(char* s) {
    for(int i = 0; s[i] != '\0'; i++) {
        if(isupper(s[i])) {
            s[i] = tolower(s[i]);
        }
    }
    return s;
}

/**
 * \brief Check a string for a true value
 *
 * Determines if a string should map to a true value. Strings which are
 * considered true are "true", "t", "1", "yes", and "y"
 *
 * \param v The string to check
 * \return The truth value of the string
 */
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
 * \defgroup Config Configuration
 * \ingroup Core
 * \brief Functions for loading configuration values
 *
 * Configuration options may be loaded from a file to specify values for
 * libseawolf to use. Whitespace is ignored, and lines start with a '#' are
 * comments. All other lines have the form 
 *
 * &lt;option&gt; = &lt;value&gt;
 *
 * The valid options are,
 *  - Comm_server - This options specifies the IP address of hub server (default is 127.0.0.1)
 *  - Comm_port - The port of the hub server (default is 31427)
 *  - Comm_password - The password to authenticate with the hub server (default is empty)
 *
 * \{
 */

/**
 * \brief Load a configuration file
 *
 * Load the options in the given configuration file
 *
 * \param filename File to load configuration from
 */
void Seawolf_loadConfig(const char* filename) {
    FILE* config_file = fopen(filename, "r");
    char option[64], value[MAX_LINE - 64];
    int i, tmp = 0;
    char line[MAX_LINE];
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
            while(i < MAX_LINE - 1) {
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
        if(strcmp(option, "Comm_password") == 0) {
            Comm_setPassword(value);
        } else if(strcmp(option, "Comm_server") == 0) {
            Comm_setServer(value);
        } else if(strcmp(option, "Comm_port") == 0) {
            Comm_setPort(atoi(value));
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

/** \} */
