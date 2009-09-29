
#include "seawolf.h"

void dataOut(double mv) {
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

    pid = PID_new(0.0, SeaSQL_getPitchPID_p(),
                       SeaSQL_getPitchPID_i(),
                       SeaSQL_getPitchPID_d());

    mv = PID_start(pid, 0.0);
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "PitchPID") == 0) {
            PID_setCoefficients(pid,
                                SeaSQL_getPitchPID_p(),
                                SeaSQL_getPitchPID_i(),
                                SeaSQL_getPitchPID_d());
            PID_resetIntegral(pid);
        } else {
            mv = PID_update(pid, SeaSQL_getSEA_Pitch());
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
