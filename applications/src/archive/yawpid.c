
#include "seawolf.h"

#include <math.h>

#define THRUSTER_CAP 0.4
#define ACTIVE_REGION 30

static double thruster_log(double mv) {
    if (fabs(mv) < 0.01) return 0.0;
    return (mv/fabs(mv)) * log2(fabs(mv) + 1);
}

static void dataOut(double mv) {
    float out = Util_inRange(-THRUSTER_CAP, thruster_log(mv), THRUSTER_CAP);
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %.4f", out));
}

static double angleError(double a1, double a2) {
    double error = (a2 - a1);

    if(fabs(error) > 180) {
        if(error < 0) {
            return (360.0 - fabs(error));
        }

        return -(360.0 - fabs(error));
    }

    return error;
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Yaw PID");

    Var_subscribe("YawPID.p");
    Var_subscribe("YawPID.i");
    Var_subscribe("YawPID.d");
    Var_subscribe("YawPID.Heading");
    Var_subscribe("YawPID.Paused");
    Var_subscribe("SEA.Yaw");

    PID* pid;
    double mv;
    double yaw;
    bool paused = (Var_get("YawPID.Paused") != 0.0);
    float heading = Var_get("YawPID.Heading");

    pid = PID_new(0.0, Var_get("YawPID.p"),
                       Var_get("YawPID.i"),
                       Var_get("YawPID.d"));

    // set active region (region where response of the robot
    // is practically linear). Outside this region, thrusters
    // would be maxed out, and the ITerm would get staturated.
    // Outside this region, the we use PD control. Inside this
    // region, we use PID control.
    PID_setActiveRegion(pid, ACTIVE_REGION);

    dataOut(0.0);

    while(true) {

        Var_sync();

        /* Update SEA.Yaw */
        if (Var_stale("SEA.Yaw")) {
            yaw = Var_get("SEA.Yaw");
        }

        /* Update PID Coefficients */
        if (Var_stale("YawPID.p") ||
            Var_stale("YawPID.i") ||
            Var_stale("YawPID.d"))
        {
            PID_setCoefficients(pid,
                                Var_get("YawPID.p"),
                                Var_get("YawPID.i"),
                                Var_get("YawPID.d"));
            PID_resetIntegral(pid);
        }

        /* Update Heading */
        if (Var_stale("YawPID.Heading")) {
            heading = Var_get("YawPID.Heading");
            // Automatically unpause if heading is updated
            if(paused) {
                Var_set("YawPID.Paused", 0.0);
            }
        }

        /* Update Paused */
        if (Var_stale("YawPID.Paused")) {
            paused = (Var_get("YawPID.Paused") != 0.0);
            if (paused) {
                dataOut(0.0);
                Notify_send("PIDPAUSED", "Yaw");
                PID_pause(pid);
            }
        }

        /* Update Thrusters */
        if (paused == false)
        {
            mv = PID_update(pid, angleError(heading, yaw));
            dataOut(mv);
        }

        //Util_usleep(0.01);

    }

    Seawolf_close();
    return 0;
}
