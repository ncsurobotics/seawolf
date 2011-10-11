
#include "seawolf.h"

#include "math.h"

#define CTRL_LIGHTS  0x01
#define CTRL_DROPPER 0x02
#define CTRL_TORPEDO 0x03

/* Air and water pressure constants. Varies by location (calibration recommended) */
#define PSI_PER_FOOT 0.4335
#define AIR_PRESSURE 14.23
#define DEPTH_ZERO 0.0

/* Ignore changes in depth greater than this. */
#define MAX_DEPTH_DELTA 2

/* Stops depth from running. */
//#define DISABLE_DEPTH

void manage(SerialPort sp);

const char* app_name = "Serial : PerphBoard";

static SerialPort sp;

static int outgoing_data(void) {
    char action[16], data[32];

    Notify_filter(FILTER_MATCH, "UPDATED StatusLight");
    Notify_filter(FILTER_MATCH, "RUN Dropper");
    Notify_filter(FILTER_MATCH, "RUN Torpedo");

    while(true) {
        Notify_get(action, data);

        if(strcmp(data, "StatusLight") == 0) {
            Serial_sendByte(sp, 0xff);
            Serial_sendByte(sp, CTRL_LIGHTS);
            Serial_sendByte(sp, (unsigned char) Var_get("StatusLight"));
        } else if(strcmp(data, "Dropper") == 0) {
            Serial_sendByte(sp, 0xff);
            Serial_sendByte(sp, CTRL_DROPPER);
            Serial_sendByte(sp, 0x01);
        } else if(strcmp(data, "Torpedo") == 0) {
            Serial_sendByte(sp, 0xff);
            Serial_sendByte(sp, CTRL_TORPEDO);
            Serial_sendByte(sp, 0x01);
        }
    }

    return 0;
}

static void sync_stream(void) {
    int syncs = 0, n;
    while(syncs < 3) {
        n = Serial_getByte(sp);

        if(n == 0xff) {
            syncs++;
        } else {
            syncs = 0;
        }
    }
}

void manage(SerialPort _sp) {
    uint8_t data[3];
    short raw_depth;
    float voltage, psi, depth, last_good_depth;
    bool good_depth_seeded = false;

    /* Store serial port globally */
    sp = _sp;
    
    /* Set blocking */
    Serial_setBlocking(sp);

    /* Align data stream */
    sync_stream();

    /* Start thread for outgoing data/requests */
    Task_background(outgoing_data);

    while(true) {
        Serial_get(sp, data, 3);
        if(data[0] == 0x01) {
            if(data[1] == 0x01) {
                Notify_send("EVENT", "PowerKill");
                Logging_log(DEBUG, "Power killed");
            } else if(data[1] == 0x02) {
                Notify_send("EVENT", "SystemReset");
                Logging_log(DEBUG, "System reset");
            } else {
                Logging_log(ERROR, Util_format("Unknown event 0x%02X 0x%02X", data[1], data[2]));
            }
        } else if(data[0] == 0x02) {
            #ifdef DISABLE_DEPTH
                continue;
            #endif
            /* Compute depth */
            raw_depth = (data[1] * 256) + data[2];
            voltage = raw_depth * (5.0/1024.0);
            psi = ((voltage - 0.5) * 100) / 4.0;
            depth = (psi - AIR_PRESSURE) / PSI_PER_FOOT - DEPTH_ZERO;

            if(good_depth_seeded == false) {
                good_depth_seeded = true;
                last_good_depth = depth;
                continue;
            }

            if(fabs(depth - last_good_depth) > MAX_DEPTH_DELTA) {
                Logging_log(ERROR, Util_format("Extraodinary depth value. (%.2f, 0x%04x)", depth, raw_depth));
                continue;
            }

            Var_set("Depth", depth);
            last_good_depth = depth;
        } else {
            Logging_log(ERROR, "Invalid data from peripheral board!");
        }
    }
}
