
/* Seawolf libraries */
#include "seawolf.h"
#include "seawolf_hub.h"

/* Signal handling */
#include <signal.h>

static void Hub_catchSignal(int sig);

void Hub_exitError(void) {
    Hub_Logging_log(INFO, "Terminating hub due to error condition");
    exit(1);
}

static void Hub_catchSignal(int sig) {
    /* Caught signal, exit and properly shut down */
    Hub_Logging_log(CRITICAL, "Signal caught! Shutting down...");
    Hub_exitError();
}

static void Hub_close(void) {
    Hub_Var_close();
    Hub_DB_close();
    Hub_Logging_close();
    
    /* Util is part of the core libseawolf, does not require an _init() call,
       but *does* require a _close() call */
    Util_close();
}

int main(int argc, char** argv) {
    /* Ensure shutdown during normal exit */
    atexit(Hub_close);
    
    /* Please *ignore* SIGPIPE. It will cause the program to close in the case
       of writing to a closed socket. We handle this ourselves. */
    signal(SIGPIPE, SIG_IGN);

    /* Catch common siginals and insure proper shutdown */
    signal(SIGINT, Hub_catchSignal);
    signal(SIGHUP, Hub_catchSignal);
    signal(SIGTERM, Hub_catchSignal);

    /* Use argument as database file */
    if(argc == 2) {
        Hub_DB_setFile(argv[1]);
    } else {
        Hub_DB_setFile("../db/seawolf.db");
    }

    /* Initialize subcomponents */
    Hub_DB_init();
    Hub_Var_init();
    Hub_Logging_init();

    /* Run the main network loop */
    Hub_Net_mainLoop();

    return 0;
}
