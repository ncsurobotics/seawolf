
#include "seawolf.h"

static void dataOut(double mv) {
    int out = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    int front = (int) out * 0.7;
    Notify_send("THRUSTER_REQUEST", Util_format("Alt %d %d %d", front, front, out));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Altitude PID");

    PID* pid;
    char action[64], data[64];
    double mv;

    Notify_filter(FILTER_MATCH, "UPDATED AltitudePID");
    Notify_filter(FILTER_MATCH, "UPDATED AltitudeHeading");
    Notify_filter(FILTER_MATCH, "UPDATED Altitude");

    pid = PID_new(SeaSQL_getAltitudeHeading(),
                  SeaSQL_getAltitudePID_p(),
                  SeaSQL_getAltitudePID_i(),
                  SeaSQL_getAltitudePID_d());

    mv = PID_start(pid, SeaSQL_getAltitude());
    dataOut(mv);
    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "AltitudePID") == 0) {
            PID_setCoefficients(pid,
                                SeaSQL_getAltitudePID_p(),
                                SeaSQL_getAltitudePID_i(),
                                SeaSQL_getAltitudePID_d());
            PID_resetIntegral(pid);
        } else if(strcmp(data, "AltitudeHeading") == 0) {
            PID_setSetPoint(pid, SeaSQL_getAltitudeHeading());
            mv = PID_start(pid, SeaSQL_getAltitude());
        } else {
            mv = PID_update(pid, SeaSQL_getAltitude());
        }
        
        dataOut(mv);
    }

    Seawolf_close();
    return 0;
}
