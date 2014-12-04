
#include "seawolf.h"

int main(int argc, char** argv) {
    if(!(argc == 3 || argc == 4)) {
        printf("Usage: %s <depth|pitch|roll|yaw> <p|i|d> [<value>]\n", argv[0]);
        exit(0);
    }

    Seawolf_loadConfig("../conf/seawolf.conf");
    Var_setAutoNotify(false);
    Seawolf_init("PID Adjuster");

    char* sensor = argv[1];
    char var = argv[2][0];
    float value = 0;

    enum {
        SET,
        GET
    } action = GET;

    if (argc == 4) {
        value = atof(argv[3]);
        action = SET;
    }

    if (strcmp(sensor, "depth") == 0) {
        if(var == 'p') {
            if(action == SET) {
                Var_set("DepthPID.p", value);
            } else {
                printf("%.2f\n", Var_get("DepthPID.p"));
            }
        } else if(var == 'i') {
            if(action == SET) {
                Var_set("DepthPID.i", value);
            } else {
                printf("%.2f\n", Var_get("DepthPID.i"));
            }
        } else if(var == 'd') {
            if(action == SET) {
                Var_set("DepthPID.d", value);
            } else {
                printf("%.2f\n", Var_get("DepthPID.d"));
            }
        }
        Notify_send("UPDATED", "DepthPID.Coefficients");
    } else if(strcmp(sensor, "yaw") == 0) {
        if(var == 'p') {
            if(action == SET) {
                Var_set("YawPID.p", value);
            } else {
                printf("%.2f\n", Var_get("YawPID.p"));
            }
        } else if(var == 'i') {
            if(action == SET) {
                Var_set("YawPID.i", value);
            } else {
                printf("%.2f\n", Var_get("YawPID.i"));
            }
        } else if(var == 'd') {
            if(action == SET) {
                Var_set("YawPID.d", value);
            } else {
                printf("%.2f\n", Var_get("YawPID.d"));
            }
        }
        Notify_send("UPDATED", "YawPID.Coefficients");
    } else if(strcmp(sensor, "pitch") == 0) {
        if(var == 'p') {
            if(action == SET) {
                Var_set("PitchPID.p", value);
            } else {
                printf("%.2f\n", Var_get("PitchPID.p"));
            }
        } else if(var == 'i') {
            if(action == SET) {
                Var_set("PitchPID.i", value);
            } else {
                printf("%.2f\n", Var_get("PitchPID.i"));
            }
        } else if(var == 'd') {
            if(action == SET) {
                Var_set("PitchPID.d", value);
            } else {
                printf("%.2f\n", Var_get("PitchPID.d"));
            }
        }
        Notify_send("UPDATED", "PitchPID.Coefficients");
    } else if(strcmp(sensor, "roll") == 0) {
        if(var == 'p') {
            if(action == SET) {
                Var_set("RollPID.p", value);
            } else {
                printf("%.2f\n", Var_get("RollPID.p"));
            }
        } else if(var == 'i') {
            if(action == SET) {
                Var_set("RollPID.i", value);
            } else {
                printf("%.2f\n", Var_get("RollPID.i"));
            }
        } else if(var == 'd') {
            if(action == SET) {
                Var_set("RollPID.d", value);
            } else {
                printf("%.2f\n", Var_get("RollPID.d"));
            }
        }
        Notify_send("UPDATED", "RollPID.Coefficients");
    } else {
        printf("Invalid arguments\n");
    }

    Seawolf_close();
    return 0;
}
