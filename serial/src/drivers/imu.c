
#include "seawolf.h"

#include <math.h>
#include <unistd.h>

/* Uncomment for stabilized euler angles */
//#define STABILIZED_EULER
#define SUM_SIZE 2

#define BFIELD(buff, i)        (((uint8_t*)(buff))[(i)-1])
#define SFIELD(buff, i)        ((int16_t)((((int16_t)BFIELD(buff, i)) << 8) | ((int16_t)BFIELD(buff, i+1))))
#define USFIELD(buff, i)       ((uint16_t)SFIELD(buff, i))

#define CHECKSUM_FIELD(buff)   (USFIELD(buff, 10))
#define CHECKSUM_COMPUTE(buff) ((BFIELD(buff, 1) + USFIELD(buff, 2) + USFIELD(buff, 4) + USFIELD(buff, 6) + USFIELD(buff, 8)) & 0xFFFF)

#ifdef STABILIZED_EULER
# define COMMAND_BYTE 0x0E
#else
# define COMMAND_BYTE 0x0D
#endif

#define X 0
#define Y 1

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Var_setAutoNotify(false);
    Seawolf_init("Serial : IMU");

    /* Device path */
    char* device_real = argv[1];

    /* Data buffer */
    unsigned char imu_buff[32];

    /* Serial port device */
    SerialPort sp;

    /* Running sum variables */
    double val_roll[SUM_SIZE], val_pitch[SUM_SIZE], val_yaw[SUM_SIZE];
    double sum_roll = 0, sum_pitch = 0;
    double avg_yaw[] = {0.0, 0.0};

    /* Yaw values */
    double shift;
    double base_angle;

    /* Return values */
    int n;

    /* Zero arrays */
    memset(val_roll, 0, sizeof(int) * SUM_SIZE);
    memset(val_pitch, 0, sizeof(int) * SUM_SIZE);
    memset(val_yaw, 0, sizeof(int) * SUM_SIZE);

    /* Open and initialize the serial port */
    sp = Serial_open(device_real);
    if(sp == -1) {
        Logging_log(ERROR, "Could not open serial port for IMU! Exiting.");
        Seawolf_exitError();
    }

    /* Set options */
    Serial_setBaud(sp, 38400);
    
    /* Poke the IMU and then flush input buffers */
    Serial_sendByte(sp, 0xF0);
    Util_usleep(1.0);
    Serial_flush(sp);
    
    for(int i = 0; ; i = (i+1) % SUM_SIZE) {
        /* Get data set from IMU */
        n = Serial_sendByte(sp, COMMAND_BYTE);
        if(n == -1) {
            Logging_log(ERROR, "Can not send data to IMU! Retrying in 1 second.");
            Serial_flush(sp);
            Util_usleep(1.0);
            continue;
        }
        
        n = Serial_get(sp, imu_buff, 11);
        if(n == -1) {
            Logging_log(ERROR, "Error encountered while receive response from IMU! Retrying in 1 second.");
            Serial_flush(sp);
            Util_usleep(1.0);
            continue;
        }

        /* The first byte in the response should match the command byte sent to
           the IMU */
        if(imu_buff[0] != COMMAND_BYTE) {
            Logging_log(ERROR, "Invalid command byte returned for request! Retrying.");
            Serial_flush(sp);
            Util_usleep(1.0);
            continue;
        }

        /* Verify the checksum for the data packet */
        if(CHECKSUM_FIELD(imu_buff) != CHECKSUM_COMPUTE(imu_buff)) {
            Logging_log(ERROR, Util_format("Received corrupt data from IMU (%d)! Retrying.", CHECKSUM_FIELD(imu_buff) - CHECKSUM_COMPUTE(imu_buff)));
            Serial_flush(sp);
            Util_usleep(1.0);
            continue;
        }

        /* Subtract old values from the running sum */
        sum_roll -= val_roll[i];
        sum_pitch -= val_pitch[i];

        /* Store new euler angles values into the circular buffer */
        val_roll[i] = SFIELD(imu_buff, 2);
        val_pitch[i] = SFIELD(imu_buff, 4);
        val_yaw[i] = SFIELD(imu_buff, 6);

        /* Convert the roll and pitch to degrees and the yaw to radians */
        val_roll[i] = ((float)val_roll[i]*360) / 65535;
        val_pitch[i] = ((float)val_pitch[i]*360) / 65535;
        val_yaw[i] = ((float)val_yaw[i]*2*M_PI) / 65535;

        //printf("[%d] %6.2f %6.2f %6.2f (roll, pitch, yaw)\n", i, val_roll[i], val_pitch[i], val_yaw[i]);
        printf("[%d] %6.2f %6.2f %6.2f (roll, pitch, yaw)\n", i, sum_roll, sum_pitch, val_yaw[i]);

        /* Invert sign. This reorrientates the yaw axis so that positive yaw is
           west of north and negative yaw is east of north, which while not
           intuitive, this means that yaw values increase counter clockwise, as
           they do in math. The sign of the yaw is reinverted at the end to
           maintain cardinal direction */
        val_roll[i] *= -1;
        val_pitch[i] *= -1;
        val_yaw[i] *= -1;

        /* Add in new points to the running sum */
        sum_roll += val_roll[i];
        sum_pitch += val_pitch[i];

        /* Save the average values from the running sum */
        Var_set("SEA.Roll", (float) sum_roll/SUM_SIZE );
        Var_set("SEA.Pitch", (float) sum_pitch/SUM_SIZE );

        /* Compute component averages of the yaw */
        avg_yaw[X] = 0;
        avg_yaw[Y] = 0;
        for(int j = 0; j < SUM_SIZE; j++) {
            avg_yaw[X] += cos(val_yaw[j]);
            avg_yaw[Y] += sin(val_yaw[j]);
        }
        avg_yaw[X] /= SUM_SIZE;
        avg_yaw[Y] /= SUM_SIZE;

        /* Compute base angle for yaw */
        base_angle = atan(avg_yaw[Y] / avg_yaw[X]);

        /* Determinte necessary shift for computed base */
        if(avg_yaw[X] < 0) {
            shift = M_PI * (avg_yaw[Y] < 0 ? 1 : -1);
        } else {
            shift = 0;
        }

        /* Flip the axis back and convert to degrees before saving */
        Var_set("SEA.Yaw", -1 * (180.0 / M_PI) * (base_angle - shift));

        Notify_send("UPDATED", "IMU");
        Util_usleep(0.1);
    }

    Serial_closePort(sp);
    Seawolf_close();

    return 0;
}
