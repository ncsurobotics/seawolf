
/*     __
      |  |\
     ---------------------\
    |                     |\
    |   Seawolf VI        ||
    |                     ||
    \---------------------\|
     \---------------------\

   forward
   <----------O
              |\
              | \ Strafe
              |  \
              |   *
              |
              v Depth
 
 * as shown, depth points down. depth = -z for those of you who are 
 * used to the traditional xyz coordinate system. Positive depth means x 
 * ft "below" the surface.*/

#include "seawolf.h"

#include <pthread.h>

/* PSI per foot of fresh water (calculate) */
#define PSI_PER_FOOT 0.433527504

/* Approximate air pressure in Raleigh. This number is the median air pressure
*  recorded in the span from Saturday 04/23 to Monday 05/02 (year 2016).
*  MAX/MIN pressures recorded in this time span were 14.84/14.63 PSI.*/
#define AIR_PRESSURE 14.74 //pounds per square inch, 
#define DEPTH_OFFSET -2    //correction factor for putting sensor noise margin
                           //above the surface rather than at the surface

#define DEPTH_OVRSAMPLE 4

#define MOTOR_RANGE 127
#define RANGE_CORRECTION 0.500

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
    SW_KILL     = 0x08,
    SW_REALIGN  = 0x09,
    SW_ERROR    = 0xaa,
    SW_MARKER   = 0xbb
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
    STRAFET = 4,
    STRAFEB = 5,
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

typedef enum {
    INVALID_REQUEST = 0,
    SERIAL_ERROR = 1,
    TWI_ERROR = 2,
    SYNC_ERROR = 3
} Error;

typedef struct LPF_STRUCT16 {
        float value;
        float* buf;
        uint8_t head;
        uint8_t n_samples;
} LPF_t;

static const char* error_messages[] = {
    [INVALID_REQUEST] = "Invalid request",
    [SERIAL_ERROR] = "Serial error",
    [TWI_ERROR] = "I2C error",
    [SYNC_ERROR] = "Synchronization error"
};

static pthread_mutex_t send_lock = PTHREAD_MUTEX_INITIALIZER;

static void avr_synchronize(SerialPort sp) {
    int i;
    int n;

    for(i = 0; i < 5; i++) {
        Serial_sendByte(sp, SW_RESET);
    }

    Logging_log(DEBUG, "Sent reset sequence");

    i = 0;
    while(i < 10) {
        n = Serial_getByte(sp);

        if(n == 0xff) {
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
    static float buf[DEPTH_OVRSAMPLE];
    
    static LPF_t depth_filter = {
        .value = 0,
        .buf = buf,
        .head = 0,
        .n_samples = DEPTH_OVRSAMPLE,
    };

    /* Convert 12 bit unsigned ADC reading to a voltage */
    voltage = 5.004 * (raw_adc_value / 4095.0);

    /* The pressure sensor produces output between 0.5 and 4.5 volts. This range
       maps linearly to the 0-100psi range */
    psi = ((voltage - 0.5) / 4.0) * 100;

    //Logging_log(DEBUG, Util_format("Current Air Pressure: %f lb/in^2\n",psi));
    //Logging_log(DEBUG, Util_format("Pressure Sensor Voltage: %f V\n",voltage));

    /* Compute depth based on surface pressure and PSI per foot */
    depth = (psi - AIR_PRESSURE) / PSI_PER_FOOT;
    depth += DEPTH_OFFSET;

    /* run lowpass filter on depth sensor */
    /* note: we only sample depth sensor at a rate of 10Hz. we may want
    *  to increase the sample rate on this since we have a low pass filter
    *  here now */
    depth_filter.buf[depth_filter.head] = depth; //sample
    depth_filter.head = (depth_filter.head + 1) % depth_filter.n_samples; //incr
    depth_filter.value = 0;
    for(int i=0; i<depth_filter.n_samples; i++) {
        depth_filter.value += depth_filter.buf[i]; //sum
    }
    depth = (depth_filter.value/ depth_filter.n_samples); //output
    //printf("depth of %0.2f\n" , depth);

    /* submit depth measurement to robot */
    Var_set("Depth", depth);
}

static void set_temp(int16_t raw_adc_value) {
    Var_set("Temperature", (float) raw_adc_value / 2047.0);
}

static void send_message(SerialPort sp, unsigned char cmd, unsigned char arg1, unsigned char arg2) {
    unsigned char command[3];

    command[0] = cmd;
    command[1] = arg1;
    command[2] = arg2;

    if (cmd== SW_MOTOR) {
        printf("arg2=%d\n", arg2);
    }

    pthread_mutex_lock(&send_lock);
    Serial_send(sp, command, 3);
    pthread_mutex_unlock(&send_lock);
}

static void* receive_thread(void* _sp) {
    SerialPort sp = *((SerialPort*)_sp);
    uint8_t frame[3];

    while(true) {
        Serial_get(sp, frame, 3);
        //Logging_log(DEBUG, Util_format("Checking packet from AVR! (0x%02x, 0x%02x, 0x%02x)",
        //                                      frame[0], frame[1], frame[2]));

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
                //Var_set("StatusLight", 3);
                break;
            }
            break;

        case SW_KILL:
            /* Send appropirate notification */
            /* is diver commands the robot to be unkilled
            (kill switch disengaged) command a system reset,
            which can act as a signal to seawolf that it is
            ready to begin a mission. */
            if(frame[2] == 0) {
                Notify_send("EVENT", "SystemReset");
                
            /* if error, report kill switch detection fault */
            /* April 3rd: Currently suspecting the Powerboard is going rouge and
            responding to with 0xFF ocassionally. */
            } else if (frame[2] == 0xFF) {
            	Logging_log(ERROR, "AVR error: Killswitch detection fault.");
            
            /* else, seawolf has been killed (kill switch
            engaged), thus send out a notification indicating
            so. */
            } else {
                Notify_send("EVENT", "PowerKill");
            }
            break;

        case SW_ERROR:
            Logging_log(ERROR, Util_format("AVR error: %s (0x%02x)", error_messages[frame[1]], frame[2]));
            break;

        case SW_REALIGN:
            Logging_log(ERROR, "Realigning");
            send_message(sp, SW_MARKER, SW_MARKER, SW_MARKER);
            break;

        default:
            Logging_log(CRITICAL, Util_format("Invalid packet from AVR! (0x%02x, 0x%02x, 0x%02x)",
                                              frame[0], frame[1], frame[2]));
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

    /* Open and initialize the serial port */
    sp = Serial_open(device_real);

    if(sp == -1) {
        Logging_log(ERROR, "Could not open serial port for AVR! Exiting.");
        Seawolf_exitError();
    }

    /* Set options */
    Serial_setBaud(sp, 57600);
    Serial_setBlocking(sp);
    Serial_flush(sp);

    avr_synchronize(sp);
    Logging_log(DEBUG, "Synchronized");

    /* Spawn receive thread */
    pthread_create(&thread, NULL, receive_thread, &sp);

    /* Reset status light */
    Var_set("StatusLight", 0);

    Var_subscribe("Bow");
    Var_subscribe("Stern");
    Var_subscribe("StrafeT");
    Var_subscribe("StrafeB");
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
        	//printf("Bow = %.2f\n", -Var_get("Bow"));
            send_message(sp, SW_MOTOR, BOW, (int) (MOTOR_RANGE * -Var_get("Bow") * RANGE_CORRECTION));
        }

        if(Var_poked("Stern")) {
        	//printf("Stern\n");
            send_message(sp, SW_MOTOR, STERN, (int) (MOTOR_RANGE * -Var_get("Stern") * RANGE_CORRECTION));
        }

        if(Var_poked("StrafeT")) {
        	//printf("StrafeT\n");
            send_message(sp, SW_MOTOR, STRAFET, (int) (MOTOR_RANGE * -Var_get("StrafeT") * RANGE_CORRECTION));
        }

        if(Var_poked("StrafeB")) {
        	//printf("StrafeB\n");
            send_message(sp, SW_MOTOR, STRAFEB, (int) (MOTOR_RANGE * -Var_get("StrafeB") * RANGE_CORRECTION));
        }

        if(Var_poked("Port")) {
        	//printf("Port\n");
            send_message(sp, SW_MOTOR, PORT, (int) (MOTOR_RANGE * -Var_get("Port") * RANGE_CORRECTION));
        }

        if(Var_poked("Star")) {
        	//printf("Star\n");
            send_message(sp, SW_MOTOR, STAR, (int) (MOTOR_RANGE * -Var_get("Star") * RANGE_CORRECTION));
        }

        if(Var_stale("StatusLight")) {
            switch((int)Var_get("StatusLight")) {
            /* legacy code. Not supported in new electronics system  */
            case 0:

                //send_message(sp, SW_STATUS, 0, 200);
                break;

            case 1:
                //send_message(sp, SW_STATUS, 0, 100);
                break;

            case 2:
                //send_message(sp, SW_STATUS, 0, 0);
                break;

            case 3:
                //send_message(sp, SW_STATUS, 0, 180);
                break;

            default:
                Logging_log(ERROR, "Invalid StatusLight value!");
            }
        }

#if 0
        if(Var_poked("Solenoid.0")) {
            send_message(sp, SW_SOLENOID, SOLENOID1, (int) Var_get("Solenoid.0"));
        }

        if(Var_poked("Solenoid.1")) {
            send_message(sp, SW_SOLENOID, SOLENOID2, (int) Var_get("Solenoid.1"));
        }

        if(Var_poked("Solenoid.2")) {
            send_message(sp, SW_SOLENOID, SOLENOID3, (int) Var_get("Solenoid.2"));
        }

        if(Var_poked("Servo.0")) {
            send_message(sp, SW_SERVO, SERVO1, (int) Var_get("Servo.0"));
        }

        if(Var_poked("Servo.1")) {
            send_message(sp, SW_SERVO, SERVO2, (int) Var_get("Servo.1"));
        }
#endif
    }

    Serial_closePort(sp);
    Seawolf_close();

    return 0;
}
