
#include "seawolf.h"
#include "seawolf3.h"

#include <math.h>
#include <stdarg.h>
#include <unistd.h>
#include <signal.h>

#define MAX_ARGS 31

/* Run an application with the given NULL terminated argument list. The
   application will fork into the background and the current program will
   resume. The PID of the spawned application is returned. */
static int spawn(char* path, char* args, ...) {
    int pid;
    va_list ap;
    char* argv[MAX_ARGS + 1];

    /* Build arguments array */
    argv[0] = path;
    argv[1] = NULL;

    va_start(ap, args);
    for(int i = 1; i < MAX_ARGS && args != NULL; i++) {
        argv[i] = args;
        argv[i+1] = NULL;
        args = va_arg(ap, char*);
    }
    va_end(ap);

    /* Run program */
    pid = fork();
    if(pid == 0) {
        /* Replace current process with the given application */
        execv(path, argv);
        
        /* Should *not* happen */
        fprintf(stderr, "Application %s failed to spawn!\n", path);
        exit(EXIT_FAILURE);
    }

    return pid;
}

static void zero_thrusters(void) {
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 0, 0));

    /* Turn off drivers */
    Var_set("PortX", 0);
    Var_set("PortY", 0);
    Var_set("StarX", 0);
    Var_set("StarY", 0);
    Var_set("Aft", 0);

    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", 0, 0, 0));
    Notify_send("THRUSTER_REQUEST", Util_format("Roll %d %d", 0, 0));
    Var_set("DepthHeading", 0.0);

    // Zero yaw pid
    float current_yaw = Var_get("SEA.Yaw");
    Var_set("Rot.Mode", 1.0);
    Var_set("Rot.Angular.Target", current_yaw);

    Var_set("Strafe", 0.0);
}

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Conductor");

    /* PIDs of all spawned applications */
    int pid[8];
    char event[16];
    bool running = false;

    Notify_filter(FILTER_MATCH, "EVENT MissionStart");
    Notify_filter(FILTER_MATCH, "EVENT PowerKill");
    Notify_filter(FILTER_MATCH, "EVENT SystemReset");

    /* Clear VisionReset */
    Var_set("VisionReset", 0.0);
    zero_thrusters();
    Var_set("StatusLight", STATUS_LIGHT_OFF);

    while(true) {
        Notify_get(NULL, event);

        if(strcmp(event, "MissionStart") == 0) {
            if(running == true) {
                Logging_log(ERROR, "Received MissionStart while running");
                continue;
            }

            Var_set("StatusLight", STATUS_LIGHT_BLINK);
            for(int i = 3; i > 0; i--) {
                Logging_log(DEBUG, Util_format("Preparing to start - %d", i));
                Util_usleep(1);
            }
            
            /* Start everthing */
            pid[0] = spawn("./bin/depthpid", NULL);
            pid[1] = spawn("./bin/rotpid", NULL);
            Util_usleep(0.5);

            pid[2] = spawn("./bin/mixer", NULL);
            Util_usleep(0.5);

            // The go vision signal is NOT sent here.  The mixer will send it
            // (ugly, I know) because it's the easiest way to prevent race
            // conditions.  For example, vision could send a FORWARD request
            // before the mixer starts.
            //Notify_send("GO", "Vision");

            Var_set("StatusLight", STATUS_LIGHT_ON);
            running = true;
        } else if(strcmp(event, "PowerKill") == 0) {
            if(running == false) {
                Logging_log(ERROR, "Received PowerKill while not running!");
                continue;
            }

            zero_thrusters();
            Logging_log(DEBUG, "Killing...");

            kill(pid[0], SIGTERM);
            kill(pid[1], SIGTERM);
            kill(pid[2], SIGTERM);

            zero_thrusters();
            Util_usleep(0.1);
            zero_thrusters();
            Util_usleep(1.0);
            
            Var_set("VisionReset", 1.0);
            zero_thrusters();
            Var_set("StatusLight", STATUS_LIGHT_OFF);

            /* Wait for vision to acknowledge reset */
            while(Var_get("VisionReset") == 1.0) {
                Util_usleep(0.05);
            }

            running = false;
        } else if(strcmp(event, "SystemReset") == 0) {
            Logging_log(DEBUG, "System reset");
        } else {
            Logging_log(ERROR, Util_format("Received invalid event '%s'", event));
        }
    }

    Seawolf_close();
    return 0;
}
