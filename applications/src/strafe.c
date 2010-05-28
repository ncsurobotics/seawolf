
#include "seawolf.h"
#include "seawolf3.h"

// Seawolf_fork() ?

static void strafe_right(void) {
    Var_set("Rot.Mode", ROT_MODE_ANGULAR);
    Var_set("Rot.Angular.Target", Var_get("IMU.Yaw"));
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", 30, -20, 15));
}

static void strafe_left(void) {
    Var_set("Rot.Mode", ROT_MODE_ANGULAR);
    Var_set("Rot.Angular.Target", Var_get("IMU.Yaw"));
    Notify_send("THRUSTER_REQUEST", Util_format("Depth %d %d %d", -20, 30, 15));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Strafe");

    strafe_right();
    
    Seawolf_close();
    return 0;
}
