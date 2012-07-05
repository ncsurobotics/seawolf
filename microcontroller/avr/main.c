
#include <string.h>
#include <stdint.h>

#include <sw.h>

static int kill_status = -1;

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
        serial_send_byte(0xff);

        if(serial_available() && serial_read_byte() == 0x00) {
            break;
        }
    }

    if(serial_available()) {
        char command[3] = {
            SW_ERROR,
            SYNC_ERROR,
            0
        };

        serial_send_bytes(command, 3);
    }

    serial_send_byte(0xf0);
}

void check_batteries(void) {
    char message[3];

    message[0] = SW_BATTERY;
    message[2] = 0;

    if((PORTB.IN & 0x1) == 0) {
        message[1] = SLA2;
        serial_send_bytes(message, 3);
    }

    if((PORTB.IN & 0x2) == 0) {
        message[1] = SLA1;
        serial_send_bytes(message, 3);
    }

    if((PORTB.IN & 0x8) == 0) {
        message[1] = LIPO;
        serial_send_bytes(message, 3);
    }
}

void check_kill(void) {
    int stat = (PORTB.IN & 0x4) >> 2;
    char message[3];

    message[0] = SW_KILL;
    message[1] = 0;

    if(stat != kill_status) {
        kill_status = stat;
        message[2] = kill_status;
        serial_send_bytes(message, 3);
    }
}

static void invalid_request(char command) {
    char message[3];

    message[0] = SW_ERROR;
    message[1] = INVALID_REQUEST;
    message[2] = command;

    serial_send_bytes(message, 3);
}

int main(void) {
    char command[3];

    /* Enable 32Mhz clock and wait for it to be ready */
    OSC.CTRL |= OSC_RC32MEN_bm;
    while((OSC.STATUS & OSC_RC32MRDY_bm) == 0x00);

    /* Set clock to 32Mhz and then lock it */
    CCP = CCP_IOREG_gc;
    CLK.CTRL = CLK_SCLKSEL_RC32M_gc;
    CLK.LOCK = CLK_LOCK_bm;

    init_servos();
    init_solenoids();
    init_motors();
    init_serial();
    init_analog();
    init_status();

    PORTB.DIRCLR = 0x0f;

    enable_interrupts();

    synchronize_comm();

    /* Wait until after initializing the serial link to start sending depth and
       temperature information */
    init_scheduler();

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

        case SW_SOLENOID:
            set_solenoid(command[1], command[2]);

        case SW_STATUS:
            set_status((unsigned char)command[2]);
            break;

        case SW_TEMP:
            ADCA.CH1.CTRL |= ADC_CH_START_bm;
            break;

        default:
            invalid_request(command[0]);
            realign_buffer();
            break;
        }
    }

    return 0;
}
