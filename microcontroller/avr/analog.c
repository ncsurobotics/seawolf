
#include <sw.h>

static volatile int counter = 0;

/* Depth */
ISR(ADCA_CH0_vect) {
    char message[3];

    message[0] = SW_DEPTH;
    message[1] = ADCA.CH0.RESH;
    message[2] = ADCA.CH0.RESL;

    serial_send_bytes(message, 3);
}

/* Temperature */
ISR(ADCA_CH1_vect) {
    char message[3];

    message[0] = SW_TEMP;
    message[1] = ADCA.CH1.RESH;
    message[2] = ADCA.CH1.RESL;

    serial_send_bytes(message, 3);
}

/* 100 Hz timer */
ISR(TCC0_OVF_vect) {
    /* Increment counter, roll over at 100 (once a second) */
    counter = (counter + 1) % 100;

    /* Send depth at 10 Hz */
    if(counter % 10 == 0) {
        ADCA.CH0.CTRL |= ADC_CH_START_bm;
    }

    /* Send temperature once a second */
    if(counter % 100 == 0) { 
        ADCA.CH1.CTRL |= ADC_CH_START_bm;
    }
}

void init_analog(void) {
    /* Set signed mode */
    ADCA.CTRLB = ADC_CONMODE_bm;

    /* Select 1V internal vref as voltage reference for ADC and enable
       temperature reference */
    ADCA.REFCTRL = ADC_REFSEL_INT1V_gc | ADC_TEMPREF_bm;
    
    /* Set ADC frequency of 2MHz / 256 */
    ADCA.PRESCALER = ADC_PRESCALER_DIV256_gc;
    
    ADCA.CH0.CTRL = ADC_CH_INPUTMODE_SINGLEENDED_gc;
    ADCA.CH0.MUXCTRL = ADC_CH_MUXPOS_PIN0_gc;
    ADCA.CH0.INTCTRL = ADC_CH_INTLVL_LO_gc;

    ADCA.CH1.CTRL = ADC_CH_INPUTMODE_INTERNAL_gc;
    ADCA.CH1.MUXCTRL = ADC_CH_MUXINT_TEMP_gc;
    ADCA.CH1.INTCTRL = ADC_CH_INTLVL_LO_gc;

    /* Enable ADC */
    ADCA.CTRLA |= ADC_ENABLE_bm;

    /* Enable timer 0 on port C. Run timer at 1/4 system clock (500kHz) */
    TCC0.CTRLA = TC_CLKSEL_DIV4_gc;
    TCC0.CTRLB = TC_WGMODE_SS_gc;
    
    /* Run at frequency of 100 Hz */
    TCC0.PER = 5000;

    /* Enable overflow interrupt at low level */
    TCC0.INTCTRLA = TC_OVFINTLVL_LO_gc;
}
