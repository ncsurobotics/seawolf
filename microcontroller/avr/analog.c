
#include <sw.h>

/* Temperature */
ISR(ADCA_CH1_vect) {
    char message[3];

    message[0] = SW_TEMP;
    message[1] = ADCA.CH1.RESH;
    message[2] = ADCA.CH1.RESL;

    serial_send_bytes(message, 3);
}

void get_depth_reading(void) {
    char message[3];

    message[0] = SW_DEPTH;
    message[1] = 0;
    message[2] = 0;

    /* Force bus to idle */
    TWIE.MASTER.STATUS = TWI_MASTER_BUSSTATE_IDLE_gc;

    /* Start transmission */
    TWIE.MASTER.ADDR = 0x9b;

    /* Wait for first byte, then send an ACK */
    while((TWIE.MASTER.STATUS & TWI_MASTER_RIF_bm) == 0);
    message[1] = TWIE.MASTER.DATA;
    TWIE.MASTER.CTRLC = 0x2;

    /* Wait for second byte, then send a NACK and a STOP bit */
    while((TWIE.MASTER.STATUS & TWI_MASTER_RIF_bm) == 0);
    message[2] = TWIE.MASTER.DATA;
    TWIE.MASTER.CTRLC = 0x7;

    serial_send_bytes(message, 3);
}

void init_analog(void) {
    /* Set signed mode */
    ADCA.CTRLB = ADC_CONMODE_bm;
    ADCA.CTRLB = 0x00;

    /* Select 1V internal vref as voltage reference for ADC and enable
       temperature reference */
    ADCA.REFCTRL = ADC_REFSEL_INT1V_gc | ADC_TEMPREF_bm;

    /* Set ADC frequency of 2MHz / 256 */
    ADCA.PRESCALER = ADC_PRESCALER_DIV256_gc;

    /* Set temperature ADC channel settings */
    ADCA.CH1.CTRL = ADC_CH_INPUTMODE_INTERNAL_gc;
    ADCA.CH1.MUXCTRL = ADC_CH_MUXINT_TEMP_gc;
    ADCA.CH1.INTCTRL = ADC_CH_INTLVL_LO_gc;

    /* Enable TWI interface for communicating with the depth sensor ADC */
    TWIE.MASTER.BAUD = 5;
    TWIE.MASTER.CTRLA = TWI_MASTER_ENABLE_bm;

    /* Enable ADC */
    ADCA.CTRLA |= ADC_ENABLE_bm;

}
