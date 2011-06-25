
#include "seawolf.h"

#include <stdio.h>
#include <string.h>

/* Air and water pressure constants. Varies by location (calibration recommended) */
#define PSI_PER_FOOT 0.4335
#define AIR_PRESSURE 14.23
#define DEPTH_ZERO -1.4

void manage(SerialPort sp);

const char* app_name = "Serial : Depth";

void manage(SerialPort sp) {
    unsigned char data[2];
    unsigned short raw_depth;
    float voltage, psi, depth;

    Serial_setBlocking(sp);

    while(true) {

        /* Wait for good data */
        while(Serial_getByte(sp) != 0x01);

        Serial_get(sp, data, 2);

        /* Compute depth */
        raw_depth = (data[0] * 256) + data[1];
        voltage = raw_depth * (5.0/1024.0);
        psi = ((voltage - 0.5) * 100) / 4.0;  
        depth = (psi - AIR_PRESSURE) / PSI_PER_FOOT - DEPTH_ZERO;
        //if (depth <= 0.0) depth=0.0;

        Var_set("Depth", depth);
    }
}
