
#include "seawolf.h"

int main(void) {
printf("run1\n");
    Seawolf_loadConfig("seawolf.conf");
printf("run2\n");
    Seawolf_init("Remote control");
printf("run3\n");

    while(true) {
        SeaSQL_setDepth(0.0);
        Util_usleep(1.5);
    }

    Seawolf_close();
    return 0;
}
