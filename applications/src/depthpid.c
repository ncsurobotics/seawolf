
#include "seawolf.h"
#include "seawolf3.h"

#define THRUSTER_CAP 50   // Thrusters capped at this unless panicing
#define PANIC_DEPTH  12.0 // At what depth we panic and go up full force
#define PANIC_TIME   10.0 // Time in seconds that we panic

static void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d", out, out));
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

        double depth = Var_get("Depth");
        if(strcmp(data, "DepthPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("DepthPID.p"),
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "DepthHeading") == 0) {
            PID_setSetPoint(pid, Var_get("DepthHeading"));
            mv = PID_update(pid, depth);
        } else {
            mv = PID_update(pid, depth);
        }
       
        if(pid->sp == 0){
             PID_resetIntegral(pid);
        }

        /* Under ordinary circumstances limit thruster values */
        mv = Util_inRange(-THRUSTER_CAP, mv, THRUSTER_CAP);

        /* If we're too deep attempt to surface at all costs immediately */
        if(depth > PANIC_DEPTH) {
            Logging_log(CRITICAL, Util_format("Depth: %f\n", depth));
            Logging_log(CRITICAL, "Oh Em Geez!  I'm too freekin deep, rising full force!\n");

            Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d", -THRUSTER_MAX, -THRUSTER_MAX));
            Util_usleep(PANIC_TIME);
        } else {
            dataOut(mv);
        }
    }

    Seawolf_close();
    return 0;
}
