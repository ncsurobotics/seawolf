
#include "seawolf.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>

#define FIELD(buff, i)         ((unsigned short)((((buff)[(i-1)]) << 8) | ((buff)[(i)])))
#define CHECKSUM_FIELD(buff)   ((int)FIELD(buff, 10))
#define COMPUTE_CHECKSUM(buff) ((int)((FIELD(buff, 2) + FIELD(buff, 4) + FIELD(buff, 6) + FIELD(buff, 8) + 0x0D) & ((1 << 16) - 1)))

#define ERROR_THRESHOLD  5
#define SUM_SIZE        10

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    SeaSQL_setAutoNotify(false);
    Seawolf_init("Serial : IMU");

    char* device_real = argv[1];
    unsigned char imu_buff[32];
    SerialPort sp = Serial_open(device_real);

    /* Running sum variables */
    int val_roll[SUM_SIZE], val_pitch[SUM_SIZE], val_yaw[SUM_SIZE];
    int sum_roll = 0, sum_pitch = 0, sum_yaw = 0;
    int i = 0;
    int checksum_error;

    /* Zero arrays */
    memset(val_roll, 0, sizeof(int) * SUM_SIZE);
    memset(val_pitch, 0, sizeof(int) * SUM_SIZE);
    memset(val_yaw, 0, sizeof(int) * SUM_SIZE);

    Serial_setBaud(sp, 38400);
    Serial_flush(sp);

    /* Set continuous mode and discard the response */
    Serial_sendByte(sp, 0x10);
    Serial_sendByte(sp, 0x00);
    Serial_sendByte(sp, 0x0D);

    /* Align data read */
    while(true) {
        Serial_get(sp, imu_buff, 11);
        checksum_error = CHECKSUM_FIELD(imu_buff) - COMPUTE_CHECKSUM(imu_buff);
        if(imu_buff[0] == 0x0D) {
            Logging_log(DEBUG, "Zoom");
        }
        if(imu_buff[0] != 0x0D || checksum_error) {
            /* Shift by one */
            Serial_getByte(sp);
        } else {
            Logging_log(DEBUG, "Properly aligned");
            break;
        }
    }
    
    while(true) {
        /* Instantatious Euler Angles */
        Serial_get(sp, imu_buff, 11);
        checksum_error = CHECKSUM_FIELD(imu_buff) - COMPUTE_CHECKSUM(imu_buff);
        if(abs(checksum_error) > ERROR_THRESHOLD) {
            Logging_log(ERROR, Util_format("Received corrupt data from IMU (%d).  Pausing for 2 seconds", checksum_error));
            Util_usleep(2);
            continue;
        }

        /* Subtract old values */
        sum_roll -= val_roll[i];
        sum_pitch -= val_pitch[i];
        sum_yaw -= val_yaw[i];

        /* Store new gyro-stabilized euler angles values */
        val_roll[i] = FIELD(imu_buff, 2);
        val_pitch[i] = FIELD(imu_buff, 4);
        val_yaw[i] = FIELD(imu_buff, 6);

        /* Rescale */
        val_roll[i] = (val_roll[i]*360) / 65535;
        val_pitch[i] = (val_pitch[i]*360) / 65535;
        val_yaw[i] = (val_yaw[i]*360) / 65535;

        /* Make signed */
        if(val_roll[i] > 180) {
            val_roll[i] -= 360;
        }
        if(val_pitch[i] > 180) {
            val_pitch[i] -= 360;
        }
        if(val_yaw[i] > 180) {
            val_yaw[i] -= 360;
        }

        /* Invert sign */
        val_roll[i] *= -1;
        val_pitch[i] *= -1;
        val_yaw[i] *= -1;

        /* Add in new points */
        sum_roll += val_roll[i];
        sum_pitch += val_pitch[i];
        sum_yaw += val_yaw[i];

        /* Send data out */
        SeaSQL_setSEA_Roll((float)sum_roll/SUM_SIZE);
        SeaSQL_setSEA_Pitch((float)sum_pitch/SUM_SIZE);
        SeaSQL_setSEA_Yaw((float)sum_yaw/SUM_SIZE);
        Notify_send("UPDATED", "IMU");

        i = (i+1) % SUM_SIZE;
    }

    Serial_closePort(sp);
    
    Logging_log(INFO, "IMU Controller Exiting");

    Seawolf_close();
    return 0;
}
