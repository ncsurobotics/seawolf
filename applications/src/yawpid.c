
#include "seawolf.h"

static void dataOut(double mv) {
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %d %d", (int) mv, (int) -mv));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Yaw PID");

    PID* pid;
    char action[64], data[64];
    double mv;
    bool do_yaw = (Var_get("PIDDoYaw") == 1.0);
    float yaw;
    float yaw_heading = Var_get("YawHeading");
    
    Notify_filter(FILTER_MATCH, "UPDATED IMU");
    Notify_filter(FILTER_MATCH, "UPDATED YawPID");
    Notify_filter(FILTER_MATCH, "UPDATED YawHeading");
    Notify_filter(FILTER_MATCH, "UPDATED PIDDoYaw");

    pid = PID_new(yaw_heading,
                  Var_get("YawPID.p"),
                  Var_get("YawPID.i"),
                  Var_get("YawPID.d"));

    Var_set("PIDDoYaw", 0);
    mv = PID_start(pid, Var_get("SEA.Yaw"));
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "YawPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("YawPID.p"),
                                Var_get("YawPID.i"),
                                Var_get("YawPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "YawHeading") == 0) {
            yaw_heading = Var_get("YawHeading");
            PID_setSetPoint(pid, yaw_heading);
            mv = PID_start(pid, Var_get("SEA.Yaw"));
        } else if(strcmp(data, "PIDDoYaw") == 0) {
            do_yaw = (Var_get("PIDDoYaw") == 1.0);
        } else {
            yaw = Var_get("SEA.Yaw");
            if(yaw - yaw_heading > 0 && yaw - yaw_heading < 180) {
                mv = PID_update(pid, yaw);
            } else if(yaw - yaw_heading > 180) {
                mv = PID_update(pid, yaw - 360);
            } else if(yaw - yaw_heading < 0 && yaw - yaw_heading > -180) {
                mv = PID_update(pid, yaw);
            } else {
                mv = PID_update(pid, 360 - yaw);
            }
        }
        
        if(do_yaw) {
            dataOut(mv);
        }
    }

    Seawolf_close();
    return 0;
}
