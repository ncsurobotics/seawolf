
#include "seawolf.h"

#include <pthread.h>

/* PSI per foot of fresh water (calculate) */
#define PSI_PER_FOOT 0.433527504

/* Approximate air pressure in Raleigh. This number is from a weather forecast
   for Raleigh */
#define AIR_PRESSURE 14.782

#define MOTOR_RANGE 128

enum Commands {
    SW_RESET    = 0x72,  /* 'r' full reset */
    SW_NOP      = 0x00,
    SW_MOTOR    = 0x01,
    SW_SERVO    = 0x02,
    SW_STATUS   = 0x03,
    SW_DEPTH    = 0x04,
    SW_TEMP     = 0x05
};

enum Motors {
    PORT   = 0,
    STAR   = 1,
    STERN  = 2,
    BOW    = 3,
    STRAFE = 4
};

static void avr_synchronize(SerialPort sp) {
    int i;

    for(i = 0; i < 5; i++) {
        Serial_sendByte(sp, SW_RESET);
    }

    i = 0;
    while(i < 8) {
        if(Serial_getByte(sp) == 0xff) {
            i++;
        } else{
            i = 0;
        }
    }

    Serial_sendByte(sp, 0x00);
    
    while(Serial_getByte(sp) != 0xf0);
}

static void set_depth(int16_t raw_adc_value) {
    float voltage;
    float psi;
    float depth;

    /* Ground starts at 200 and 4095 is 0.95 (max reading) volts approximately */
    //voltage = ((raw_adc_value - 200.0) / (4095.0 - 200.0)) * 0.95;
    voltage = raw_adc_value / 2047.0;
    
    /* Depth sensor output has been halved. The depth sensor outputs between 0.5
       and 4.5 volts. This 4V range corresponds linearly to 0 to 100 PSI */
    psi = (((voltage * 2) - 0.5) / 4.0) * 100;

    /* Compute depth based on surface pressure and PSI per foot */
    depth = (psi - AIR_PRESSURE) / PSI_PER_FOOT;

    Var_set("Depth", depth);
}

static void set_temp(int16_t raw_adc_value) {
    Var_set("Temperature", (float) raw_adc_value / 2047.0);
}

static void* receive_thread(void* _sp) {
    SerialPort sp = *((SerialPort*)_sp);
    uint8_t frame[3];
    
    while(true) {
        Serial_get(sp, frame, 3);
        
        switch(frame[0]) {
        case SW_DEPTH:
            set_depth(frame[1] << 8 | frame[2]);
            break;

        case SW_TEMP:
            set_temp(frame[1] << 8 | frame[2]);
            break;
        }
    }

    return NULL;
}
 
int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Serial : AVR");

    /* Device path */
    char* device_real = argv[1];

    /* Serial port device */
    SerialPort sp;

    /* Receive thread */
    pthread_t thread;

    /* Command */
    char command[3];

    /* Open and initialize the serial port */
    sp = Serial_open(device_real);
    Serial_setBlocking(sp);
    if(sp == -1) {
        Logging_log(ERROR, "Could not open serial port for AVR! Exiting.");
        Seawolf_exitError();
    }

    /* Set options */
    Serial_setBaud(sp, 57600);

    avr_synchronize(sp);
    Logging_log(DEBUG, "Synchronized");

    /* Spawn receive thread */
    pthread_create(&thread, NULL, receive_thread, &sp);

    Var_subscribe("Bow");
    Var_subscribe("Stern");
    Var_subscribe("Strafe");
    Var_subscribe("Port");
    Var_subscribe("Star");

    while(true) {
        Var_sync();

        if(Var_poked("Bow")) {
            command[0] = SW_MOTOR;
            command[1] = BOW;
            command[2] = (int) (MOTOR_RANGE * Var_get("Bow"));
            Serial_send(sp, command, 3);
        } 

        if(Var_poked("Stern")) {
            command[0] = SW_MOTOR;
            command[1] = STERN;
            command[2] = (int) (MOTOR_RANGE * Var_get("Stern"));
            Serial_send(sp, command, 3);
        } 

        if(Var_poked("Strafe")) {
            command[0] = SW_MOTOR;
            command[1] = STRAFE;
            command[2] = (int) (MOTOR_RANGE * Var_get("Strafe"));
            Serial_send(sp, command, 3);
        } 

        if(Var_poked("Port")) {
            command[0] = SW_MOTOR;
            command[1] = PORT;
            command[2] = (int) (MOTOR_RANGE * Var_get("Port"));
            Serial_send(sp, command, 3);
        } 

        if(Var_poked("Star")) {
            command[0] = SW_MOTOR;
            command[1] = STAR;
            command[2] = (int) (MOTOR_RANGE * Var_get("Star"));
            Serial_send(sp, command, 3);
        } 
    }

    Serial_closePort(sp);
    Seawolf_close();

    return 0;
}
