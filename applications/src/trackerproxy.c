
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Tracker Proxy");

    char action[16], data[64];
    int source = (int) SeaSQL_getSetPointSource();

    Notify_filter(FILTER_MATCH, "UPDATED SetPointSource");
    Notify_filter(FILTER_MATCH, "UPDATED SetPointVision");
    Notify_filter(FILTER_MATCH, "UPDATED SetPointAcoustics");

    while(true) {
        Notify_get(action, data);
        if(strcmp(data, "SetPointSource") == 0) {
            Logging_log(DEBUG, "New source");
            source = (int) SeaSQL_getSetPointSource();
            SeaSQL_setSetPoint_Theta(0.0);
            SeaSQL_setSetPoint_Phi(0.0);
            SeaSQL_setSetPoint_Rho(0.0);
        } else {
            if(source == SETPOINT_SOURCE_VISION && strcmp(data, "SetPointVision") == 0) {
                SeaSQL_setSetPoint_Theta(SeaSQL_getSetPointVision_Theta());
                SeaSQL_setSetPoint_Phi(SeaSQL_getSetPointVision_Phi());
                SeaSQL_setSetPoint_Rho(SeaSQL_getSetPointVision_Rho());
            } else if(source == SETPOINT_SOURCE_ACOUSTICS && strcmp(data, "SetPointAcoustics") == 0) {
                SeaSQL_setSetPoint_Theta(SeaSQL_getSetPointAcoustics_Theta());
                SeaSQL_setSetPoint_Phi(SeaSQL_getSetPointAcoustics_Phi());
                SeaSQL_setSetPoint_Rho(SeaSQL_getSetPointAcoustics_Rho());
            } else if(source == SETPOINT_SOURCE_OVERRIDE && strcmp(data, "SetPointOverride") == 0) {
                SeaSQL_setSetPoint_Theta(SeaSQL_getSetPointOverride_Theta());
                SeaSQL_setSetPoint_Phi(SeaSQL_getSetPointOverride_Phi());
                SeaSQL_setSetPoint_Rho(SeaSQL_getSetPointOverride_Rho());
            }
            Notify_send("UPDATED", "SetPoint");
        }
    }

    Seawolf_close();
    return 0;
}
