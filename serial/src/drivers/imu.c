//#define debug

#include "seawolf.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>

#define FIELD(buff, i)         ((short)((((buff)[(i-1)]) << 8) | ((buff)[(i)])))
#define UFIELD(buff, i)        ((unsigned short)FIELD((buff), (i)))
#define CHECKSUM_FIELD(buff)   ((int)UFIELD(buff, 10))
#define COMPUTE_CHECKSUM(buff) ((int)((UFIELD(buff, 2) + UFIELD(buff, 4) + UFIELD(buff, 6) + UFIELD(buff, 8) + 0x0D) & ((1 << 16) - 1)))

#define ERROR_THRESHOLD 10
#define SUM_SIZE        2

int main(int argc, char** argv) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    SeaSQL_setAutoNotify(false);
    Seawolf_init("Serial : IMU");

    char* device_real = argv[1];
    unsigned char imu_buff[32];
    SerialPort sp = Serial_open(device_real);

    /* Running sum variables */
    float val_roll[SUM_SIZE], val_pitch[SUM_SIZE], val_yaw[SUM_SIZE];
    int sum_roll = 0, sum_pitch = 0;
    double sum_yaw[] = {0.0, 0.0};
    int i, checksum_error;

    /* Zero arrays */
    memset(val_roll, 0, sizeof(int) * SUM_SIZE);
    memset(val_pitch, 0, sizeof(int) * SUM_SIZE);
    memset(val_yaw, 0, sizeof(int) * SUM_SIZE);

    Serial_setBaud(sp, 38400);
    tcflush(sp, TCIOFLUSH);
    
    i = 0;
    while(true) {
        /* Instantatious Euler Angles */
        Serial_sendByte(sp, 0x0D);
        Serial_get(sp, imu_buff, 11);
        checksum_error = CHECKSUM_FIELD(imu_buff) - COMPUTE_CHECKSUM(imu_buff);
        if(abs(checksum_error) > ERROR_THRESHOLD) {
            Logging_log(ERROR, Util_format("Received corrupt data from IMU (%d).  Pausing for 2 seconds", checksum_error));
            //Util_usleep(0.5);
            //continue;
        }

        /* Subtract old values */
        sum_roll -= val_roll[i];
        sum_pitch -= val_pitch[i];

        /* Store new gyro-stabilized euler angles values */
        val_roll[i] = FIELD(imu_buff, 2);
        val_pitch[i] = FIELD(imu_buff, 4);
        val_yaw[i] = FIELD(imu_buff, 6);

        /* Rescale */
        val_roll[i] = ((float)val_roll[i]*360) / 65535;
        val_pitch[i] = ((float)val_pitch[i]*360) / 65535;
        val_yaw[i] = ((float)val_yaw[i]*360) / 65535;
        //Logging_log(DEBUG, Util_format("==== %d", val_yaw[i]));

	#ifdef debug
        printf("\nYaw: %+4.2f", val_yaw[i]);
	fflush(NULL);
	#endif

	/* Invert sign */
        val_roll[i] *= -1;
        val_pitch[i] *= -1;
        val_yaw[i] *= -1;

        /* Add in new points */
        sum_roll += val_roll[i];
        sum_pitch += val_pitch[i];

        /* Send data out */
        SeaSQL_setSEA_Roll((float)sum_roll/SUM_SIZE);
        SeaSQL_setSEA_Pitch((float)sum_pitch/SUM_SIZE);

        sum_yaw[0] = 0;
        sum_yaw[1] = 0;
        for(int j = 0; j < SUM_SIZE; j++) {
            sum_yaw[0] += cos((M_PI / 180.0) *(float)val_yaw[j]);
            sum_yaw[1] += sin((M_PI / 180.0) *(float)val_yaw[j]);
        }
        sum_yaw[0] /= SUM_SIZE;
        sum_yaw[1] /= SUM_SIZE;
        
	#ifdef debug
	printf("\t%+4.2f",sum_yaw[0]);
	printf("\t%+4.2f",sum_yaw[1]);	
	#endif

	if(sum_yaw[0]>=0 && sum_yaw[1]>=0)
	{
		SeaSQL_setSEA_Yaw(-(180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0]));
		#ifdef debug
		printf("\t%+4.2f",-(float)(180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0]));
		#endif	
	}
	else if(sum_yaw[0]>=0 && sum_yaw[1]<0)
	{
		SeaSQL_setSEA_Yaw(-(180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0]));
		#ifdef debug
		printf("\t%+4.2f",-(float)(180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0]));
		#endif
	}
	else if(sum_yaw[0]<0 && sum_yaw[1]<0)
	{
		SeaSQL_setSEA_Yaw(180.0-((180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0])));
		#ifdef debug
		printf("\t%+4.2f",(float)(180.0-(180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0])));
		#endif
	}
	else if(sum_yaw[0]<0 && sum_yaw[1]>=0)
	{
		SeaSQL_setSEA_Yaw( -((180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0])+180.0)  );
		#ifdef debug
		printf("\t%+4.2f", -((float)(180.0 / M_PI) * atan((float)sum_yaw[1] / (float)sum_yaw[0])+180.0)  );
		#endif
	}


	#ifdef debug
	printf("\t%4.2f",SeaSQL_getSEA_Yaw());
        #endif
	Notify_send("UPDATED", "IMU");

	

        i = (i+1) % SUM_SIZE;

        Util_usleep(0.2);
    }

    Serial_closePort(sp);
    
    Logging_log(INFO, "IMU Controller Exiting");

    Seawolf_close();
    return 0;
}
