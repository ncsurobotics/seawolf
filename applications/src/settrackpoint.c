
#include "seawolf.h"

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    SeaSQL_setAutoNotify(false);
    Seawolf_init("Set Tracker Set Point");

    if(argc != 3) {
        fprintf(stderr, "Missing arguments\nUsage: %s <theta> <phi>\n", argv[0]);
    }

    int t, p;
    t = atoi(argv[1]);
    p = atoi(argv[2]);

    SeaSQL_setSetPointSource(1);
    SeaSQL_setSetPointVision_Theta(t);
    SeaSQL_setSetPointVision_Phi(p);
    SeaSQL_setSetPointVision_Rho(5);
    Notify_send("UPDATED", "SetPointVision");

    Seawolf_close();
    return 0;
}
