
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Thruster Controller");

    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 0, 0));

    /* Turn off drivers */
    Var_set("PortX", 0);
    Var_set("PortY", 0);
    Var_set("StarX", 0);
    Var_set("StarY", 0);
    Var_set("Aft", 0);

    // Zero yaw pid
    float current_yaw = Var_get("SEA.Yaw");
    Var_set("Rot.Mode", 1.0);
    Var_set("Rot.Angular.Target", current_yaw);

    Seawolf_close();
    return 0;
}
