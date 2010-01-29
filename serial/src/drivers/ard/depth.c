
#include "seawolf.h"

#include <stdio.h>
#include <string.h>

void manage(SerialPort sp);

const char* app_name = "Serial : Depth";

void manage(SerialPort sp) {
    char buffer[64];
    float depth;

    /* Wait for good data */
    while(Serial_getByte(sp) != '\n');

    while(true) {
        Serial_getLine(sp, buffer);
        depth = atof(buffer);
        SeaSQL_setDepth(depth);
    }
}
