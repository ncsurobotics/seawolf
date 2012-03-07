
#include <string.h>
#include <stdint.h>

#include <sw.h>

static volatile bool depth_enabled = false;

void long_delay(float seconds) {
    unsigned int n = seconds * (1000 / 50);

    for(unsigned int i = 0; i < n; i++) {
        _delay_ms(50);
    }
}

void enable_interrupts(void) {
    /* Enable all interrupt levels */
    PMIC.CTRL |= 0x07;

    /* Enable interrupts globally */
    sei();
}

void software_reset(void) {
    CCP = CCP_IOREG_gc;
    RST.CTRL = 0x01;
}

void send_depth(void) {
    if(depth_enabled) {
        serial_print("Hello\n");
    }
}

void main(void) {
    uint8_t command[2];

    /* Lock clock. Default clock rate of 2Mhz */
    CLK.LOCK = 1;

    init_servos();
    init_motors();
    init_serial();

    enable_interrupts();

    /* Send 0xFF until 0x00 is received */
    while(true) {
        serial_send_byte(0xFF);

        if(serial_available() && serial_read_byte() == 0x00) {
            break;
        }
    }

    serial_send_byte(0xF0);
    depth_enabled = true;

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
        }
    }
}
