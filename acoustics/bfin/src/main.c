
/*      -- Debug levels --
 * 0 - No debug output (run silently)
 * 1 - Output delays only
 * 2 - Give feedback on processing stages
 * 3 - Dump FIR data
 * 4 - Run full channel dumps and exit after one run
 */
#define ACOUSTICS_DEBUG 2
#define ACOUSTICS_PROFILE

#include "seawolf.h"

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <filter.h>
#include <math_bf.h>
#include <complex_bf.h>

#include "acoustics.h"

/* Data source address in async back 2 */
static adcsample* last_addr = (adcsample*) 0x00;

/* Circular buffer state */
static adcsample* cir_buff[4];
static unsigned int cir_buff_offset;

/* FIR Coefficients */
static fract16* coefs;

/* FIR Filter States */
static fir_state_fr16 fir_state[4];
static fir_state_fr16 fir_state_trig;

/* FIR delay lines */
static fract16* fir_delay[4];
static fract16* fir_delay_trig;

/* Twiddle table for correlations */
static complex_fract16* tt;

/* FFT buffers for correlation */
static complex_fract16* fft_ref;
static complex_fract16* fft_temp;
static complex_fract16* cmplx_buff;
static int block_exponent;

/* Signal delays */
static int delay_AB;
static int delay_AC;
static int delay_AD;

/* Misc */
static unsigned int i;
static adcsample* temp_buff;

static void init(char* coefs_file_name) {
    /* Load coefficients from .cof file */
    coefs = calloc(sizeof(adcsample), FIR_COEF_COUNT);
    load_coefs(coefs, coefs_file_name, FIR_COEF_COUNT );

    /* Initialize delay lines for FIR filters */
    fir_delay[A] = calloc(sizeof(adcsample), FIR_COEF_COUNT);
    fir_delay[B] = calloc(sizeof(adcsample), FIR_COEF_COUNT);
    fir_delay[C] = calloc(sizeof(adcsample), FIR_COEF_COUNT);
    fir_delay[D] = calloc(sizeof(adcsample), FIR_COEF_COUNT);
    fir_delay_trig = calloc(sizeof(adcsample), FIR_COEF_COUNT);

    /* FIR state macros */
    fir_init(fir_state[A], coefs, fir_delay[A], FIR_COEF_COUNT, 0);
    fir_init(fir_state[B], coefs, fir_delay[B], FIR_COEF_COUNT, 0);
    fir_init(fir_state[C], coefs, fir_delay[C], FIR_COEF_COUNT, 0);
    fir_init(fir_state[D], coefs, fir_delay[D], FIR_COEF_COUNT, 0);
    fir_init(fir_state_trig, coefs, fir_delay_trig, FIR_COEF_COUNT, 0);

    /* Circular buffers per channel */
    cir_buff[A] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cir_buff[B] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cir_buff[C] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);
    cir_buff[D] = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL);

    /* Twiddle table for use in optimized correlation block */
    tt = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL / 2);

    /* Intialize twiddle table */
    twidfftrad2_fr16(tt, BUFFER_SIZE_CHANNEL);

    /* Initialize fft output buffers for use in correlation block */
    fft_ref = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
    fft_temp = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
    cmplx_buff = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);

    /* Temporary buffer used in linearization of circular buffers, to store
       output of the FIR filter applied to trigger samples, and to store the
       result from correlation */
    temp_buff = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL * 2);
}

/* Move input data from the FPGA into the circular buffers until a trigger is
   located */
static void record_ping(void) {
    int state = READING;
    unsigned int extra_reads = EXTRA_READS;
    bool cir_buff_full = false;

    /* Reset state */
    cir_buff_offset = 0x00;
    RESET_FLAG = 1;
    
#if ACOUSTICS_DEBUG >= 2
    printf("Waiting for trigger...");
    fflush(stdout);
#endif
    
    while(state != DONE) {
        while(DATA_ADDR == last_addr) {
            /* Wait for the address pointer to change */
        }
        last_addr = DATA_ADDR;
        
#if ACOUSTICS_DEBUG >= 2
        printf(".");
        fflush(stdout);
#endif

        /* Copy data out of the FPGA */
        memcpy(cir_buff[A] + cir_buff_offset, last_addr + (0 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
        memcpy(cir_buff[B] + cir_buff_offset, last_addr + (1 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
        memcpy(cir_buff[C] + cir_buff_offset, last_addr + (2 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
        memcpy(cir_buff[D] + cir_buff_offset, last_addr + (3 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
        
        /* Don't look for a trigger until the buffer has been filled */
        if(state == READING && cir_buff_full) {
            /* Run the FIR filter on the current sample from channel A */
            fir_fr16(cir_buff[A] + cir_buff_offset, temp_buff, SAMPLES_PER_CHANNEL, &fir_state_trig);
            
            /* for(i = SAMPLES_PER_CHANNEL / 2; i < SAMPLES_PER_CHANNEL; i++) { */
            for(i = 0; i < SAMPLES_PER_CHANNEL; i++) {
                if(temp_buff[i] > TRIGGER_VALUE ) {
                    state = TRIGGERED;
                    break;
                }
            }
        }
        
        /* Increment the offset into the circular buffer -- if we are back
           to 0 then set the buffer as filled to indicate that we have a
           full buffers worth of data */
        cir_buff_offset = (cir_buff_offset + SAMPLES_PER_CHANNEL) % BUFFER_SIZE_CHANNEL;
        if(cir_buff_offset == 0x00) {
            cir_buff_full = true;
        }
        
        /* Handle padding once triggered */
        if(state == TRIGGERED) {
            if(extra_reads > 0) {
                extra_reads--;
            } else {
                state = DONE;
            }
        }
        
        /* Tell the FPGA we are ready again */
        READY_FLAG = 1;
    }

#if ACOUSTICS_DEBUG >= 2
    printf("done\n");
#endif
}

static void linearize_buffers(void) {
    /* Linearize each circular buffer using a temporary buffer. Output is
       stored back into the circular buffer space */
    memcpy(temp_buff, cir_buff[A] + cir_buff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cir_buff_offset));
    memcpy(temp_buff + (BUFFER_SIZE_CHANNEL - cir_buff_offset), cir_buff[A], sizeof(adcsample) * cir_buff_offset);
    memcpy(cir_buff[A], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    
    memcpy(temp_buff, cir_buff[B] + cir_buff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cir_buff_offset));
    memcpy(temp_buff + (BUFFER_SIZE_CHANNEL - cir_buff_offset), cir_buff[B], sizeof(adcsample) * cir_buff_offset);
    memcpy(cir_buff[B], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    
    memcpy(temp_buff, cir_buff[C] + cir_buff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cir_buff_offset));
    memcpy(temp_buff + (BUFFER_SIZE_CHANNEL - cir_buff_offset), cir_buff[C], sizeof(adcsample) * cir_buff_offset);
    memcpy(cir_buff[C], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    
    memcpy(temp_buff, cir_buff[D] + cir_buff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cir_buff_offset));
    memcpy(temp_buff + (BUFFER_SIZE_CHANNEL - cir_buff_offset), cir_buff[D], sizeof(adcsample) * cir_buff_offset);
    memcpy(cir_buff[D], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
}

static void filter_buffers(void) {
    /* Apply FIR filter to each buffer */
    fir_fr16(cir_buff[A], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[A]);
    memcpy(cir_buff[A], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    
    fir_fr16(cir_buff[B], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[B]);
    memcpy(cir_buff[B], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    
    fir_fr16(cir_buff[C], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[C]);
    memcpy(cir_buff[C], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    
    fir_fr16(cir_buff[D], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[D]);
    memcpy(cir_buff[D], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
}

static void correlate_buffers(void) {
    /*** TEMPORARY OPTIMIZED CORRELATION COMPUTATION. THIS NEEDS CLEAN UP ***/
    rfft_fr16(cir_buff[A], fft_ref, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    conjugate(fft_ref, BUFFER_SIZE_CHANNEL);
    
    rfft_fr16(cir_buff[B], fft_temp, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    multiply(fft_ref, fft_temp, fft_temp, BUFFER_SIZE_CHANNEL);
    ifft_fr16(fft_temp, cmplx_buff, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    delay_AB = find_max_cmplx(cmplx_buff, BUFFER_SIZE_CHANNEL);
    
    rfft_fr16(cir_buff[C], fft_temp, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    multiply(fft_ref, fft_temp, fft_temp, BUFFER_SIZE_CHANNEL);
    ifft_fr16(fft_temp, cmplx_buff, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    delay_AC = find_max_cmplx(cmplx_buff, BUFFER_SIZE_CHANNEL);
    
    rfft_fr16(cir_buff[D], fft_temp, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    multiply(fft_ref, fft_temp, fft_temp, BUFFER_SIZE_CHANNEL);
    ifft_fr16(fft_temp, cmplx_buff, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 1);
    delay_AD = find_max_cmplx(cmplx_buff, BUFFER_SIZE_CHANNEL);
}

static void data_out(void) {
#ifdef USE_LIBSEAWOLF
    Var_set("Acoustics.Delays.AB", delay_AB);
    Var_set("Acoustics.Delays.AC", delay_AC);
    Var_set("Acoustics.Delays.AD", delay_AD);
#endif
    
#if ACOUSTICS_DEBUG >= 1
    /* Output pDelay values */
    printf("delay_AB: %d \n", delay_AB);
    printf("delay_AC: %d \n", delay_AC);
    printf("delay_AD: %d \n", delay_AD);
#endif
}

int main(int argc, char** argv) {
#ifdef USE_LIBSEAWOLF
    Seawolf_loadConfig("seawolf.conf");
    Seawolf_init("Blackfin");
#endif

#ifdef ACOUSTICS_PROFILE
    /* Timer for profiling */
    Timer* t = Timer_new();
#endif

    /* Missing coefficients file argument */
    if(argc <= 1) {
        printf("Missing required argument. Please provide a FIR filter coefficients file\n");
        exit(1);
    }
    
    /* Initialize all data structures */
    init(argv[1]);

    while(true) {
        record_ping();

        TIME_PRE(t, "Linearizing buffers...");
        linearize_buffers();
        TIME_POST(t);

        TIME_PRE(t, "Filtering buffers...");
        filter_buffers();
        TIME_POST(t);

        TIME_PRE(t, "Correlating buffers...");
        correlate_buffers();
        TIME_POST(t);

        data_out();
    }

    /* Free all allocated buffers */
    free(coefs);
    free(fir_delay[A]);
    free(fir_delay[B]);
    free(fir_delay[C]);
    free(fir_delay[D]);
    free(fir_delay_trig);
    free(cir_buff[A]);
    free(cir_buff[B]);
    free(cir_buff[C]);
    free(cir_buff[D]);
    free(temp_buff);

#ifdef USE_LIBSEAWOLF
    Seawolf_close();
#endif

    return 0;
}
