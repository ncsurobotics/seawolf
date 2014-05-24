
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Thruster Zero");

    /* Disable forward momentum */
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %.4f", 0.0));

    /* Disable PIDs */
    Var_set("DepthPID.Paused", 1.0);
    Var_set("PitchPID.Paused", 1.0);
    Var_set("YawPID.Paused", 1.0);

    /* Turn off drivers */
    Var_set("Port", 0);
    Var_set("Star", 0);
    Var_set("Bow", 0);
    Var_set("Stern", 0);
    Var_set("StrafeT", 0);
    Var_set("StrafeB", 0);

    Seawolf_close();
    return 0;
}
