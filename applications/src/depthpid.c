
#include "seawolf.h"
#include "seawolf3.h"

#define THRUSTER_CAP 0.8  // Thrusters capped at this unless panicing
#define PANIC_DEPTH  12.0 // At what depth we panic and go up full force
#define PANIC_TIME   10.0 // Time in seconds that we panic

//#define BASE_I 0.3
#define BASE_I 0.2

static void dataOut(double mv) {
    float out = Util_inRange(-1.0, mv, 1.0);
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %.4f", out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Depth PID");

    Var_subscribe("DepthPID.p");
    Var_subscribe("DepthPID.i");
    Var_subscribe("DepthPID.d");
    Var_subscribe("DepthPID.Heading");
    Var_subscribe("DepthPID.Paused");
    Var_subscribe("Depth");

    PID* pid;
    double mv;
    double depth = Var_get("Depth");
    bool paused = Var_get("DepthPID.Paused");

    pid = PID_new(Var_get("DepthPID.Heading"),
                  Var_get("DepthPID.p"),
                  Var_get("DepthPID.i"),
                  Var_get("DepthPID.d"));
    pid->e_dt = BASE_I / pid->i;
    dataOut(0.0);

    while(true) {

        Var_sync();

        /* Update Depth */
        if (Var_stale("Depth")) {
            depth = Var_get("Depth");
        }

        /* Update PID Coefficients */
        if (Var_stale("DepthPID.p") ||
            Var_stale("DepthPID.i") ||
            Var_stale("DepthPID.d"))
        {
            PID_setCoefficients(pid,
                                Var_get("DepthPID.p"),
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
            //PID_resetIntegral(pid);
            pid->e_dt = BASE_I / pid->i;
        }

        /* Update Heading */
        if (Var_poked("DepthPID.Heading")) {
            PID_setSetPoint(pid, Var_get("DepthPID.Heading"));
            // Automatically unpause if heading is updated
            if (paused) {
                Var_set("DepthPID.Paused", 0.0);
            }
        }

        //printf("e_dt = %f\n", pid->e_dt);
        /*
        if (Var_get("DepthPID.Heading") - depth < -1) {
            PID_setCoefficients(pid,
                                0.0,
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
        } else {
            PID_setCoefficients(pid,
                                Var_get("DepthPID.p"),
                                Var_get("DepthPID.i"),
                                Var_get("DepthPID.d"));
        }
        */

        /* Update Paused */
        if (Var_stale("DepthPID.Paused")) {
            paused = Var_get("DepthPID.Paused");
            if (paused) {
                dataOut(0.0);
                Notify_send("PIDPAUSED", "Depth");
                PID_pause(pid);
            }
        }

        /* Panic and breach if too deep. */
        if(depth > PANIC_DEPTH) {
            Logging_log(CRITICAL, Util_format("Depth: %f\n", depth));
            Logging_log(CRITICAL, "I'm too deep!  Rising full force!\n");

            dataOut(-1.0);
            Util_usleep(PANIC_TIME);

        /* Update Thrusters */
        } else if (paused == false) {
            mv = PID_update(pid, depth);
            mv = Util_inRange(-THRUSTER_CAP, mv, THRUSTER_CAP);
            dataOut(mv);
        }

    }

    Seawolf_close();
    return 0;
}
