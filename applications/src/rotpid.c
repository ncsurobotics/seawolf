
#include "seawolf.h"
#include "seawolf3.h"

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

    PID* angularpid;
    PID* ratepid;

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
    ratepid = PID_new(0.0,
                          Var_get("Rot.Rate.p"),
                          Var_get("Rot.Rate.i"),
                          Var_get("Rot.Rate.d"));

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
    PID_start(ratepid, rate);
    Var_set("Rot.Angular.Target", yaw);

    while(true) {
        Notify_get(NULL, data);

        if(strcmp(data, "IMU") == 0) {
            yaw = Var_get("SEA.Yaw");
            rate = yaw_dt(yaw);

            if(mode == ROT_MODE_RATE) {
                mv = PID_update(ratepid, rate);
            } else if (mode == ROT_MODE_ANGULAR) {
                mv = PID_update(angularpid, yaw);
            } else {
                printf("Rot.Mode is incorrectly set to \"%f\"!!!!\n", Var_get("Rot.Mode"));
            }

            dataOut(mv);

        } else if(strcmp(data, "Rot.Rate.Target") == 0) {
            PID_setSetPoint(ratepid, Var_get("Rot.Rate.Target"));

        } else if(strcmp(data, "Rot.Angular.Target") == 0) {
            PID_setSetPoint(angularpid, Var_get("Rot.Angular.Target"));

        } else if(strcmp(data, "Rot.Mode") == 0) {
            mode = Var_get("Rot.Mode");

        } else if(strncmp(data, "Rot.Rate", 8) == 0) {
            PID_setCoefficients(ratepid,
                                Var_get("Rot.Rate.p"),
                                Var_get("Rot.Rate.i"),
                                Var_get("Rot.Rate.d"));

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
