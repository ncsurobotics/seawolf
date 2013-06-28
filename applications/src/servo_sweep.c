
#include "seawolf.h"

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Servo Test");

    int i;
    while(1) {
        for(i=0; i < 180; i+=1) {
            Var_set("Servo.0", i);
            printf("%d\n", i);
            Util_usleep(0.01);
        }
        for(i=180; i>=1; i-=1) {
            Var_set("Servo.0", i);
            printf("%d\n", i);
            Util_usleep(0.01);
        }
    }

    Seawolf_close();
    return 0;
}
