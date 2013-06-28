
#include "seawolf.h"

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

const char* app_name = "Serial : Peripheral";
void manage(SerialPort sp);
void update_servo(SerialPort sp, unsigned char servo, float value);

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

void update_servo(SerialPort sp, unsigned char servo, float value) {
    unsigned char command[2];
    if(servo != 0 && servo != 1) {
        return;
    }
    command[0] = servo;
    command[1] = (unsigned char) Util_inRange(0, value, 255);
    Serial_send(sp, command, 2);
}

void manage(SerialPort sp) {
    Var_subscribe("Servo.0");
    Var_subscribe("Servo.1");

    while(true) {
        Var_sync();

        if(Var_poked("Servo.0")) {
            update_servo(sp, 0, Var_get("Servo.0"));
        }
        if(Var_poked("Servo.1")) {
            update_servo(sp, 1, Var_get("Servo.1"));
        }
    }

}
