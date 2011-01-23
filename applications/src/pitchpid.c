
#include "seawolf.h"
#include "seawolf3.h"

static void dataOut(double mv) {
    float out = Util_inRange(-1.0, mv, 1.0);
    Notify_send("THRUSTER_REQUEST", Util_format("Pitch %.4f", out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Pitch PID");

    PID* pid;
    char data[64];
    double mv;
    bool paused = Var_get("PitchPID.Paused");

    Notify_filter(FILTER_MATCH, "UPDATED PitchPID.Coefficients");
    Notify_filter(FILTER_MATCH, "UPDATED PitchPID.SetPoint");
    Notify_filter(FILTER_MATCH, "UPDATED PitchPID.Paused");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");

    pid = PID_new(Var_get("PitchPID.Heading"),
                  Var_get("PitchPID.p"),
                  Var_get("PitchPID.i"),
                  Var_get("PitchPID.d"));
    dataOut(0.0);

    while(true) {
        Notify_get(NULL, data);

        double pitch = Var_get("SEA.Pitch");
        if(strcmp(data, "PitchPID.Coefficients") == 0) {
            PID_setCoefficients(pid,
                                Var_get("PitchPID.p"),
                                Var_get("PitchPID.i"),
                                Var_get("PitchPID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "PitchPID.SetPoint") == 0) {
            PID_setSetPoint(pid, Var_get("PitchPID.SetPoint"));
            mv = PID_update(pid, pitch);
            if(paused) {
                Var_set("PitchPID.Paused", 0.0);
            }
        } else if(strcmp(data, "PitchPID.Paused") == 0) {
            bool p = Var_get("PitchPID.Paused");
            if(p == paused) {
                continue;
            }

            paused = p;
            if(paused) {
                dataOut(0.0);
                Notify_send("PIDPAUSED", "Pitch");
            }
        } else if(paused == true) {
            mv = PID_update(pid, pitch);
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
