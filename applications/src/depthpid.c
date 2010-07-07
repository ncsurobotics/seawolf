
#include "seawolf.h"
#include "seawolf3.h"

#define THRUSTER_CAP 30

static void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    int front = (int) out * 0.7;
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", front, front, out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Depth PID");

    PID* pid;
    char data[64];
    double mv;

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
        Notify_get(NULL, data);

        if(strcmp(data, "DepthPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("DepthPID.p"),
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "DepthHeading") == 0) {
            PID_setSetPoint(pid, Var_get("DepthHeading"));
            mv = PID_update(pid, Var_get("Depth"));
        } else {
            mv = PID_update(pid, Var_get("Depth"));
        }
       
        if(pid->sp == 0){
             PID_resetIntegral(pid);
        }

        // Don't let the motors run too fast
        if (mv > THRUSTER_CAP) mv = THRUSTER_CAP;
        else if(mv < -1*THRUSTER_CAP) mv = -1* THRUSTER_CAP;

        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
