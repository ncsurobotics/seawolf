
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Tracker Proxy");

    char action[16], data[64];
    int source = (int) Var_get("SetPointSource");

    Notify_filter(FILTER_MATCH, "UPDATED SetPointSource");
    Notify_filter(FILTER_MATCH, "UPDATED SetPointVision");
    Notify_filter(FILTER_MATCH, "UPDATED SetPointAcoustics");

    while(true) {
        Notify_get(action, data);
        if(strcmp(data, "SetPointSource") == 0) {
            Logging_log(DEBUG, "New source");
            source = (int) Var_get("SetPointSource");
            Var_set("SetPoint.Theta", 0.0);
            Var_set("SetPoint.Phi", 0.0);
            Var_set("SetPoint.Rho", 0.0);
        } else {
            if(source == SETPOINT_SOURCE_VISION && strcmp(data, "SetPointVision") == 0) {
                Var_set("SetPoint.Theta", Var_get("SetPointVision.Theta"));
                Var_set("SetPoint.Phi", Var_get("SetPointVision.Phi"));
                Var_set("SetPoint.Rho", Var_get("SetPointVision.Rho"));
            } else if(source == SETPOINT_SOURCE_ACOUSTICS && strcmp(data, "SetPointAcoustics") == 0) {
                Var_set("SetPoint.Theta", Var_get("SetPointAcoustics.Theta"));
                Var_set("SetPoint.Phi", Var_get("SetPointAcoustics.Phi"));
                Var_set("SetPoint.Rho", Var_get("SetPointAcoustics.Rho"));
            } else if(source == SETPOINT_SOURCE_OVERRIDE && strcmp(data, "SetPointOverride") == 0) {
                Var_set("SetPoint.Theta", Var_get("SetPointOverride.Theta"));
                Var_set("SetPoint.Phi", Var_get("SetPointOverride.Phi"));
                Var_set("SetPoint.Rho", Var_get("SetPointOverride.Rho"));
            }
            Notify_send("UPDATED", "SetPoint");
        }
    }

    Seawolf_close();
    return 0;
}
