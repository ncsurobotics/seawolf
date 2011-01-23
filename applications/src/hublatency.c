
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Hub Latency");
    
    Timer* timer = Timer_new();

    Notify_filter(FILTER_MATCH, "PING PING");
    
    while(true) {
        Notify_send("PING", "PING");
        Notify_get(NULL, NULL);
        printf("Ping: %.4f\n", Timer_getDelta(timer));
    }

    return 0;
}
