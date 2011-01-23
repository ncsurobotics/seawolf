
#include "seawolf.h"
#include "seawolf3.h"

static void dataOut(double mv) {
    float out = Util_inRange(-1.0, mv, 1.0);
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %.4f", out));
}

static double yaw_dt(void) {
    static Timer* timer = NULL;
    static double last_yaw = 0.0;
    double yaw, dt;

    yaw = Var_get("SEA.Yaw");
    
    if(timer == NULL) {
        timer = Timer_new();
        dt = 0.0;
    } else {
        dt = (yaw - last_yaw) / Timer_getDelta(timer);
    }

    last_yaw = yaw;
    return dt;
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Rotate PID");

    PID* pid;
    char data[64];
    double mv;
    bool paused = Var_get("RotatePID.Paused");

    Notify_filter(FILTER_MATCH, "UPDATED RotatePID.Coefficients");
    Notify_filter(FILTER_MATCH, "UPDATED RotatePID.Heading");
    Notify_filter(FILTER_MATCH, "UPDATED RotatePID.Paused");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");

    pid = PID_new(Var_get("RotatePID.Heading"),
                  Var_get("RotatePID.p"),
                  Var_get("RotatePID.i"),
                  Var_get("RotatePID.d"));
    dataOut(0.0);

    while(true) {
        Notify_get(NULL, data);

        double rate = yaw_dt();
        if(strcmp(data, "RotatePID.Coefficients") == 0) {
            PID_setCoefficients(pid,
                                Var_get("RotatePID.p"),
                                Var_get("RotatePID.i"),
                                Var_get("RotatePID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "RotatePID.Heading") == 0) {
            PID_setSetPoint(pid, Var_get("RotatePID.Heading"));
            mv += PID_update(pid, rate);
            if(paused) {
                Var_set("RotatePID.Paused", 0.0);
            }
        } else if(strcmp(data, "RotatePID.Paused") == 0) {
            bool p = Var_get("RotatePID.Paused");
            if(p == paused) {
                continue;
            }

            paused = p;
            if(paused) {
                dataOut(0.0);
                Notify_send("PIDPAUSED", "Rotate");
            }
        } else if(paused == true) {
            mv += PID_update(pid, rate);
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
