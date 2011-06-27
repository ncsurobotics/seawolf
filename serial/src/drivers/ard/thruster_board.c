
#include "seawolf.h"

#include <math.h>
#include <string.h>

/* Thruster scaling value */
#define THRUSTER_SCALER 63

/* Minimum value to turn thrusters on at */
#define YAW_DEAD_BAND 3
#define DEPTH_DEAD_BAND 8

/* Thruster numbers */
#define PORT   0
#define STAR   1
#define BOW    2
#define STERN  3
#define STRAFE 4

void manage(SerialPort sp);

const char* app_name = "Serial : ThrusterBoard";

static void pack_message(unsigned char* data, int thruster, float value) {
    /* Get thruster number */
    data[0] = thruster;

    /* Get thruster value */
    value = (int) (value * THRUSTER_SCALER);

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
}

void manage(SerialPort sp) {
    unsigned char data[2];

    /* Set blocking */
    Serial_setBlocking(sp);

    /* Receive all thruster update notifications */
    Var_subscribe("Port");
    Var_subscribe("Star");
    Var_subscribe("Strafe");
    Var_subscribe("Bow");
    Var_subscribe("Stern");

    /* Main loop */
    while(true) {
        Var_sync();

        if(Var_stale("Port")) {
            pack_message(data, PORT, Var_get("Port"));
            Serial_send(sp, data, 2);
        }

        if(Var_stale("Star")) {
            pack_message(data, STAR, Var_get("Star"));
            Serial_send(sp, data, 2);
        }
    
        if(Var_stale("Strafe")) {
            pack_message(data, STRAFE, Var_get("Strafe"));
            Serial_send(sp, data, 2);
        } 
    
        if(Var_stale("Bow")) {
            pack_message(data, BOW, Var_get("Bow"));
            Serial_send(sp, data, 2);
        }
    
        if(Var_stale("Stern")) {
            pack_message(data, STERN, Var_get("Stern"));
            Serial_send(sp, data, 2);
        }
    }
}
