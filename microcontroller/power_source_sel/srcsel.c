
#include <msp430.h>

/* Port 1.x bits */
#define S0 0x01
#define S1 0x02
#define SRCSEL 0x04

/* Output configurations */
#define VOFF (SRCSEL)
#define VEXT (SRCSEL | S0)
#define VBATT (SRCSEL | S1)

/* Get source selection value */
#define SEL_VAL (P1IN & SRCSEL)

/* Possible source selection values */
#define SEL_EXT 0x00
#define SEL_BATT 0x04

void delay1ms(void) {
    __delay_cycles(1000);
}

void main(void) {
    int last_srcsel = 0;
    int i;
    
    /* Disable watchdog timer */
    WDTCTL = WDTPW | WDTHOLD;
    
    /* Set clock frequency to 1Mhz */
    BCSCTL1 = CALBC1_1MHZ;
    DCOCTL = CALDCO_1MHZ;
	
    /* P1.0 - Multiplexer S0
     * P1.1 - Multiplexer S1 (S2 is held high)
     * P1.2 - Source select input (pulled high internally)
     */
    P1DIR = 0x03;

    /* Enable SRCSEL internal pullup */    
    P1REN = SRCSEL;
    
    /* Turn off both voltage sources by default */
    P1OUT = VOFF;
    
    /* Get initial value of switch */
    last_srcsel = SEL_VAL;
    
    /* Delay 10 us */
    __delay_cycles(10);
    
    /* Set initial output */
    if(last_srcsel == SEL_EXT) {
        /* External power */
        P1OUT = VEXT;
    } else {
        /* Battery power */
        P1OUT = VBATT;
    }
    
    while(1) {
        if(SEL_VAL != last_srcsel) {
            /* Only switch if the pin holds its value for 250 ms */
            for(i = 0; i < 2500; i++) {
                if(SEL_VAL == last_srcsel) {
                    i = 0;
                    break;
                }
                
                __delay_cycles(100);
            }
            
            if(i > 0) {
	            /* Store new source value */
	            last_srcsel = SEL_VAL;
	            
	            if(last_srcsel == SEL_EXT) {
	                /* Switch to external power */
	                P1OUT = VOFF;
	                __delay_cycles(10);
	                P1OUT = VEXT;
	            } else {
	                /* Switch to battery power */
	                P1OUT = VOFF;
	                __delay_cycles(10);
	                P1OUT = VBATT;
	            }  
            }
        }
        
        /* Delay 1 ms */
        delay1ms();
    }
}
