
#include "seawolf.h"

#include <math.h>
#include <string.h>

/* Thruster scaling value */
#define THRUSTER_SCALER 63

/* Minimum value to turn thrusters on at */
#define YAW_DEAD_BAND 3
#define DEPTH_DEAD_BAND 8

/* Thruster numbers */
#define PORT   0 // (old PORT_X)
#define STAR   1 // (old STAR_X)
#define STRAFE 2 // (old PORT_Y)
#define BOW    3 // (old STAR_Y)
#define STERN  4 // (renamed from AFT)

void manage(SerialPort sp);

const char* app_name = "Serial : ThrusterBoard";

static int get_thruster_number(const char* name) {
    if(strcmp(name, "Port") == 0) {
        return PORT;
    } else if(strcmp(name, "Star") == 0) {
        return STAR;
    } else if(strcmp(name, "Strafe") == 0) {
        return STRAFE;
    } else if(strcmp(name, "Bow") == 0) {
        return BOW;
    } else if(strcmp(name, "Stern") == 0) {
        return STERN;
    }

    return -1;
}

void manage(SerialPort sp) {
    char varname[32];
    unsigned char data[2];
    int value;

    /* Set blocking */
    Serial_setBlocking(sp);

    /* Receive all thruster update notifications */
    Notify_filter(FILTER_MATCH, "UPDATED Port");
    Notify_filter(FILTER_MATCH, "UPDATED Star");
    Notify_filter(FILTER_MATCH, "UPDATED Strafe");
    Notify_filter(FILTER_MATCH, "UPDATED Bow");
    Notify_filter(FILTER_MATCH, "UPDATED Stern");

    /* Main loop */
    while(true) {
        Notify_get(NULL, varname);

        /* Get thruster number */
        data[0] = get_thruster_number(varname);

        /* Get thruster value */
        value = (int) (Var_get(varname) * THRUSTER_SCALER);

        /* Set base value */
        data[1] = ((value < 0) ? -value : value);
        
        /* Set to zero if less than dead band */
        if(((data[0] == STAR || data[0] == PORT) && data[1] <= YAW_DEAD_BAND) ||
           ((data[0] == STERN || data[0] == BOW) && data[1] <= DEPTH_DEAD_BAND)) {
            data[1] = 0;
        }

        /* Set direction bit */
        if(value > 0) {
            data[1] |= (1 << 6);
        }

        /* Set high bit (used as frame sync) */
        data[1] |= (1 << 7);

        /* Send data */
        Serial_send(sp, data, 2);
    }
}
