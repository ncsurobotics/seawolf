
#include "seawolf.h"

#include <math.h>

#define SIGNBIT(x) (((x) & (1<<7)) ? (((~((x)-1)) | (((x) & (1 << 7)) >> 1))) : (x))
#define DEAD_BAND 8

void manage(SerialPort sp);

const char* app_name = "Serial : thruster3";

void manage(SerialPort sp) {
    /* Only recieved notifications for the following */
    Notify_filter(FILTER_MATCH, "UPDATED Aft");

    char varname[32];
    float read_value;
    unsigned char param;

    /* Zero thrusters */
    Serial_sendByte(sp, 0);

    /* Main loop */
    while(true) {
        Notify_get(NULL, varname);
        read_value = Var_get("Aft");
        if(fabs(read_value) > DEAD_BAND) {
            param = (unsigned char) read_value;
            param = SIGNBIT(param);
        } else {
            param = 0;
        }

        Serial_sendByte(sp, param);
    }
}
