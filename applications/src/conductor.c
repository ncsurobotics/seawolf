
#include "seawolf.h"

#include <math.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>

/* Top level Seawolf directory */
#define SEAWOLF_DIR "../"

static int spawn(const char* path) {
    int pid = fork();
    if(pid == 0) {
        /* Replace current process with the given application */
        execl(path, path, NULL);
        
        /* Should *not* happen */
        fprintf(stderr, "Application %s failed to spawn!\n", path);
        exit(EXIT_FAILURE);
    }

    return pid;
}

static int spawn_vision(const char* path, char* cam1, char* cam2, char* cam3) {
    int pid = fork();
    if(pid == 0) {
        /* Replace current process with the given application */
        execl(path, path, cam1, cam2, cam3, NULL);
        
        /* Should *not* happen */
        fprintf(stderr, "Application %s failed to spawn!\n", path);
        exit(EXIT_FAILURE);
    }

    return pid;
}

static void usage(char* nm) {
    fprintf(stderr, "usage: %s {ident|test|arm|mission}\n", nm);
    exit(1);
}

int main(int argc, char** argv) {
    bool ident = false;
    bool test = false;
    bool mission = false;
    int pid[8];

    if(argc == 1) {
        usage(argv[0]);
    } else if(strcmp(argv[1], "ident") == 0) {
        ident = true;
    } else if(strcmp(argv[1], "test") == 0) {
        test = true;
    } else if(strcmp(argv[1], "mission") == 0) {
        mission = true;
    } else if(strcmp(argv[1], "arm")) {
        usage(argv[0]);
    }

    /* Change to the base directory */
    chdir(SEAWOLF_DIR);

    Seawolf_loadConfig("conf/seawolf.conf");
    Seawolf_init("Conductor");

    /* Move on to applications */
    chdir("applications/");
    if(ident) {
        // -
    } else if(test) {
        spawn("./bin/remotecontrol");
    } else {
        Notify_filter(0, NULL);
        Notify_filter(FILTER_ACTION, "MISSIONTRIGGER");

        if(mission) {
            while(true) {
                Var_set("TrackerDoDepth", 0);
                Var_set("DepthHeading", 0);
                Var_set("PIDDoYaw", 0);
                Var_set("SetPoint.Theta", 0);
                Var_set("SetPoint.Phi", 0);
                Var_set("SetPoint.Rho", 0);
                Var_set("SetPointVision.Theta", 0);
                Var_set("SetPointVision.Phi", 0);
                Var_set("SetPointVision.Rho", 0);
                Var_set("SetPointSource", Var_get("SetPointSource:Vision"));

                Var_set("PortX", 0);
                Var_set("StarX", 0);
                Var_set("PortY", 0);
                Var_set("StarY", 0);
                Var_set("Aft", 0);

                chdir("../vision/seavision/");
                pid[0] = spawn_vision("./mission", argv[2], argv[3], argv[4]);
                
                Notify_get(NULL, NULL);
                for(int i = 5; i > 0; i--) {
                    Logging_log(DEBUG, Util_format("Preparing to start - %d", i));
                    Util_usleep(1);
                }

                chdir("../../applications/");
                pid[1] = spawn("./bin/mission");
                pid[2] = spawn("./bin/depthpid");
                pid[3] = spawn("./bin/yawpid");
                pid[4] = spawn("./bin/trackerproxy");
                pid[5] = spawn("./bin/tracker");

                Util_usleep(1);
                pid[6] = spawn("./bin/mixer");

                Notify_get(NULL, NULL);
                Logging_log(DEBUG, "Killing...");
                kill(pid[0], SIGTERM);
                kill(pid[1], SIGTERM);
                kill(pid[2], SIGTERM);
                kill(pid[3], SIGTERM);
                kill(pid[4], SIGTERM);
                kill(pid[5], SIGTERM);
                kill(pid[6], SIGTERM);
                Util_usleep(1.0);
            }
        }
    }

    Seawolf_close();
    return 0;
}
