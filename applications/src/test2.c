
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Test1");

    Notify_send("HELLO", "world");
    Notify_send("GOODBYE", "world");

    Seawolf_close();
    return 0;
}
