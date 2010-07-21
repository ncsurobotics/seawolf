
#include "seawolf.h"
#include "seawolf3.h"

#define THRUSTER_CAP 25

static void dataOut(double mv) {
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %d %d", (int) mv, (int) -mv));
}

/* Calculate the rate of change in the yaw with respect to time */
static float yaw_dt(float yaw) {
    static Timer* timer = NULL;
    static float yaw_last;
    double dt, rate;

    if(timer == NULL) {
        timer = Timer_new();
        yaw_last = yaw;
        rate = 0.0;
    } else {
        dt = Timer_getDelta(timer);
        if (dt < 0.01) {
            //printf("dt Less than 0.01!\n");
        } else {
            rate = (yaw - yaw_last) / dt;
            //printf("            %6.4f %6.4f          %.4f  %.4f\n", yaw, yaw_last, dt, rate);
        }
        yaw_last = yaw;
    }

    return rate;
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Yaw PID");

    double angularpid_setpoint = 0.0;
    PID* angularpid;
    //PID* ratepid;
    double rot_rate_p = Var_get("Rot.Rate.p");
    double rot_rate_target = Var_get("Rot.Rate.Target");

    double mv;
    double yaw, rate;
    float mode;
    
    char data[64];

    /* Default to not rotating in rotational rate mode */
    Var_set("Rot.Angular.Target", 0.0);
    Var_set("Rot.Rate.Target", 0.0);
    mode = ROT_MODE_ANGULAR;
    Var_set("Rot.Mode", mode);

    angularpid = PID_new(0.0,
                     Var_get("Rot.Angular.p"),
                     Var_get("Rot.Angular.i"),
                     Var_get("Rot.Angular.d"));
    //ratepid = PID_new(0.0,
                          //Var_get("Rot.Rate.p"),
                          //Var_get("Rot.Rate.i"),
                          //Var_get("Rot.Rate.d"));

    Notify_filter(FILTER_MATCH, "UPDATED IMU");
    Notify_filter(FILTER_PREFIX, "UPDATED Rot");
    //Notify_filter(FILTER_MATCH, "UPDATED Rot.Angular.Target");

    /* Zero ouputs */
    dataOut(0.0);

    /* Initialize PIDs */
    do {
        Notify_get(NULL, data);
    } while(strcmp(data, "IMU") != 0);
    yaw = Var_get("SEA.Yaw");
    rate = yaw_dt(yaw);
    PID_start(angularpid, yaw);
    //PID_start(ratepid, rate);
    Var_set("Rot.Angular.Target", yaw);

    while(true) {
        Notify_get(NULL, data);

        if(strcmp(data, "IMU") == 0) {
            yaw = Var_get("SEA.Yaw");
            //rate = yaw_dt(yaw);

            if(mode == ROT_MODE_RATE) {
                //mv = PID_update(ratepid, rate);
                mv = rot_rate_p * rot_rate_target;

            } else if (mode == ROT_MODE_ANGULAR) {

                // Give angularpid the error, it's setpoint is always 0.0
                // We do this so that we can test which way around the 360
                // degree circle is closer to go.
                double error = yaw - angularpid_setpoint;
                if (error > 180) {
                    error = error-360;
                } else if (error < -180) {
                    error = 360+error;
                }

                //printf("Error: %f\n", error);
                mv = PID_update(angularpid, error);

                // Don't let the motors run too fast
                if (mv > THRUSTER_CAP) mv = THRUSTER_CAP;
                else if(mv < -1*THRUSTER_CAP) mv = -1* THRUSTER_CAP;

            } else {
                printf("Rot.Mode is incorrectly set to \"%f\"!!!!\n", Var_get("Rot.Mode"));
            }

            dataOut(mv);

        } else if(strcmp(data, "Rot.Rate.Target") == 0) {
            rot_rate_target = Var_get("Rot.Rate.Target");
            //PID_setSetPoint(ratepid, Var_get("Rot.Rate.Target"));

        } else if(strcmp(data, "Rot.Angular.Target") == 0) {
            // Keep track of the setpoint internally
            angularpid_setpoint = Var_get("Rot.Angular.Target");
            //PID_setSetPoint(angularpid, Var_get("Rot.Angular.Target"));

        } else if(strcmp(data, "Rot.Mode") == 0) {
            mode = Var_get("Rot.Mode");

        } else if(strncmp(data, "Rot.Rate", 8) == 0) {
            rot_rate_p = Var_get("Rot.Rate.p");
            //PID_setCoefficients(ratepid,
                                //Var_get("Rot.Rate.p"),
                                //Var_get("Rot.Rate.i"),
                                //Var_get("Rot.Rate.d"));

        } else if(strncmp(data, "Rot.Angular", 11) == 0) {
            PID_setCoefficients(angularpid,
                                Var_get("Rot.Angular.p"),
                                Var_get("Rot.Angular.i"),
                                Var_get("Rot.Angular.d"));
        }
    }

    Seawolf_close();
    return 0;
}
