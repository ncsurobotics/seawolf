
#include "seawolf.h"

#include <stdio.h>
#include <string.h>

#define DEPTH_ZERO (0.57)

void manage(SerialPort sp);

const char* app_name = "Serial : Depth";

void manage(SerialPort sp) {
    char buffer[64];
    float depth;

    Serial_setBlocking(sp);

    /* Wait for good data */
    while(Serial_getByte(sp) != '\n');

    while(true) {
        if (Serial_getLine(sp, buffer) == -1) {
            printf("Error reading serial!\n");
            Util_usleep(0.2);
        } else {
            depth = atof(buffer)-DEPTH_ZERO;
            if (depth <= 0.0) depth=0.0;
            Var_set("Depth", depth);
        }
    }
}
