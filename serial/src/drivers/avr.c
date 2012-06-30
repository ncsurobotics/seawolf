
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
    SW_TEMP     = 0x05,
    SW_SOLENOID = 0x06,
    SW_BATTERY  = 0x07,
    SW_KILL     = 0x08
};

typedef enum {
    SERVO1 = 0,
    SERVO2 = 1
} Servo;

typedef enum {
    SOLENOID1 = 0,
    SOLENOID2 = 1,
    SOLENOID3 = 2
} Solenoid;

typedef enum {
    PORT   = 0,
    STAR   = 1,
    STERN  = 2,
    BOW    = 3,
    STRAFE = 4
} Motor;

typedef enum {
    SLA1 = 0,
    SLA2 = 1,
    LIPO = 2
} Battery;

typedef enum {
    KILLED = 0,
    NOT_KILLED = 1
} KillStatus;

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

        case SW_BATTERY:
            switch(frame[1]) {
            case SLA1:
                Logging_log(WARNING, "SLA battery 1 low!");
                break;

            case SLA2:
                Logging_log(WARNING, "SLA battery 2 low!");
                break;

            case LIPO:
                Logging_log(WARNING, "LiPo batteries low!");
                break;
            }

            Var_set("StatusLight", 3);
            break;

        case SW_KILL:
            /* Send appropirate notification */
            if(frame[2] == 0) {
                Notify_send("EVENT", "PowerKill");
            } else {
                Notify_send("EVENT", "SystemReset");
            }
            break;
        }
    }

    return NULL;
}

static void set_thruster(SerialPort sp, Motor motor, float value) {
    char command[3];

    command[0] = SW_MOTOR;
    command[1] = motor;
    command[2] = (int) (MOTOR_RANGE * value);

    Serial_send(sp, command, 3);
    Util_usleep(0.01); /* XXX: Remove this when the avr works right */
}

#if 0

static void set_solenoid(SerialPort sp, Solenoid solenoid, float value) {
    char command[3];

    command[0] = SW_SOLENOID;
    command[1] = solenoid;
    command[2] = (int) value;

    Serial_send(sp, command, 3);
}

static void set_servo(SerialPort sp, Servo servo, float value) {
    char command[3];

    command[0] = SW_SERVO;
    command[1] = servo;
    command[2] = (int) value;

    Serial_send(sp, command, 3);
}

#endif

static void set_status(SerialPort sp, int value) {
    unsigned char command[3];

    command[0] = SW_STATUS;
    command[1] = 0;

    switch(value) {
    case 0:
        command[2] = 200;
        break;

    case 1:
        command[2] = 100;
        break;

    case 2:
        command[2] = 0;
        break;

    case 3:
        command[2] = 180;
        break;

    default:
        Logging_log(ERROR, "Invalid StatusLight value!");
    }

    Serial_send(sp, command, 3);
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

#if 0
    Var_subscribe("Solenoid.0");
    Var_subscribe("Solenoid.1");
    Var_subscribe("Solenoid.2");
    Var_subscribe("Servo.0");
    Var_subscribe("Servo.1");
#endif

    Var_subscribe("StatusLight");

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

#if 0
        if(Var_poked("Solenoid.0")) {
            set_solenoid(sp, SOLENOID1, Var_get("Solenoid.0"));
        }

        if(Var_poked("Solenoid.1")) {
            set_solenoid(sp, SOLENOID2, Var_get("Solenoid.1"));
        }

        if(Var_poked("Solenoid.2")) {
            set_solenoid(sp, SOLENOID3, Var_get("Solenoid.2"));
        }

        if(Var_poked("Servo.0")) {
            set_servo(sp, SERVO1, Var_get("Servo.0"));
        }

        if(Var_poked("Servo.1")) {
            set_servo(sp, SERVO2, Var_get("Servo.1"));
        }
#endif

        if(Var_poked("StatusLight")) {
            set_status(sp, Var_get("StatusLight"));
        }
    }

    Serial_closePort(sp);
    Seawolf_close();

    return 0;
}
