
#include "seawolf.h"
#include "seawolf3.h"

static void dataOut(double mv) {
    float out = Util_inRange(-1.0, mv, 1.0);
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %.4f", out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Yaw PID");

    PID* pid;
    char data[64];
    double mv;
    bool paused = (Var_get("YawPID.Paused") != 0.0);

    Notify_filter(FILTER_MATCH, "UPDATED YawPID.Coefficients");
    Notify_filter(FILTER_MATCH, "UPDATED YawPID.Heading");
    Notify_filter(FILTER_MATCH, "UPDATED YawPID.Paused");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");

    pid = PID_new(Var_get("YawPID.Heading"),
                  Var_get("YawPID.p"),
                  Var_get("YawPID.i"),
                  Var_get("YawPID.d"));
    dataOut(0.0);

    while(true) {
        Notify_get(NULL, data);

        double yaw = Var_get("SEA.Yaw");
        if(strcmp(data, "YawPID.Coefficients") == 0) {
            PID_setCoefficients(pid,
                                Var_get("YawPID.p"),
                                Var_get("YawPID.i"),
                                Var_get("YawPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "YawPID.Heading") == 0) {
            PID_setSetPoint(pid, Var_get("YawPID.Heading"));
            mv = PID_update(pid, yaw);
            if(paused) {
                Var_set("YawPID.Paused", 0.0);
            }
        } else if(strcmp(data, "YawPID.Paused") == 0) {
            bool p = (Var_get("YawPID.Paused") != 0.0);
            if(p == paused) {
                continue;
            }

            paused = p;
            if(paused) {
                dataOut(0.0);
                Notify_send("PIDPAUSED", "Yaw");
            }
        } else if(strcmp(data, "IMU") == 0 && paused == false) {
            mv = PID_update(pid, yaw);
        }
        
        if(paused == false) {
            dataOut(mv);
        }
    }

    Seawolf_close();
    return 0;
}
