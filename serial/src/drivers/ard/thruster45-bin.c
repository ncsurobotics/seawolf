
#include "seawolf.h"

#include <math.h>
#include <string.h>

#define SIGNBIT(x) (((x) & (1<<7)) ? (((~((x)-1)) | (((x) & (1 << 7)) >> 1))) : (x))
#define DEAD_BAND 3

void manage(SerialPort sp);

const char* app_name = "Serial : thruster45";

void manage(SerialPort sp) {
    /* Only recieved notifications for the following */
    Notify_filter(FILTER_MATCH, "UPDATED PortX"); // 4
    Notify_filter(FILTER_MATCH, "UPDATED StarX"); // 5

    char action[16], varname[32];
    float read_value;
    unsigned char param;

    /* Zero thrusters */
    Serial_sendByte(sp, 0);
    Serial_sendByte(sp, 1 << 7);

    /* Main loop */
    while(true) {
        Notify_get(action, varname);
        if(strcmp(varname, "PortX") == 0) {
            /* thruster PortX */
            read_value = Var_get("PortX");
            if(fabs(read_value) > DEAD_BAND) {
                param = (unsigned char) read_value;
                param = SIGNBIT(param);
                param &= (1 << 7) - 1; /* clear highest bit */
            } else {
                param = 0;
            }
        } else {
            /* thruster StarX */
            read_value = Var_get("StarX");
            if(fabs(read_value) > DEAD_BAND) {
                param = (unsigned char) read_value;
                param = SIGNBIT(param);
                param |= (1 << 7); /* set highest bit */
            } else {
                param = 1 << 7;
            }
        }
        Serial_sendByte(sp, param);
    }
}
