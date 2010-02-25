
#include "seawolf.h"
#include "seawolf_hub.h"

#include <pthread.h>
#include <unistd.h>
#include <fcntl.h>

static bool initialized = false;
static FILE* log_file = NULL;
static int log_file_fd = STDOUT_FILENO;

void Hub_Logging_init(void) {
    char* path = Hub_Config_getOption("log_file");

    if(path) {
        log_file_fd = open(path, O_RDWR|O_SYNC|O_CREAT|O_APPEND, 0);
        if(log_file_fd == -1) {
            Hub_Logging_log(ERROR, __Util_format("Could not open log file: %s", strerror(errno)));
            log_file_fd = STDOUT_FILENO;
        }
        free(path);
    } else {
        Hub_Logging_log(INFO, "No log file specified. Using standard output");
    }

    log_file = fdopen(log_file_fd, "a");
    if(log_file == NULL) {
        Hub_Logging_log(ERROR, __Util_format("Unable to associated log file descriptor with file handle: %s", strerror(errno)));
    }

    initialized = true;
}

void Hub_Logging_log(short log_level, char* msg) {
    Hub_Logging_logWithName("Hub", log_level, msg);
}

void Hub_Logging_logWithName(char* app_name, short log_level, char* msg) {
    if(!initialized) {
        printf("[%s][%s] %s\n", app_name, Logging_getLevelName(log_level), msg);
    } else {
        fprintf(log_file, "[%s][%s] %s\n", app_name, Logging_getLevelName(log_level), msg);
        fflush(log_file);
    }
}

void Hub_Logging_close(void) {
    if(log_file) {
        fflush(log_file);
        fclose(log_file);
        close(log_file_fd);
    }
}
