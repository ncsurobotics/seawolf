
#include "seawolf.h"

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

    PID* rotpid;
    PID* straightpid;

    double mv;
    double yaw, rate;
    float mode;
    bool reset;

    char action[64], data[64];
   
    /* Default to not rotating in rotational rate mode */
    Var_set("RotHeading", 0.0);
    Var_set("RotMode", Var_get("RotModeRate"));
    mode = Var_get("RotMode");
    
    rotpid = PID_new(0.0,
                     Var_get("RotPID.p"),
                     Var_get("RotPID.i"),
                     Var_get("RotPID.d"));

    straightpid = PID_new(0.0,
                          Var_get("StraightPID.p"),
                          Var_get("StraightPID.i"),
                          Var_get("StraightPID.d"));

    Notify_filter(FILTER_MATCH, "UPDATED IMU");
    Notify_filter(FILTER_MATCH, "UPDATED RotPID");
    Notify_filter(FILTER_MATCH, "UPDATED StraightPID");
    Notify_filter(FILTER_MATCH, "UPDATED RotHeading");
    Notify_filter(FILTER_MATCH, "UPDATED RotMode");

    /* Zero ouputs */
    dataOut(0.0);

    /* Seed yaw derivative */
    do {
        Notify_get(action, data);
    } while(strcmp(data, "IMU") != 0);
    yaw = Var_get("SEA.Yaw");
    rate = yaw_dt(yaw);

    reset = true;

    while(true) {
        Notify_get(action, data);
        
        if(strcmp(data, "IMU") == 0) {
            yaw = Var_get("SEA.Yaw");
            rate = yaw_dt(yaw);

            //printf("%.2f\n", rate);
            if(mode == Var_get("RotModeRate")) {
                if(reset) {
                    mv = PID_start(rotpid, rate);
                } else {
                    mv = PID_update(rotpid, rate);
                }
            } else {
                if(reset) {
                    printf("Set desired heading to: %f\n", yaw);
                    PID_setSetPoint(straightpid, yaw);
                    mv = PID_start(straightpid, yaw);
                    reset = false;
                } else {
                    mv = PID_update(straightpid, yaw);
                }
                printf("PID Error: %f\n", straightpid->sp - yaw);
            }

            dataOut(mv);
        } else if(strcmp(data, "RotHeading") == 0) {
            /* Update rotation rate heading */
            PID_setSetPoint(rotpid, Var_get("RotHeading"));
        } else if(strcmp(data, "RotMode") == 0) {
            /* Mode change, reset PID */
            mode = Var_get("RotMode");
            reset = true;
        } else if(strcmp(data, "RotPID") == 0) {
            PID_setCoefficients(rotpid,
                                Var_get("RotPID.p"),
                                Var_get("RotPID.i"),
                                Var_get("RotPID.d"));
        } else if(strcmp(data, "StraightPID") == 0) {
            PID_setCoefficients(straightpid,
                                Var_get("StraightPID.p"),
                                Var_get("StraightPID.i"),
                                Var_get("StraightPID.d"));
        }
    }

    Seawolf_close();
    return 0;
}
