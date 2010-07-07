
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Thruster Zero");

    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 0, 0));

    /* Turn off drivers */
    Var_set("PortX", 0);
    Var_set("PortY", 0);
    Var_set("StarX", 0);
    Var_set("StarY", 0);
    Var_set("Aft", 0);

    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", 0, 0, 0));
    Notify_send("THRUSTER_REQUEST", Util_format("Roll %d %d", 0, 0));
    Var_set("DepthHeading", 0.0);

    // Zero yaw pid
    float current_yaw = Var_get("SEA.Yaw");
    Var_set("Rot.Mode", 1.0);
    Var_set("Rot.Angular.Target", current_yaw);

    Var_set("Strafe", 0.0);

    Seawolf_close();
    return 0;
}
