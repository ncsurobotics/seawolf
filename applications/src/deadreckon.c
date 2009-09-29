
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Dead reckon");
    
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 0, 0));
    SeaSQL_setYawHeading(SeaSQL_getSEA_Yaw());
    SeaSQL_setDepthHeading(0.0);
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", 40, 40));
    
    Seawolf_close();
    return 0;
}
