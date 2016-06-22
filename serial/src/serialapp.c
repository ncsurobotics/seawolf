
#include "seawolf.h"

#include <glob.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stropts.h>
#include <unistd.h>
#include <errno.h>

/* Device types */
typedef enum{
    PT_UNMANAGED = 0,
    PT_IMU = 1,
    PT_AVR = 2,
    PT_DEPTH = 3,
    PT_PERIPHERAL = 4,
    PT_PNEUMATICS = 5,
    PT_IMUSPARK = 6,
} PeripheralType;

/* Cycle the DTR line on the given serial port */
/*
static void cycleDTR(SerialPort sp) {
    Serial_setDTR(sp, 0);
    Util_usleep(0.1);
    Serial_setDTR(sp, 1);
    Util_usleep(0.1);
}
*/

static int handshake_imu_spark(SerialPort sp) {
    // set baud
    Serial_setBaud(sp, 57600);
    
    // send synchro message
    char* sync_req = "#s12";
    char* sync_match_string = "#SYNCH12\r\n";
    int   match_length = strlen(sync_match_string);
    Serial_flush(sp);
    Util_usleep(.05);

    // is it streaming?
    //printf("[IMU-test] %d bytes available.\n", Serial_available(sp));
    if (Serial_available(sp) <= 0) {
        return false;
    }

    //Serial_flush(sp); commented out because it slows down the code when avr runs. why?
    Serial_send(sp, sync_req, strlen(sync_req));

    // listen for synchro message
    uint8_t i = 0;
    uint8_t nomatch=0;
    while ( (nomatch < 255) && (i < match_length) ) {
        // read data
        char b = (char) Serial_getByte(sp);
        //printf("(%d,%c) : ",nomatch,b);
        //printf("%s\n",strerror(errno));

        if (b != sync_match_string[i]) {
            // no match
            i = 0;
            nomatch++;
        }

        if (b == sync_match_string[i]) {
            // matching char discovered
            i++;
        }

        // not sure why this is needed, but code doesn't work without it.
        Util_usleep(.001);
        
    }

    if (i==match_length) {
        //(sparkfun) IMU found!
        return true;
    } else {
        return false;
    }
}

static int handshake_avr (SerialPort sp) {
    /* Set to AVR baud rate */
    Serial_setBaud(sp, 57600);

    // setup variables
    int n=0;

    /* Send reset sequence */
    for(int i = 0; i < 5; i++) {

        n = Serial_sendByte(sp, 'r');

        if(n == -1) {
            Logging_log(ERROR, "Unable to send data");
            return -1;
        }
    }

    // setup variables
    int bytes_received  = 0; //Number of bytes received
    int good_count      = 0; //Number of consecutive 0xff bytes received */
    int error_count     = 0; //Number of consecutive failures to get a byte */
    

    do {
        if(Serial_available(sp) > 0) {
            n = Serial_getByte(sp);
            
            bytes_received++;
            error_count = 0;

            // look for the 0xff reply stream
            if(n == 0xff) {
                good_count++;
            } else {
                good_count = 0;
            }

            // convinced after a few iterations
            if(good_count == 16) {
                return true;
            }
        } else {
            Util_usleep(0.1);
            error_count++;
        }
    } while(error_count < 5 && bytes_received < 512);

    /* Give up after 5 attempts to receive data or 1024 bytes received total */
    return false;
}

static int handshake_imu_lord(SerialPort sp) {
    /* Set to IMU's baud rate */
    Serial_setBaud(sp, 38400);

    /* setup variables */
    int n = 1;
    
    /* Probe IMU by sending version number command */
    Serial_flush(sp);
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
            return true;
        }
    }

    return false;
}

static int handshake_pneumatics(SerialPort sp) {
    // set baud rate
    Serial_setBaud(sp, 9600);

    // setup variables
    int n = 0;
    char ret_string[128];

    // reset pneumatics
    n = Serial_sendByte(sp, 'r');//reset pneumatics
    Serial_flush(sp);

    /* Poke Pneumatics with predefined command */
    n = Serial_sendByte(sp, 0xFE);
    if(n == -1) {
        Logging_log(ERROR, "Unable to send data");
        return -1;
    }

    //give a little time for arduino to respond
    Util_usleep(.1);

    //if any response has been obtained, check if {ID|PNEUMATICS}\r\n
    n = Serial_available(sp);
    if ((n > 0) && (n < 128)) {
        Serial_get(sp,ret_string,n);
        if (strncmp(ret_string, "{ID|Pneumatics}\r\n",n)==0) {
            /* Received PNEUMATICS response */
            Logging_log(DEBUG, "PNEUMATICS Found");
            Serial_flush(sp);
            return true;
        }
    }

    return false;
}

static int getPeripheralType(SerialPort sp) {
    //printf("going\n");
    //char id[32];
    int results = 0;


    /* attempt AVR */
    if (handshake_avr(sp)==true){
        return PT_AVR;
    }

    /* attempt (SPARKFUN) IMU */
    Util_usleep(2); // uncomment if IMU DTR pin is connected.
    /* WARNING: do not do this check before the AVR test. The check against
     * AVR vs. this handshake is VERY SLOW when AVR is already active, because
     * the AVR also streams data, but at a very casual rate. */
    if (handshake_imu_spark(sp)==true){
        return PT_IMUSPARK;
    }

    /* attempt (LORD) IMU */
    results = handshake_imu_lord(sp);
    if (results==true){
        return PT_IMU;
    } else if (results==-1) {
        return -1;
    }

    
    
    /* attempt Pneumatics */
    if (handshake_pneumatics(sp)==true){
        return PT_PNEUMATICS;
    }

    // if none of these succeed, there's probably nothing there.
    return -1;
}

int main(void) {
    /* Configuration */
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Serial");

    const char* port_path;
    SerialPort sp;
    PeripheralType pt;

    /* Glob type for serial interface search */
    glob_t globbuff;

    /* App to executable mappings */
    char* drivers[] = {
        [PT_IMU] = "./bin/imu",
        [PT_AVR] = "./bin/avr",
        [PT_DEPTH] = "./bin/depth",
        [PT_PERIPHERAL] = "./bin/peripheral",
        [PT_PNEUMATICS] = "./bin/pneumatics",
        [PT_IMUSPARK] = "./bin/imuspark",
    };

    /* Find serial ports */
    glob("/dev/ttyUSB*", 0, NULL, &globbuff);
    //glob("/dev/ttyS*", GLOB_APPEND, NULL, &globbuff);

    for(int i = 0; i < globbuff.gl_pathc; i++) {
        port_path = globbuff.gl_pathv[i];
        sp = Serial_open(port_path);

        if(sp == -1) {
            Logging_log(ERROR, Util_format("Error opening %s: %s.", port_path, strerror(errno)));
            continue;
        }

        pt = getPeripheralType(sp);
        Serial_closePort(sp);

        if(pt == -1) {
            Logging_log(ERROR, Util_format("Unable to identify device on %s", port_path));
        } else {
            Logging_log(INFO, Util_format("Identified device on %s. Spawning %s", port_path, drivers[pt]));

            /* Fork and execute subprocess in child */
            if(fork() == 0) {
                execl(drivers[pt], drivers[pt], port_path, NULL);
                fprintf(stderr, "Unable to spawn application (%s)\n", drivers[pt]);
                _exit(1);
            }
        }
    }

    /* Send notification of completion */
    Notify_send("COMPLETED", "Serial identification");

    while(true) {
        Util_usleep(5.0);
    }

    Seawolf_close();
    return 0;
}
