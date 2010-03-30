
#include "seawolf.h"

static void dataOut(double mv) {
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %d %d", (int) mv, (int) -mv));
}

/* Calculate the rate of change in the yaw with respect to time */
static float yaw_dt(float yaw) {
    static Timer* timer = NULL;
    static float yaw_last;
    float dt, rate;

    if(timer == NULL) {
        timer = Timer_new();
        yaw_last = yaw;
        rate = 0;
    } else {
        dt = Timer_getDelta(timer);
        rate = (yaw - yaw_last) / dt;
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

            if(mode == Var_get("RotModeRate")) {
                if(reset) {
                    mv = PID_start(rotpid, rate);
                    reset = false;
                } else {
                    mv = PID_update(rotpid, rate);
                }
            } else {
                if(reset) {
                    PID_setSetPoint(straightpid, yaw);
                    mv = PID_start(straightpid, yaw);
                    reset = false;
                } else {
                    mv = PID_update(straightpid, yaw);
                }
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
