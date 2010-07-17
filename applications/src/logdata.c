
#include "seawolf.h"

int main(int argc, char** argv) {
    if(argc != 3) {
        fprintf(stderr, "Usage: %s <variable> <file>\n", argv[0]);
        exit(1);
    }

    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("DataLogger");

    char* var = argv[1];
    FILE* dump_file = fopen(argv[2], "w");
    Timer* time = Timer_new();

    Var_get(var);

    Notify_filter(FILTER_MATCH, Util_format("UPDATED %s", var));

    while(true) {
        Notify_get(NULL, NULL);
        fprintf(dump_file, "%5.2f %.2f\n", Timer_getTotal(time), Var_get(var));
    }

    fclose(dump_file);
    Seawolf_close();
    return 0;
}
