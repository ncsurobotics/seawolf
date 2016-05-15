
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
    PT_PERIPHERAL = 4
} PeripheralType;

/* Cycle the DTR line on the given serial port */
static void cycleDTR(SerialPort sp) {
    Serial_setDTR(sp, 0);
    Util_usleep(0.1);
    Serial_setDTR(sp, 1);
    Util_usleep(0.1);
}

static int getPeripheralType(SerialPort sp) {
    //char id[32];
    int n;
    int bytes_received;
    int good_count;
    int error_count;

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
    
    /* IMU fingerprint failed, attempt Arduino */
    
    Serial_setBaud(sp, 9600);
    Serial_flush(sp);
    cycleDTR(sp);

    /*
    for(int i = 0; i < 4; i++) {
        if(ArdComm_getId(sp, id) != -1) {
            if(strcmp(id, "Depth") == 0) {
                return PT_DEPTH;
            } else if(strcmp(id, "Peripheral") == 0) {
                return PT_PERIPHERAL;
            } else {
                Logging_log(ERROR, Util_format("Received unknown ID '%s'", id));
            }
            break;
        } else {
            Util_usleep(0.5);
        }
    }
    */

    /* IMU fingerprint failed, attempt AVR */

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
