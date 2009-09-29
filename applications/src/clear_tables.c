
#include "seawolf.h"

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    SeaSQL_init();
    SeaSQL_clearVariables();
    SeaSQL_execute("DELETE FROM log;");
    SeaSQL_close();
    return 0;
}
