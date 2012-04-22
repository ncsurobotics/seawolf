
#include "seawolf.h"

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

/* Air and water pressure constants. Varies by location (calibration recommended) */
#define PSI_PER_FOOT 0.4335
#define AIR_PRESSURE 14.23
#define DEPTH_ZERO -1.0

/* Ignore changes in depth greater than this. */
#define MAX_DEPTH_DELTA 2

const char* app_name = "Serial : Depth";
void manage(SerialPort sp);

int main(int argc, char** argv) {
    /* Configuration */
    Seawolf_loadConfig("../conf/seawolf.conf");

    /* Init libseawolf */
    Seawolf_init(app_name);

    /* Check arguments */
    if(argc != 2) {
        Logging_log(ERROR, Util_format("%s spawned with invalid argument count of %d", argv[0], argc));
        exit(1);
    }

    /* Attempt to open serial device */
    char* device = argv[1];
    SerialPort sp = Serial_open(device);

    /* Error opening device */
    if(sp == 0) {
        Logging_log(ERROR, Util_format("%s could not open device %s", argv[0], device));
        exit(1);
    }

    /* Set baud rate */
    Serial_setBaud(sp, 9600);

    /* Error checking done */
    Logging_log(INFO, Util_format("%s running successfully with device %s", argv[0], device));

    /* Complete handshake */
    while(ArdComm_handshake(sp) == -1) {
        Util_usleep(0.5);
    }

    /* Start app specific code */
    manage(sp);

    /* Close serial device and exit */
    Serial_closePort(sp);
    Seawolf_close();
    return 0;
}

void manage(SerialPort sp) {
    unsigned char data[2];
    unsigned short raw_depth;
    float voltage, psi, depth, last_good_depth;
    bool good_depth_seeded = false;

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

        if(good_depth_seeded && fabs(depth - last_good_depth) < MAX_DEPTH_DELTA) {
            last_good_depth = depth;
            Var_set("Depth", depth);
        } else if (!good_depth_seeded) {
            last_good_depth = depth;
            good_depth_seeded = true;
            Logging_log(INFO, Util_format("Seeded Depth: %f", last_good_depth));
        } else {
            Logging_log(ERROR, Util_format("Extraordinary depth value. (%.2f, 0x%04x)", depth, raw_depth));
        }
    }
}
