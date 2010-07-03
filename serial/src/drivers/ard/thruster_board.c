
#include "seawolf.h"

#include <math.h>
#include <string.h>

/* Minimum value to turn thrusters on at */
#define DEAD_BAND 8

/* Thruster numbers */
#define PORT_X 0
#define STAR_X 1
#define PORT_Y 2
#define STAR_Y 3
#define AFT    4

void manage(SerialPort sp);

const char* app_name = "Serial : ThrusterBoard";

static int get_thruster_number(const char* name) {
    if(strcmp(name, "PortX") == 0) {
        return PORT_X;
    } else if(strcmp(name, "StarX") == 0) {
        return STAR_X;
    } else if(strcmp(name, "PortY") == 0) {
        return PORT_Y;
    } else if(strcmp(name, "StarY") == 0) {
        return STAR_Y;
    } else if(strcmp(name, "Aft") == 0) {
        return AFT;
    }

    return -1;
}

void manage(SerialPort sp) {
    char varname[32];
    unsigned char data[2];
    float value;

    /* Set blocking */
    Serial_setBlocking(sp);

    /* Receive all thruster update notifications */
    Notify_filter(FILTER_MATCH, "UPDATED PortX");
    Notify_filter(FILTER_MATCH, "UPDATED StarX");
    Notify_filter(FILTER_MATCH, "UPDATED PortY");
    Notify_filter(FILTER_MATCH, "UPDATED StarY");
    Notify_filter(FILTER_MATCH, "UPDATED Aft");

    /* Main loop */
    while(true) {
        Notify_get(NULL, varname);

        /* Get thruster number */
        data[0] = get_thruster_number(varname);

        /* Get thruster value */
        value = (int) Var_get(varname);

        /* Set base value */
        data[1] = (int) fabs(value);
        
        /* Set to zero if less than dead band */
        if(data[1] <= DEAD_BAND) {
            data[1] = 0;
        }

        /* Set direction bit */
        if(value < 0) {
            data[1] |= (1 << 6);
        }

        /* Set high bit (used as frame sync) */
        data[1] |= (1 << 7);

        /* Send data */
        Serial_send(sp, data, 2);
    }
}
