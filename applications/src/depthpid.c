
#include "seawolf.h"

static int thruster_max;

static void dataOut(double mv) {
    int out = Util_inRange(-thruster_max, (int) mv, thruster_max);
    int front = (int) out * 0.7;
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", front, front, out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Depth PID");

    PID* pid;
    char action[64], data[64];
    double mv;

    thruster_max = Var_get("ThrusterMax");

    Notify_filter(FILTER_MATCH, "UPDATED DepthPID");
    Notify_filter(FILTER_MATCH, "UPDATED DepthHeading");
    Notify_filter(FILTER_MATCH, "UPDATED Depth");

    pid = PID_new(Var_get("DepthHeading"),
                  Var_get("DepthPID.p"),
                  Var_get("DepthPID.i"),
                  Var_get("DepthPID.d"));

    mv = PID_start(pid, Var_get("Depth"));
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "DepthPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("DepthPID.p"),
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "DepthHeading") == 0) {
            PID_setSetPoint(pid, Var_get("DepthHeading"));
            mv = PID_start(pid, Var_get("Depth"));
        } else {
            mv = PID_update(pid, Var_get("Depth"));
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
