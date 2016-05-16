
#include "seawolf.h"

#include <glob.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stropts.h>
#include <unistd.h>

/* Device types */
typedef enum{
    PT_UNMANAGED = 0,
    PT_IMU = 1,
    PT_AVR = 2,
    PT_DEPTH = 3,
    PT_PERIPHERAL = 4,
    PT_PNEUMATICS = 5
} PeripheralType;

/* Cycle the DTR line on the given serial port */
/*
static void cycleDTR(SerialPort sp) {
    Serial_setDTR(sp, 0);
    Util_usleep(0.1);
    Serial_setDTR(sp, 1);
    Util_usleep(0.1);
}
*/

static int getPeripheralType(SerialPort sp) {
    printf("going\n");
    //char id[32];
    int n;
    int bytes_received;
    int good_count;
    int error_count;
    char ret_string[128];

    /* Set to IMU's baud rate */
    Serial_setBaud(sp, 38400);
    Serial_flush(sp);

    /* Probe IMU by sending version number command */
    n = Serial_sendByte(sp, 0xF0);
    if(n == -1) {
        Logging_log(ERROR, "Unable to send data");
        return -1;
    }

    Util_usleep(0.1);
    if(Serial_available(sp) > 0) {
        n = Serial_getByte(sp);
        if(n == 0xf0) {
            /* Received IMU response */
            Logging_log(DEBUG, "IMU Found");
            Serial_flush(sp);
            return PT_IMU;
        }
    }
    
    /* IMU fingerprint failed, attempt Pneumatics */
    Serial_setBaud(sp, 9600);
    n = Serial_sendByte(sp, 'r');//reset pneumatics
    Serial_flush(sp);
    //cycleDTR(sp);

    /* Poke Pneumatics with predefined command */
    n = Serial_sendByte(sp, 0xFE);
    if(n == -1) {
        Logging_log(ERROR, "Unable to send data");
        return -1;
    }

    //give a little time for arduino to respond
    Util_usleep(.1);

    //if any response has been obtained, check if {ID|PNEUMATICS}\r\n
    n = Serial_available(sp);
    if ((n > 0) && (n < 128)) {
        Serial_get(sp,ret_string,n);
        if (strncmp(ret_string, "{ID|Pneumatics}\r\n",n)==0) {
            /* Received PNEUMATICS response */
            Logging_log(DEBUG, "PNEUMATICS Found");
            Serial_flush(sp);
            return PT_PNEUMATICS;
        }
    }
    


    /* PNEUMATICS fingerprint failed, attempt AVR */

    /* Set to AVR baud rate */
    Serial_setBaud(sp, 57600);

    /* Send reset sequence */
    for(int i = 0; i < 5; i++) {
        n = Serial_sendByte(sp, 'r');

        if(n == -1) {
            Logging_log(ERROR, "Unable to send data");
            return -1;
        }
    }

    /* Number of bytes received */
    bytes_received = 0;

    /* Number of consecutive 0xff bytes received */
    good_count = 0;

    /* Number of consecutive failures to get a byte */
    error_count = 0;

    do {
        if(Serial_available(sp) > 0) {
            n = Serial_getByte(sp);
            bytes_received++;

            error_count = 0;

            if(n == 0xff) {
                good_count++;
            } else {
                good_count = 0;
            }

            if(good_count == 16) {
                return PT_AVR;
            }
        } else {
            Util_usleep(0.1);
            error_count++;
        }
    } while(error_count < 5 && bytes_received < 512);

    /* Give up after 5 attempts to receive data or 1024 bytes received total */

    return -1;
}

int main(void) {
    /* Configuration */
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Serial");

    const char* port_path;
    SerialPort sp;
    PeripheralType pt;

    /* Glob type for serial interface search */
    glob_t globbuff;

    /* App to executable mappings */
    char* drivers[] = {
        [PT_IMU] = "./bin/imu",
        [PT_AVR] = "./bin/avr",
        [PT_DEPTH] = "./bin/depth",
        [PT_PERIPHERAL] = "./bin/peripheral",
        [PT_PNEUMATICS] = "./bin/pneumatics"
    };

    /* Find serial ports */
    glob("/dev/ttyUSB*", 0, NULL, &globbuff);
    //glob("/dev/ttyS*", GLOB_APPEND, NULL, &globbuff);

    for(int i = 0; i < globbuff.gl_pathc; i++) {
        port_path = globbuff.gl_pathv[i];
        sp = Serial_open(port_path);

        if(sp == -1) {
            Logging_log(ERROR, Util_format("Error opening %s: %s.", port_path, strerror(errno)));
            continue;
        }

        pt = getPeripheralType(sp);
        Serial_closePort(sp);

        if(pt == -1) {
            Logging_log(ERROR, Util_format("Unable to identify device on %s", port_path));
        } else {
            Logging_log(INFO, Util_format("Identified device on %s. Spawning %s", port_path, drivers[pt]));

            /* Fork and execute subprocess in child */
            if(fork() == 0) {
                execl(drivers[pt], drivers[pt], port_path, NULL);
                fprintf(stderr, "Unable to spawn application (%s)\n", drivers[pt]);
                _exit(1);
            }
        }
    }

    /* Send notification of completion */
    Notify_send("COMPLETED", "Serial identification");

    while(true) {
        Util_usleep(5.0);
    }

    Seawolf_close();
    return 0;
}
