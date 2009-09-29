
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Test1");
    
    char action[64], data[64];

    Notify_filter(FILTER_MATCH, "HELLO world");
    Notify_get(action, data);
    Logging_log(DEBUG, Util_format("%s === %s", action, data));

    //Notify_filter(0, NULL);
    //Notify_filter(FILTER_MATCH, "GOODBYE world");
    Notify_get(action, data);
    Logging_log(DEBUG, Util_format("%s === %s", action, data));

    Seawolf_close();
    return 0;
}
