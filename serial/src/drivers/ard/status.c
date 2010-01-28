
#include "seawolf.h"

#include <stdio.h>
#include <string.h>

void manage(SerialPort sp);

const char* app_name = "Serial : Mission Status";

void manage(SerialPort sp) {
    while(true) {
        Logging_log(DEBUG, "Waiting for start");
        while(Serial_getByte(sp) != 0xBA);
        Notify_send("MISSIONTRIGGER", "NULL");
        Logging_log(DEBUG, "Got start");
    }
}
