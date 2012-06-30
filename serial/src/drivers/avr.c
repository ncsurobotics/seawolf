
#include "seawolf.h"

#include <pthread.h>

/* PSI per foot of fresh water (calculate) */
#define PSI_PER_FOOT 0.433527504

/* Approximate air pressure in Raleigh. This number is from a weather forecast
   for Raleigh */
#define AIR_PRESSURE 14.782

/* XXX: Make this 128 when the avr works right */
#define MOTOR_RANGE 127

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

    /* Convert 12 bit unsigned ADC reading to a voltage */
    voltage = 5.004 * (raw_adc_value / 4095.0);

    /* The pressure sensor produces output between 0.5 and 4.5 volts. This range
       maps linearly to the 0-100psi range */
    psi = ((voltage - 0.5) / 4.0) * 100;

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

static void set_thruster(SerialPort sp, enum Motors motor, float value) {
    char command[3];
    command[0] = SW_MOTOR;
    command[1] = motor;
    command[2] = (int) (MOTOR_RANGE * value);
    Serial_send(sp, command, 3);
    Util_usleep(0.01); /* XXX: Remove this when the avr works right */
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
            set_thruster(sp, BOW, Var_get("Bow"));
        }

        if(Var_poked("Stern")) {
            set_thruster(sp, STERN, Var_get("Stern"));
        }

        if(Var_poked("Strafe")) {
            set_thruster(sp, STRAFE, Var_get("Strafe"));
        }

        if(Var_poked("Port")) {
            set_thruster(sp, PORT, Var_get("Port"));
        }

        if(Var_poked("Star")) {
            set_thruster(sp, STAR, Var_get("Star"));
        }

    }

    Serial_closePort(sp);
    Seawolf_close();

    return 0;
}
