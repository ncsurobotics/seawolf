
#include "seawolf.h"

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stropts.h>
#include <unistd.h>

/* Device types */
typedef enum{PT_UNMANAGED,
             PT_IMU} PeripheralType;

/* Represents and open serial port */
struct comm_device {
    const char* device;
    SerialPort sp;
    PeripheralType peripheral_type;
};

/* Represents a driver */
struct comm_assignment {
    const char* bin;
    bool started;
};

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
    /* char id[32]; */
    int n;

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

    /* Fallback to Serial Device, get ID */
    Logging_log(ERROR, "No Microcontrollers set up in the serial app!!!!!!!!!!!!!!!");
    // When you remove this block of code, please remove "char id[32]" at the beginning of the function, and the cycleDTR function.
    /*
    Serial_setBaud(sp, 9600);
    Serial_flush(sp);
    cycleDTR(sp);

    for(int i = 0; i < 3; i++) {
        if(ArdComm_getId(sp, id) != -1) {
            if(strcmp(id, "ThrusterBoard") == 0) {
                return PT_THRUSTER_BOARD;
            } else {
                Logging_log(ERROR, Util_format("Received unknown ID '%s'", id));
            }
            break;
        } else {
            Util_usleep(0.5);
        }
    }
    */

    /* Fingerprinting failed */
    Logging_log(DEBUG, "Could not ID");
    return -1;
}

int main(void) {
    /* Configuration */
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Serial");

    /* Peripheral type */
    PeripheralType pt;

    /* Device/app mappings */
    struct comm_device device_pool[] = {{"/dev/ttyUSB0", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB1", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB2", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB3", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB4", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB5", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB6", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB7", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB8", 0, PT_UNMANAGED},
                                        {"/dev/ttyUSB9", 0, PT_UNMANAGED}};
    const int device_count = sizeof(device_pool) / sizeof(struct comm_device);

    /* App to executable mappings */
    struct comm_assignment app_pool[] = {[PT_IMU]            = {"./bin/imu",              false}};
    const int app_count = sizeof(app_pool) / sizeof(struct comm_assignment);

    int i = 0;
    int apps_waiting = app_count;
    int unassigned_ports = 10;

    /* Open serial ports */
    for(i = 0; i < device_count; i++) {
        /* Open serial device */
        device_pool[i].sp = Serial_open(device_pool[i].device);
        if(device_pool[i].sp != -1) {
            Logging_log(DEBUG, Util_format("Opening %s", device_pool[i].device));
            Serial_setBlocking(device_pool[i].sp);
        } else {
            unassigned_ports--;
        }
    }

    i = 0;
    while(apps_waiting > 0 && unassigned_ports > 0) {
        if(device_pool[i].peripheral_type == PT_UNMANAGED && device_pool[i].sp != -1) {
            /* Serial port is now open, attempt to fingerprint */
            Logging_log(DEBUG, Util_format("Fingerprinting %s", device_pool[i].device));
            if(device_pool[i].sp != -1 && (pt = getPeripheralType(device_pool[i].sp)) != -1) {
                Logging_log(DEBUG, Util_format("Serial port ready %s", device_pool[i].device));

                /* Close port and copy device */
                Serial_closePort(device_pool[i].sp);
                unassigned_ports--;

                if(app_pool[pt].started == false) {
                    /* Fork and execute subprocess in child */
                    if(fork() == 0) {
                        Logging_log(INFO, Util_format("Connected to device on %s with identifier %d. Spawning %s",
                                                      device_pool[i].device, pt, app_pool[pt].bin));
                        execl(app_pool[pt].bin, app_pool[pt].bin, device_pool[i].device, NULL);
                    }

                    /* Decrease number of waiting apps */
                    apps_waiting -= 1;

                    /* Set the device as attached, and the application as running */
                    device_pool[i].peripheral_type = pt;
                    app_pool[pt].started = true;
                } else {
                    Logging_log(ERROR, Util_format("Error, attempt to connect %s twice", device_pool[i].device));
                }
            }
        }

        i = (i + 1) % device_count;
        if(i == 0) {
            /* Sleep 500 milliseconds after exhausting device list */
            Util_usleep(0.5);
        }
    }

    /* Finished identifying all devices */
    if(apps_waiting > 0) {
        Logging_log(WARNING, "All available devices handled but applications remain unhandled");
    } else {
        Logging_log(INFO, "Identified and properly handled all devices");
    }

    /* Send notification of completion */
    Notify_send("COMPLETED", "Serial identification");

    while(true) {
        Util_usleep(5.0);
    }

    Seawolf_close();
    return 0;
}
