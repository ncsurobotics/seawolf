
#include "seawolf.h"

#include <stdio.h>
#include <string.h>

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
            depth = atof(buffer);
            Var_set("Depth", depth);
        }
    }
}
