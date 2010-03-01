
#include "seawolf.h"

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Var_setAutoNotify(false);
    Seawolf_init("Set Tracker Set Point");

    if(argc != 3) {
        fprintf(stderr, "Missing arguments\nUsage: %s <theta> <phi>\n", argv[0]);
    }

    int t, p;
    t = atoi(argv[1]);
    p = atoi(argv[2]);

    Var_set("SetPointSource", 1);
    Var_set("SetPointVision.Theta", t);
    Var_set("SetPointVision.Phi", p);
    Var_set("SetPointVision.Rho", 5);
    Notify_send("UPDATED", "SetPointVision");

    Seawolf_close();
    return 0;
}
