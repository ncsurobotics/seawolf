
#include <string.h>
#include <stdint.h>

#include <sw.h>

static volatile bool depth_enabled = false;

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

ISR(ADCA_CH0_vect) {
    uint8_t message[3];

    message[0] = SW_DEPTH;
    message[1] = ADCA.CH0.RESH;
    message[2] = ADCA.CH0.RESL;

    serial_send_bytes(message, 3);
}

void send_depth(void) {
    if(depth_enabled) {
        /* Start conversion */
        ADCA.CH0.CTRL |= 0x80;
    }
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

void init_adc(void) {
    ADCA.REFCTRL = ADC_REFSEL_INT1V_gc;
    ADCA.PRESCALER = ADC_PRESCALER_DIV64_gc;
    
    ADCA.CH0.CTRL = ADC_CH_INPUTMODE_SINGLEENDED_gc;
    ADCA.CH0.MUXCTRL = ADC_CH_MUXPOS_PIN0_gc;
    ADCA.CH0.INTCTRL = ADC_CH_INTLVL_LO_gc;

    /* Enable ADC */
    ADCA.CTRLA |= 0x01;
}

void main(void) {
    uint8_t command[3];

    /* Lock clock. Default clock rate of 2Mhz */
    CLK.LOCK = 1;

    init_servos();
    init_motors();
    init_serial();
    init_adc();

    enable_interrupts();

    synchronize_comm();

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
            // send_temp();
            break;
        }
    }
}
