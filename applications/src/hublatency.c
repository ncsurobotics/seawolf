
#include "seawolf.h"

#define PRINT_RATE 50.0
#define PING_RATE 10000.0

static void ping(int n, int count) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init(Util_format("Pinger %d", n));
    
    Timer* timer = Timer_new();
    static char action[16], data[16];
    char* num = strdup(Util_format("%d", n));
    int i = n;

    Notify_filter(FILTER_MATCH, Util_format("PING %d", n));
    Util_usleep(1.0);

    const int rate = count * (PING_RATE / PRINT_RATE);

    while(true) {
        Notify_send("PING", Util_format("%d", n));
        Notify_get(action, data);

        assert(strcmp(action, "PING") == 0);
        assert(strcmp(data, num) == 0);

        if(i == (rate / count) * n) {
            printf("%3d: %.4f\n", n, (Timer_getDelta(timer) / rate) - (1 / PING_RATE));
        }

        i = (i + 1) % rate;
        Util_usleep(1 / PING_RATE);
    }
}

static void usage(const char* pname) {
    printf("usage: %s [-h] [-c <count>]\n", pname);
    exit(1);
}

int main(int argc, char** argv) {
    int count = 1;

    /* Parse options */
    for(int i = 1; i < argc; i++) {
        if(strcmp(argv[i], "-h") == 0) {
            usage(argv[0]);
        } else if((argc - i) > 1) {
            if(strcmp(argv[i], "-c") == 0) {
                count = atoi(argv[++i]);
            } else {
                usage(argv[0]);
            }
        } else {
            usage(argv[0]);
        }
    }

    for(int i = 1; i < count; i++) {
        if(fork() == 0) {
            ping(i, count);
        }
    }
    ping(0, count);

    return 0;
}
