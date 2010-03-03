
#include "seawolf.h"
#include "seawolf_hub.h"

#include <unistd.h>
#include <fcntl.h>
#include <time.h>

#define TIME_BUFFER_SIZE 64

static bool initialized = false;
static FILE* log_file = NULL;
static int log_file_fd = STDOUT_FILENO;
static char time_buffer[TIME_BUFFER_SIZE];
static short min_log_level = NORMAL;
static bool replicate_stdout = false;

void Hub_Logging_init(void) {
    char* path = Hub_Config_getOption("log_file");

    if(path) {
        log_file_fd = open(path, O_RDWR|O_SYNC|O_CREAT|O_APPEND, S_IRUSR|S_IWUSR);
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

    min_log_level = Hub_Var_get("LogLevel");
    if(min_log_level == -1) {
        min_log_level = NORMAL;
    }

    replicate_stdout = (Hub_Var_get("LogReplicateStdout") == 1);

    initialized = true;
}

void Hub_Logging_log(short log_level, char* msg) {
    if(log_level >= min_log_level) {
        Hub_Logging_logWithName("Hub", log_level, msg);
    }
}

void Hub_Logging_logWithName(char* app_name, short log_level, char* msg) {
    time_t t;

    if(!initialized || replicate_stdout) {
        printf("[%s][%s] %s\n", app_name, Logging_getLevelName(log_level), msg);
    }

    if(initialized) {
        time(&t);
        strftime(time_buffer, TIME_BUFFER_SIZE, "%H:%M:%S", localtime(&t));

        fprintf(log_file, "[%s][%s][%s] %s\n", time_buffer, app_name, Logging_getLevelName(log_level), msg);
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
