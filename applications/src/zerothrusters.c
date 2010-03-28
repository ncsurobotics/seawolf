
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Thruster Controller");

    /* Turn off drivers */
    Var_set("PortX", 0);
    Var_set("PortY", 0);
    Var_set("StarX", 0);
    Var_set("StarY", 0);
    Var_set("Aft", 0);

    Seawolf_close();
    return 0;
}
