
#include "seawolf.h"

static int thruster_max;

static void dataOut(double mv) {
    int out = Util_inRange(-thruster_max, (int) mv, thruster_max);
    int front = (int) out * 0.7;
    Notify_send("THRUSTER_REQUEST", Util_format("Alt %d %d %d", front, front, out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Altitude PID");

    PID* pid;
    char action[64], data[64];
    double mv;

    thruster_max = Var_get("ThrusterMax");

    Notify_filter(FILTER_MATCH, "UPDATED AltitudePID");
    Notify_filter(FILTER_MATCH, "UPDATED AltitudeHeading");
    Notify_filter(FILTER_MATCH, "UPDATED Altitude");

    pid = PID_new(Var_get("AltitudeHeading"),
                  Var_get("AltitudePID.p"),
                  Var_get("AltitudePID.i"),
                  Var_get("AltitudePID.d"));

    mv = PID_start(pid, Var_get("Altitude"));
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "AltitudePID") == 0) {
            PID_setCoefficients(pid,
                                Var_get("AltitudePID.p"),
                                Var_get("AltitudePID.i"),
                                Var_get("AltitudePID.d"));
            PID_resetIntegral(pid);
        } else if(strcmp(data, "AltitudeHeading") == 0) {
            PID_setSetPoint(pid, Var_get("AltitudeHeading"));
            mv = PID_start(pid, Var_get("Altitude"));
        } else {
            mv = PID_update(pid, Var_get("Altitude"));
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
