
#include "seawolf.h"
#include "seawolf3.h"

static void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    Notify_send("THRUSTER_REQUEST", Util_format("Roll %d %d", out, -out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Roll PID");

    PID* pid;
    char data[64];
    double mv;
    double strafe_amount = Var_get("Strafe.Amount");
    double strafe_direction = Var_get("Strafe");
    double sp = strafe_direction * strafe_amount;

    Notify_filter(FILTER_MATCH, "UPDATED RollPID");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");
    Notify_filter(FILTER_MATCH, "UPDATED Strafe");
    Notify_filter(FILTER_MATCH, "UPDATED Strafe.Amount");

    pid = PID_new(sp, Var_get("RollPID.p"),
                      Var_get("RollPID.i"),
                      Var_get("RollPID.d"));

    mv = PID_start(pid, 0.0);
    dataOut(mv);
    while(true) {
        Notify_get(NULL, data);

        if(strcmp(data, "RollPID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("RollPID.p"),
                                Var_get("RollPID.i"),
                                Var_get("RollPID.d"));
            PID_resetIntegral(pid);
        } else if (strcmp(data, "IMU")) {
            // Do nothing, PID is updated every cycle regardless
            //mv = PID_update(pid, Var_get("SEA.Roll"));
        } else if (strcmp(data, "Strafe.Amount")) {
            strafe_amount = Var_get("Strafe.Amount");
            sp = strafe_direction * strafe_amount;
            PID_setSetPoint(pid, sp);
        } else { // Strafe
            strafe_direction = Var_get("Strafe");
            sp = strafe_direction * strafe_amount;
            PID_setSetPoint(pid, sp);
        }
        mv = PID_update(pid, Var_get("SEA.Roll"));
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
