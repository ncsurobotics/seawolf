
#include "seawolf.h"

#include <unistd.h>
#include <assert.h>

#define COLLECT_TIME 20 // How long to collect data (seconds)
#define CALIBRATION_TYPE 1 // 0 for 3D, 1 for 2D
/**
 * MAGNETIC_Z_COMPONENT
 * This must be a positive integer that fits into two bytes.  It is the Z
 * component of the Earth magnetic field measured in milli Gauss.  Note that
 * this value is different in San Diego and Raleigh!  This value is only used
 * in 2D calibration.
 *
 * I used this website to get the magnetic z component (remember to convert
 * nanotesla to milligauss!):
 * http://www.ngdc.noaa.gov/geomagmodels/struts/calcPointIGRF
 */
#define MAGNETIC_Z_COMPONENT 454  // Raleigh
//#define MAGNETIC_Z_COMPONENT 397  // San Diego


#define BFIELD(buff, i)        (((uint8_t*)(buff))[(i)-1])
#define SFIELD(buff, i)        ((int16_t)((((int16_t)BFIELD(buff, i)) << 8) | ((int16_t)BFIELD(buff, i+1))))
#define USFIELD(buff, i)       ((uint16_t)SFIELD(buff, i))

unsigned char init_calibration_command[] = {0x40, 0x71, 0x3E};
unsigned char collect_calibration_command[] = {0x41};
unsigned char compute_calibration_command[] = {0x42, 0x71, 0x3E};

/**
 * check_checksum
 * Computes the correct checksum and checks it with the checksum sent.
 *
 * buff - (buffer) A reply message from the IMU.
 * checksum_field_index - The byte index of the MSB of the checksum in the
 *     given buffer.  The bytes are 1 indexed.
 */
bool check_checksum(unsigned char* buff, int checksum_field_index) {
    int checksum = BFIELD(buff, 1);
    for (int i=2; i<checksum_field_index; i+=2) {
        checksum += USFIELD(buff, i);
    }
    checksum &= 0xFFFF;
    //printf("%d == %d\n", checksum, USFIELD(buff, checksum_field_index));
    return checksum == USFIELD(buff, checksum_field_index);
}

int main(int argc, char** argv) {

    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("IMU Calibration");

    if (argc < 2) {
        printf("\n");
        printf("Usage: %s <Serial Device>\n", argv[0]);
        printf("\n");
    }
    char* serial_device_string = argv[1];

    /* Data buffer */
    unsigned char imu_buff[32];

    /* Serial port device */
    SerialPort sp;

    /* Return values */
    int n;

    /* Open and initialize the serial port */
    sp = Serial_open(serial_device_string);
    if(sp == -1) {
        Logging_log(ERROR, "Could not open serial port for IMU! Exiting.");
        Seawolf_exitError();
    }
    Serial_setBlocking(sp);
    Serial_setBaud(sp, 38400);

    /* Poke the IMU and then flush input buffers */
    Serial_sendByte(sp, 0xF0);
    Util_usleep(1.0);
    Serial_flush(sp);

    /* Initialize calibration */
    n = Serial_send(sp, init_calibration_command,
        sizeof(init_calibration_command));
    if (n == -1) {
        Logging_log(ERROR, "Could not send init calibration command to IMU! Exiting.");
        Seawolf_exitError();
    }
    n = Serial_get(sp, imu_buff, 5);
    if (n == -1) {
        Logging_log(ERROR, "Could not get data from IMU after sending init calibration command! Exiting.");
        Seawolf_exitError();
    }
    if (!check_checksum(imu_buff, 4)) {
        Logging_log(ERROR, "Bad checksum recieved after sending init calibration command! Exiting.");
        Seawolf_exitError();
    }
    if (BFIELD(imu_buff, 1) != init_calibration_command[0]) {
        Logging_log(ERROR, "Bad command byte recieved after sending init calibration command! Exiting.");
        Seawolf_exitError();
    }

    /* Loop for a while collecting calibration data. */
    Timer* collecting_timer = Timer_new();
    unsigned int loop_counter = 0;
    while (Timer_getTotal(collecting_timer) < COLLECT_TIME) {

        /* Collect data from IMU */
        n = Serial_send(sp, collect_calibration_command,
            sizeof(collect_calibration_command));
        if(n == -1) {
            Logging_log(ERROR, "Could not send collect calibration command to IMU! Exiting.");
            Logging_log(ERROR, "WARNING: The IMU could still be in calibration mode.  You should power cycle it.");
            Seawolf_exitError();
        }
        n = Serial_get(sp, imu_buff, 23);
        if(n == -1) {
            Logging_log(ERROR, "Could not get data from IMU after sending collect calibration command! Exiting.");
            Logging_log(ERROR, "WARNING: The IMU could still be in calibration mode.  You should power cycle it.");
            Seawolf_exitError();
        }
        if(BFIELD(imu_buff, 1) != collect_calibration_command[0]) {
            Logging_log(ERROR, "Bad command byte recieved after sending collect calibration command! Exiting.");
            Logging_log(ERROR, "WARNING: The IMU could still be in calibration mode.  You should power cycle it.");
            Seawolf_exitError();
        }
        if(!check_checksum(imu_buff, 22)) {
            Logging_log(ERROR, "Bad checksum recieved after sending collect calibration command! Exiting.");
            Logging_log(ERROR, "WARNING: The IMU could still be in calibration mode.  You should power cycle it.");
            Seawolf_exitError();
        }

        /* Collect Data */
        int magfield_x = SFIELD(imu_buff, 2);
        int magfield_y = SFIELD(imu_buff, 4);
        int magfield_z = SFIELD(imu_buff, 6);
        int magfield_x_min = SFIELD(imu_buff, 8);
        int magfield_y_min = SFIELD(imu_buff, 10);
        int magfield_z_min = SFIELD(imu_buff, 12);
        int magfield_x_max = SFIELD(imu_buff, 14);
        int magfield_y_max = SFIELD(imu_buff, 16);
        int magfield_z_max = SFIELD(imu_buff, 18);

        printf("\n");
        printf("Magfield (x, y, z):\n");
        printf("current: (%d, %d, %d)\n",
            magfield_x, magfield_y, magfield_z);
        printf("min: (%d, %d, %d)\n",
            magfield_x_min, magfield_y_min, magfield_z_min);
        printf("max: (%d, %d, %d)\n",
            magfield_x_max, magfield_y_max, magfield_z_max);

        loop_counter++;

        Util_usleep(0.03);
    }

    /* End calibration
     * We send some extra information needs to be sent so the IMU can calibrate
     * correctly, and store the calibration values.
     */

    // z component of Earth's magnetic field in milligauss.
    unsigned char mag_z_msb = (MAGNETIC_Z_COMPONENT >> 8) & 0xFF;
    unsigned char mag_z_lsb = MAGNETIC_Z_COMPONENT & 0xFF;

    unsigned char data_to_send[] = {
        compute_calibration_command[0],
        compute_calibration_command[1],
        compute_calibration_command[2],
        CALIBRATION_TYPE,
        mag_z_msb,
        mag_z_lsb
    };
    n = Serial_send(sp, data_to_send, sizeof(data_to_send));
    if (n == -1) {
        Logging_log(ERROR, "Could not send compute calibration command to IMU! Exiting.");
        Logging_log(ERROR, "WARNING: The IMU could still be in calibration mode.  You should power cycle it.");
        Seawolf_exitError();
    }
    n = Serial_get(sp, imu_buff, 11);
    if (n == -1) {
        Logging_log(ERROR, "Could not get data from IMU after sending compute calibration command! Exiting.");
        Seawolf_exitError();
    }
    if (!check_checksum(imu_buff, 10)) {
        Logging_log(ERROR, "Bad checksum recieved after sending compute calibration command! Exiting.");
        Seawolf_exitError();
    }
    if (BFIELD(imu_buff, 1) != compute_calibration_command[0]) {
        Logging_log(ERROR, "Bad command byte recieved after sending compute calibration command! Exiting.");
        Seawolf_exitError();
    }

    /* Collect Data */
    int hard_iron_offset_x = SFIELD(imu_buff, 2);
    int hard_iron_offset_y = SFIELD(imu_buff, 4);
    int hard_iron_offset_z = SFIELD(imu_buff, 6);

    printf("\n");
    printf("Values stored in IMU:\n");
    printf("hard_iron_offset_x: %d\n", hard_iron_offset_x);
    printf("hard_iron_offset_y: %d\n", hard_iron_offset_y);
    printf("hard_iron_offset_z: %d\n", hard_iron_offset_z);

    Serial_closePort(sp);
    Seawolf_close();

    return 0;
}
