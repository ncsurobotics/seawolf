
#include "seawolf.h"

int main(int argc, char** argv) {
    if(argc != 3) {
        printf("Usage: %s <variable name> <variable value>\n", argv[0]);
        return 0;
    }

    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Set Variable");

    Var_set(argv[1], atof(argv[2]));

    Seawolf_close();
    return 0;
}
