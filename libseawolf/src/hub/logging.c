
#include "seawolf.h"
#include "seawolf_hub.h"

#include <pthread.h>

static bool initialized = false;
static FILE* log_file = NULL;

void Hub_Logging_init(void) {
    const char* path = Hub_Config_getOption("log_file");

    if(path) {
        log_file = fopen(path, "a");
        if(log_file == NULL) {
            Hub_Logging_log(ERROR, Util_format("Could not open log file: %s", strerror(errno)));
            log_file = stdout;
        }
    } else {
        Hub_Logging_log(INFO, "No log file specified. Using standard output");
        log_file = stdout;
    }

    initialized = true;
}

void Hub_Logging_log(short log_level, char* msg) {
    if(!initialized) {
        printf("[Hub][%s] %s\n", Logging_getLevelName(log_level), msg);
    } else {
        Hub_Logging_logWithName("Hub", log_level, msg);
    }
}

void Hub_Logging_logWithName(char* app_name, short log_level, char* msg) {
    printf("[%s][%s] %s\n", app_name, Logging_getLevelName(log_level), msg);
}

void Hub_Logging_close(void) {
    if(log_file) {
        fflush(log_file);
        fclose(log_file);
    }
}
