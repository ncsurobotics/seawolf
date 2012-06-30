
#include <string.h>
#include <stdint.h>

#include <sw.h>

static volatile bool depth_enabled = false;

void enable_interrupts(void) {
    /* Enable all interrupt levels */
    PMIC.CTRL |= (PMIC_HILVLEN_bm | PMIC_MEDLVLEN_bm | PMIC_LOLVLEN_bm);

    /* Enable interrupts globally */
    sei();
}

void software_reset(void) {
    CCP = CCP_IOREG_gc;
    RST.CTRL = RST_SWRST_bm;
}

/* Synchronize with computer. Send a stream of 0xff bytes until a 0x00 byte is
   received. Terminate synchronization by sending 0xf0 */
void synchronize_comm(void) {
    /* Send 0xFF until 0x00 is received */
    while(true) {
        serial_send_byte(0xFF);

        if(serial_available() && serial_read_byte() == 0x00) {
            break;
        }
    }

    serial_send_byte(0xF0);
    depth_enabled = true;
}

int main(void) {
    char command[3];

    /* Lock clock. Default clock rate of 2Mhz */
    CLK.LOCK = CLK_LOCK_bm;

    init_servos();
    init_motors();
    init_serial();

    enable_interrupts();

    synchronize_comm();

    /* Wait until after initializing the serial link to start sending depth and
       temperature information */
    init_analog();

    while(true) {
        serial_read_bytes(command, 3);

        switch(command[0]) {
        case SW_RESET:
            software_reset();
            break;

        case SW_NOP:
            break;

        case SW_MOTOR:
            set_motor_speed(command[1], command[2]);
            break;

        case SW_SERVO:
            set_servo_position(command[1], command[2]);
            break;

        case SW_STATUS:
            // send_status();
            break;

        case SW_TEMP:
            ADCA.CH1.CTRL |= ADC_CH_START_bm;
            break;
        }
    }

    return 0;
}
