
#include <sw.h>

static volatile int counter = 0;

/* 100 Hz timer */
ISR(TCC0_OVF_vect) {
    /* Increment counter, roll over at 1000 (once every 10 seconds) */
    counter = (counter + 1) % 1000;

    /* Send depth at 10 Hz */
    if(counter % 10 == 0) {
        start_depth_reading();
    }

    /* Send temperature once a second */
    if(counter % 100 == 0) {
        ADCA.CH1.CTRL |= ADC_CH_START_bm;
    }

    /* Check batteries every 5 seconds */
    if(counter % 500 == 0) {
        check_batteries();
    }

    /* Check kill status every 100ms */
    if(counter % 10) {
        check_kill();
    }

    update_status(counter);
}

void init_scheduler(void) {
    /* Enable timer 0 on port C. Run timer at 1/64 system clock (500kHz) */
    TCC0.CTRLA = TC_CLKSEL_DIV64_gc;
    TCC0.CTRLB = TC_WGMODE_SS_gc;

    /* Run at frequency of 100 Hz */
    TCC0.PER = 5000;

    /* Enable overflow interrupt at low level */
    TCC0.INTCTRLA = TC_OVFINTLVL_LO_gc;
}
