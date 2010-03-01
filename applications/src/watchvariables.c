
#include "seawolf.h"

int main(int argc, char** argv) {
    int* lengths;
    
    if(argc < 2) {
        printf("Usage: %s <variable name> ...\n", argv[0]);
        return 0;
    }

    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Watch Variables");

    lengths = malloc(sizeof(int) * (argc - 1));
    for(int i = 1; i < argc; i++) {
        lengths[i-1] = strlen(argv[i]);
    }

    for(int m = 0; ; m = (m + 1) % 10) {
        if(m == 0) {
            printf("\n");
            for(int i = 1; i < argc; i++) {
                printf("%*s ", lengths[i-1], argv[i]);
            }
            printf("\n");
        }

        for(int i = 1; i < argc; i++) {
            printf("%*.2f ", lengths[i-1], Var_get(argv[i]));
        }
        printf("\n");

        Util_usleep(0.01);
    }

    free(lengths);
    Seawolf_close();
    return 0;
}
