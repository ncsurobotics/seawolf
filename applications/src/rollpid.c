
#include "seawolf.h"

static void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    Notify_send("THRUSTER_REQUEST", Util_format("Roll %d %d", out, -out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Roll PID");

    PID* pid;
    char action[64], data[64];
    double mv;

    Notify_filter(FILTER_MATCH, "UPDATED RollPID");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");

    pid = PID_new(0.0, Var_get("RollPID.p"),
                       Var_get("RollPID.i"),
                       Var_get("RollPID.d"));

    mv = PID_start(pid, 0.0);
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "RollPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("RollPID.p"),
                                Var_get("RollPID.i"),
                                Var_get("RollPID.d"));
            PID_resetIntegral(pid);
        } else {
            mv = PID_update(pid, Var_get("SEA.Roll"));
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
