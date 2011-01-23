
#include "seawolf.h"
#include "seawolf3.h"

#define THRUSTER_CAP 0.8  // Thrusters capped at this unless panicing
#define PANIC_DEPTH  12.0 // At what depth we panic and go up full force
#define PANIC_TIME   10.0 // Time in seconds that we panic

static void dataOut(double mv) {
    float out = Util_inRange(-1.0, mv, 1.0);
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %.4f", out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Depth PID");

    PID* pid;
    char data[64];
    double mv;
    bool paused = Var_get("DepthPID.Paused");

    Notify_filter(FILTER_MATCH, "UPDATED DepthPID.Coefficients");
    Notify_filter(FILTER_MATCH, "UPDATED DepthPID.Heading");
    Notify_filter(FILTER_MATCH, "UPDATED DepthPID.Paused");
    Notify_filter(FILTER_MATCH, "UPDATED Depth");

    pid = PID_new(Var_get("DepthPID.Heading"),
                  Var_get("DepthPID.p"),
                  Var_get("DepthPID.i"),
                  Var_get("DepthPID.d"));
    dataOut(0.0);

    while(true) {
        Notify_get(NULL, data);

        double depth = Var_get("Depth");
        if(strcmp(data, "DepthPID.Coefficients") == 0) {
            PID_setCoefficients(pid,
                                Var_get("DepthPID.p"),
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "DepthPID.Heading") == 0) {
            PID_setSetPoint(pid, Var_get("DepthPID.Heading"));
            mv = PID_update(pid, depth);
            if(paused) {
                Var_set("DepthPID.Paused", 0.0);
            }
        } else if(strcmp(data, "DepthPID.Paused") == 0) {
            bool p = Var_get("DepthPID.Paused");
            if(p == paused) {
                continue;
            }

            paused = p;
            if(paused) {
                dataOut(0.0);
                Notify_send("PIDPAUSED", "Depth");
            }
        } else if(strcmp(data, "Depth") == 0 && paused == false) {
            mv = PID_update(pid, depth);
        }
       
        /* Under ordinary circumstances limit thruster values */
        mv = Util_inRange(-THRUSTER_CAP, mv, THRUSTER_CAP);

        /* If we're too deep attempt to surface at all costs immediately */
        if(depth > PANIC_DEPTH) {
            Logging_log(CRITICAL, Util_format("Depth: %f\n", depth));
            Logging_log(CRITICAL, "Oh Em Geez!  I'm too freekin deep, rising full force!\n");

            dataOut(-1.0);
            Util_usleep(PANIC_TIME);
        } else if(paused == false) {
            dataOut(mv);
        }
    }

    Seawolf_close();
    return 0;
}
