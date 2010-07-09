
#include "seawolf.h"

int main(int argc, char** argv) {
    if(argc != 3) {
        printf("Usage: %s <action> <data>\n", argv[0]);
        return 0;
    }

    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Send notification");

    Notify_send(argv[1], argv[2]);

    Seawolf_close();
    return 0;
}
