
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Mission Controller");

    //Notify_filter(FILTER_ACTION, "MISSIONTRIGGER");
    //Notify_get(NULL, NULL);

    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 0, 0));
    //Var_set("Rot.Angular.Target", 50.0);
    //Var_set("DepthHeading", 10.0);

    // Go Forward
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 20, 20));

    // Zero yaw pid
    float current_yaw = Var_get("SEA.Yaw");
    Var_set("Rot.Mode", 1.0);
    Var_set("Rot.Angular.Target", current_yaw);

    Seawolf_close();
    return 0;
}
