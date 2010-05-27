
#include "seawolf.h"
#include "seawolf3.h"

static void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    int front = (int) out * -0.5;
    Notify_send("THRUSTER_REQUEST", Util_format("Pitch %d %d %d", front, front, out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Pitch PID");

    PID* pid;
    char action[64], data[64];
    double mv;

    Notify_filter(FILTER_MATCH, "UPDATED PitchPID");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");

    pid = PID_new(0.0, Var_get("PitchPID.p"),
                       Var_get("PitchPID.i"),
                       Var_get("PitchPID.d"));

    mv = PID_start(pid, 0.0);
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "PitchPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("PitchPID.p"),
                                Var_get("PitchPID.i"),
                                Var_get("PitchPID.d"));
            PID_resetIntegral(pid);
        } else {
            mv = PID_update(pid, Var_get("SEA.Pitch"));
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
