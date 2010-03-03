/**
 * \file
 * \brief Core functions
 */

#include "seawolf.h"

#include <signal.h>

static char app_name[256];
static void Seawolf_catchSignal(int sig);

/**
 * \mainpage
 *
 * \section intro Introduction
 *
 * See the "Modules" tab for API documentation. Architecture and general use
 * documentation should be available soon.
 */

/**
 * \defgroup Core Core Routines
 * \defgroup Communications Communications
 * \defgroup DataStructures Data Structures
 * \defgroup Hardware Hardware Access
 * \defgroup Utilities Utilities
 */

/**
 * \defgroup Main Core libseawolf
 * \ingroup Core
 * \brief Core routines for libseawolf initialization and management
 * \{
 */

/**
 * \brief Initialize the library
 *
 * Perform all initialization to ready the library for use. Care must be taken
 * when making any calls before this is called
 *
 * \param name Name of the program. This is used in debugging and logging
 */
void Seawolf_init(const char* name) {
    /* Copy name */
    strcpy(app_name, name);


    /* Catch siginals and insure proper shutdown */
    signal(SIGINT, Seawolf_catchSignal);
    signal(SIGHUP, Seawolf_catchSignal);
    signal(SIGTERM, Seawolf_catchSignal);

    /* Ensure shutdown during normal exit */
    atexit(Seawolf_close);

    /* Call all initialization methods. Order here *is* important. Logging
       relies on the database being up for instance */
    Comm_init();
    Logging_init();
    Notify_init();
    Var_init();
    Serial_init();

    /* Log message announcing application launch */
    Logging_log(INFO, "Initialized");
}

/**
 * Catches signals and shuts down libseawolf properly before exiting
 */
static void Seawolf_catchSignal(int sig) {
    /* Caught signal, exit and properly shut down */
    Logging_log(CRITICAL, "Signal caught! Shutting down...");
    Seawolf_exitError();
}

/**
 * \brief Close the library
 *
 * Close the library and free any resources claimed by it
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
    Var_close();
    Logging_close();
    Comm_close();
    Notify_close();
    Util_close();
}

/**
 * \brief Terminate application due to error
 *
 * Terminate application because of an error condition
 */
void Seawolf_exitError(void) {
    Logging_log(INFO, "Terminating application due to error condition");
    exit(1);
}

/**
 * \brief Get the application name
 *
 * Return the name registered with the library with a call to Seawolf_init()
 *
 * \return The registered application name
 */
char* Seawolf_getName(void) {
    return app_name;
}

/** \} */
