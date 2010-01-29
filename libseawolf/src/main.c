
#include "seawolf.h"

#include <signal.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

static char app_name[256];
static void Seawolf_catchSignal(int sig);

/**
 * Initialize Seawolf and all its components and register the given name with
 * this initialize
 */
void Seawolf_init(const char* name) {
    /* Copy name */
    strcpy(app_name, name);

    /* Call all initialization methods. Order here *is* important. Logging
       relies on the database being up for instance */
    Notify_init();
    SeaSQL_init();
    Logging_init();
    Serial_init();

    /* Catch siginals and insure proper shutdown */
    signal(SIGINT, Seawolf_catchSignal);
    signal(SIGHUP, Seawolf_catchSignal);
    signal(SIGTERM, Seawolf_catchSignal);

    /* Ensure shutdown during normal exit */
    atexit(Seawolf_close);

    /* Log message announcing application launch */
    Logging_log(INFO, "Initialized");
}

/**
 * Catches signals and shuts down libseawolf properly before exiting
 */
static void Seawolf_catchSignal(int sig) {
    /* Caught signal, exit and properly shut down */
    printf("\nSignal caught! Shutting down...\n");
    Seawolf_close();
    exit(0);
}

/**
 * Close libseawolf
 */
void Seawolf_close(void) {
    static bool closed = false;

    /* Only close once */
    if(closed) {
        return;
    }
    closed = true;

    /* Announce closing */
    Logging_log(INFO, "Closing");
    
    Serial_close();
    Logging_close();
    SeaSQL_close();
    Notify_close();
    Util_close();
}

/**
 * Return the name associated with the initialization of this component
 */
char* Seawolf_getName(void) {
    return app_name;
}
