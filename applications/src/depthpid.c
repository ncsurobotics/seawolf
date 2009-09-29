
#include "seawolf.h"

void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    int front = (int) out * 0.7;
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", front, front, out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Depth PID");

    PID* pid;
    char action[64], data[64];
    double mv;

    Notify_filter(FILTER_MATCH, "UPDATED DepthPID");
    Notify_filter(FILTER_MATCH, "UPDATED DepthHeading");
    Notify_filter(FILTER_MATCH, "UPDATED Depth");

    pid = PID_new(SeaSQL_getDepthHeading(),
                  SeaSQL_getDepthPID_p(),
                  SeaSQL_getDepthPID_i(),
                  SeaSQL_getDepthPID_d());

    mv = PID_start(pid, SeaSQL_getDepth());
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "DepthPID") == 0) {
            PID_setCoefficients(pid,
                                SeaSQL_getDepthPID_p(),
                                SeaSQL_getDepthPID_i(),
                                SeaSQL_getDepthPID_d());
            PID_resetIntegral(pid);
        } else if(strcmp(data, "DepthHeading") == 0) {
            PID_setSetPoint(pid, SeaSQL_getDepthHeading());
            mv = PID_start(pid, SeaSQL_getDepth());
        } else {
            mv = PID_update(pid, SeaSQL_getDepth());
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
