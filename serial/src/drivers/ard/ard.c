
#include "seawolf.h"

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

extern const char* app_name;
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

    /* Set port to block */
    Serial_setBlocking(sp);

    /* Error checking done */
    Logging_log(INFO, Util_format("%s running successfully with device %s", argv[0], device));

    /* Complete handshake */
    ArdComm_handshake(sp);

    /* Start app specific code */
    manage(sp);

    /* Close serial device and exit */
    Serial_closePort(sp);
    Seawolf_close();
    return 0;
}
