
#include <sw.h>

enum DepthState {
    NOT_RUNNING = 0,
    BYTE1 = 1,
    BYTE2 = 2
};

static enum DepthState depth_state = NOT_RUNNING;
static char depth_message[3] = {SW_DEPTH, 0, 0};

/* Temperature */
ISR(ADCA_CH1_vect) {
    char message[3];

    message[0] = SW_TEMP;
    message[1] = ADCA.CH1.RESH;
    message[2] = ADCA.CH1.RESL;

    serial_send_bytes(message, 3);
}

static bool twi_is_error(void) {
    uint8_t status;
    bool rxack;
    bool arblost;
    bool rif;
    bool wif;
    bool buserr;

    status = TWIE.MASTER.STATUS;

    rxack =  (status & TWI_MASTER_RXACK_bm) != 0;
    arblost = (status & TWI_MASTER_ARBLOST_bm) != 0;
    buserr = (status & TWI_MASTER_BUSERR_bm) != 0;
    rif = (status & TWI_MASTER_RIF_bm) != 0;
    wif = (status & TWI_MASTER_WIF_bm) != 0;

    if((wif && arblost) || (wif && rxack) || buserr) {
        return true;
    } else if(rif && !rxack) {
        return false;
    }

    return true;
}

static void twi_error(void) {
    char message[3];

    message[0] = SW_ERROR;
    message[1] = TWI_ERROR;
    message[2] = TWIE.MASTER.STATUS;

    serial_send_bytes(message, 3);
}

ISR(TWIE_TWIM_vect) {
    if(twi_is_error()) {
        twi_error();
        depth_state = NOT_RUNNING;
        return;
    }

    switch(depth_state) {
    case NOT_RUNNING:
        return;

    case BYTE1:
        depth_message[1] = TWIE.MASTER.DATA;
        TWIE.MASTER.CTRLC = TWI_MASTER_CMD_RECVTRANS_gc;
        depth_state = BYTE2;
        break;

    case BYTE2:
        depth_message[2] = TWIE.MASTER.DATA;
        TWIE.MASTER.CTRLC = TWI_MASTER_CMD_STOP_gc | TWI_MASTER_ACKACT_bm;
        serial_send_bytes(depth_message, 3);
        depth_state = NOT_RUNNING;
        break;
    }
}

void start_depth_reading(void) {
    char message[3];

    message[0] = SW_DEPTH;
    message[1] = 0;
    message[2] = 0;

    /* Force bus to idle */
    TWIE.MASTER.STATUS = TWI_MASTER_BUSSTATE_IDLE_gc;

    /* Set state */
    depth_state = BYTE1;

    /* Start transmission */
    TWIE.MASTER.ADDR = 0x9b;
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
    TWIE.MASTER.CTRLA = TWI_MASTER_INTLVL_LO_gc | TWI_MASTER_RIEN_bm | TWI_MASTER_WIEN_bm | TWI_MASTER_ENABLE_bm;

    /* Enable ADC */
    ADCA.CTRLA |= ADC_ENABLE_bm;
}
