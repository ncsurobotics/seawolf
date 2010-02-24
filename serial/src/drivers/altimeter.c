
#include "seawolf.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>

#define MAX_VALID_ALT 25
#define MAX_VALID_DELTA 8

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Serial::Altimeter");

    /* Buffers */
    char b1[256], b2[256], b3[256];
    char* device_real = argv[1];
    float last_alt = -1;
    float alt;
    SerialPort sp = Serial_open(device_real);

    /* Initialize serial port */
    Serial_setBaud(sp, 4800);
    Serial_setBlocking(sp);
    Util_usleep(1.5);
    tcflush(sp, TCIFLUSH); /* Zero input buffers */
    
    /* Clear */
    Serial_getLine(sp, b1);

    while(true) {
        Serial_getLine(sp, b1);

        if(b1[0] != '$') {
            /* Simple sanity check */
            Logging_log(ERROR, "Inconsistent message from altimeter!");
            continue;
        }

        if(b1[4] != 'B') {
            /* Not 'height' line */
            continue;
        }

        Util_split(b1, ',', b2, b3);
        Util_split(b3, ',', b1, b2);

        alt = atof(b1);

        /* Initialize */
        if(last_alt == -1) {
            last_alt = alt;
        }
        
        if(alt > MAX_VALID_ALT) {
            Logging_log(WARNING, Util_format("Ignoring invalid altitude value of %.2f feet", alt));
            continue;
        }

        if(fabs(alt - last_alt) > MAX_VALID_DELTA) {
            Logging_log(WARNING, Util_format("Ignoring value of %.2f feet giving excessive delta of %.2f feet", alt, alt - last_alt));
            continue;
        }

        /* Valid value, store it */
        last_alt = alt;
        Var_set("Altitude", alt);
    }

    Serial_closePort(sp);
    Seawolf_close();
    return 0;
}
