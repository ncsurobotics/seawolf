
#include "seawolf.h"

int main(int argc, char** argv) {
    if(!(argc == 3 || argc == 4)) {
        printf("Usage: %s <depth|alt|roll|pitch|yaw> <p|i|d> [<value>]\n", argv[0]);
        exit(0);
    }

    Seawolf_loadConfig("../conf/seawolf.conf");
    SeaSQL_setAutoNotify(false);
    Seawolf_init("PID Adjuster");

    char* sensor = argv[1];
    char var = argv[2][0];
    float value = 0;

    enum {
        SET,
        GET
    } action = GET;
    
    if(argc == 4) {
        value = atof(argv[3]);
        action = SET;
    }

    if(strcmp(sensor, "depth") == 0) {
        if(var == 'p') {
            if(action == SET) {
                SeaSQL_setDepthPID_p(value);
            } else {
                printf("%.2f\n", SeaSQL_getDepthPID_p());
            }
        } else if(var == 'i') {
            if(action == SET) {
                SeaSQL_setDepthPID_i(value);
            } else {
                printf("%.2f\n", SeaSQL_getDepthPID_i());
            }
        } else if(var == 'd') {
            if(action == SET) {
                SeaSQL_setDepthPID_d(value);
            } else {
                printf("%.2f\n", SeaSQL_getDepthPID_d());
            }
        }
        Notify_send("UPDATED", "DepthPID");
    } else if(strcmp(sensor, "alt") == 0) {
        if(var == 'p') {
            if(action == SET) {
                SeaSQL_setAltitudePID_p(value);
            } else {
                printf("%.2f\n", SeaSQL_getAltitudePID_p());
            }
        } else if(var == 'i') {
            if(action == SET) {
                SeaSQL_setAltitudePID_i(value);
            } else {
                printf("%.2f\n", SeaSQL_getAltitudePID_i());
            }
        } else if(var == 'd') {
            if(action == SET) {
                SeaSQL_setAltitudePID_d(value);
            } else {
                printf("%.2f\n", SeaSQL_getAltitudePID_d());
            }
        }
        Notify_send("UPDATED", "AltitudePID");
    } else if(strcmp(sensor, "yaw") == 0) {
        if(var == 'p') {
            if(action == SET) {
                SeaSQL_setYawPID_p(value);
            } else {
                printf("%.2f\n", SeaSQL_getYawPID_p());
            }
        } else if(var == 'i') {
            if(action == SET) {
                SeaSQL_setYawPID_i(value);
            } else {
                printf("%.2f\n", SeaSQL_getYawPID_i());
            }
        } else if(var == 'd') {
            if(action == SET) {
                SeaSQL_setYawPID_d(value);
            } else {
                printf("%.2f\n", SeaSQL_getYawPID_d());
            }
        }
        Notify_send("UPDATED", "YawPID");
    } else if(strcmp(sensor, "roll") == 0) {
        if(var == 'p') {
            if(action == SET) {
                SeaSQL_setRollPID_p(value);
            } else {
                printf("%.2f\n", SeaSQL_getRollPID_p());
            }
        } else if(var == 'i') {
            if(action == SET) {
                SeaSQL_setRollPID_i(value);
            } else {
                printf("%.2f\n", SeaSQL_getRollPID_i());
            }
        } else if(var == 'd') {
            if(action == SET) {
                SeaSQL_setRollPID_d(value);
            } else {
                printf("%.2f\n", SeaSQL_getRollPID_d());
            }
        }
        Notify_send("UPDATED", "RollPID");
     } else if(strcmp(sensor, "pitch") == 0) {
        if(var == 'p') {
            if(action == SET) {
                SeaSQL_setPitchPID_p(value);
            } else {
                printf("%.2f\n", SeaSQL_getPitchPID_p());
            }
        } else if(var == 'i') {
            if(action == SET) {
                SeaSQL_setPitchPID_i(value);
            } else {
                printf("%.2f\n", SeaSQL_getPitchPID_i());
            }
        } else if(var == 'd') {
            if(action == SET) {
                SeaSQL_setPitchPID_d(value);
            } else {
                printf("%.2f\n", SeaSQL_getPitchPID_d());
            }
        }
        Notify_send("UPDATED", "PitchPID");
    } else {
        printf("Invalid arguments\n");
    }

    Seawolf_close();
    return 0;
}
