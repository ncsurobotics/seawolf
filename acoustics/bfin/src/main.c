
/*      -- Debug levels --
 * 0 - No debug output (run silently)
 * 1 - Output delays only
 * 2 - Give feedback on processing stages
 * 3 - Dump FIR data
 * 4 - Run full channel dumps and exit after one run
 */
#define ACOUSTICS_DEBUG 2

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

#include "acoustics_math.h"
#include "csv_io.h"

/* A sample from the FPGA/ADC is 16 bits */
typedef fract16 adcsample;

/* Asychronous banks */
#define BANK_0 0x20000000
#define BANK_1 0x20100000
#define BANK_2 0x20200000
#define BANK_3 0x20300000

/* Channels */
#define A 0
#define B 1
#define C 2
#define D 3

/* Data source locations */
#define DATA_ADDR  (*((adcsample**)BANK_2))
#define READY_FLAG (*(((adcsample*)BANK_2) + 1))
#define RESET_FLAG (*(((adcsample*)BANK_2) + 3))

/* Input data configuration */
#define CHANNELS 4
#define SAMPLES_PER_CHANNEL (8 * 1024)
#define SAMPLES_PER_BANK    (CHANNELS * SAMPLES_PER_CHANNEL)

/* Size of a circular buffer for a single channel. This is populated in
   increments of SAMPLES_PER_CHANNEL */
//#define BUFFER_SIZE_CHANNEL (512 * 1024)
#define BUFFER_SIZE_CHANNEL (128 * 1024)

/* FIR filter coefficient count */
#define FIR_COEF_COUNT 613

/* Value to trigger on */
#define TRIGGER_VALUE ((short)(-1100))
#define UN_FREQ 1728 /* Unnormalized Frequency to look for (1728 = 27kHz / 64kHz * 4096 samples) */
#define THRESH_LEVEL 0x0120

/* Circular buffer state */
#define READING   0x00
#define TRIGGERED 0x01
#define DONE      0x02

/* Extra number of read cyles to perform after trigger. This can be used to
   "pad" the other channels and ensure that the trigger is present in all
   channels */
#define EXTRA_READS 4

/* Specify samples to start and end dump at */
#define START_DUMP 4096
#define DUMP_SIZE  1048576
#define END_DUMP   (START_DUMP + DUMP_SIZE)

/* Dump channel buffer to CSV file */
#if ACOUSTICS_DEBUG >= 4
static void dump(const char* fname, adcsample* n) {
    FILE* f = fopen(fname, "w");
    for(int i = START_DUMP; i < END_DUMP; i++) {
        fprintf(f, "%.5f\n", n[i] / ((float)(1 << 15)));
    }
    fclose(f);
}
#endif

#if 0
static int my_atoi(const char* s) {
    int n = 0;

    while(isspace(*s)) {
        s++;
    }

    while(isdigit(*s) && *s != '\0') {
        n = (n * 10) + ((*s) - '0');
        s++;
    }

    return n;
}
#endif

/* Pull in coefficient values from a file */
static void load_coefs(fract16* coefs, char* coef_file_name, int num_coefs) {
    FILE* f;
    char buff[256];

    /* Open file */
    f = fopen(coef_file_name, "r");

    if(f == NULL) {
        printf("Could not open coefficients file: %s\n", coef_file_name);
        exit(1);
    }

    /* Read coefficients */
    for(int i = 0; i < num_coefs; i++) {
        fgets(buff, 255, f);
        coefs[i] = atoi(buff);
    }

    /* Close File */
    fclose(f);
}

int main(int argc, char** argv) {
#ifdef USE_LIBSEAWOLF
    Seawolf_loadConfig("seawolf.conf");
    Seawolf_init("Blackfin");
#endif
    Timer* t = Timer_new();

    adcsample* last_addr = (adcsample*) 0x00;
    adcsample* cir_buff[4];
    adcsample* temp_buff;

    unsigned int cir_buff_offset;
    unsigned int extra_reads;
    unsigned int i;

    /* Circular buffer state */
    int state;
    bool cir_buff_full;

    /* FIR Coefficients */
    fract16* coefs;

    /* FIR Filter States */
    fir_state_fr16 fir_state[4];
    fir_state_fr16 fir_state_trig;
    
    /* FIR delay lines */
    fract16* fir_delay[4];
    fract16* fir_delay_trig;

    /* Signal delays */
    int delay_AB;
    int delay_AC;
    int delay_AD;

    /* Twiddle table for correlations */
    complex_fract16* tt;

    /* FFT buffers for correlation */
    complex_fract16* fft_ref;
    complex_fract16* fft_temp;
    complex_fract16* cmplx_buff;
    int block_exponent;

    /* Missing coefficients file argument */
    if(argc <= 1) {
        printf("Missing required argument. Please provide a FIR filter coefficients file\n");
        exit(1);
    }

    /* Load coefficients from .cof file */
    coefs = calloc(sizeof(adcsample), FIR_COEF_COUNT);
    load_coefs(coefs, argv[1], FIR_COEF_COUNT );

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

    /* Temporary buffer used in linearization of circular buffers, to store
       output of the FIR filter applied to trigger samples, and to store the
       result from correlation */
    temp_buff = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL * 2);

    /* Twiddle table for use in optimized correlation block */
    tt = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL / 2);

    /* Initialize fft output buffers */
    fft_ref = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
    fft_temp = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
    cmplx_buff = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);

    /* Intialize twiddle table */
    twidfftrad2_fr16(tt, BUFFER_SIZE_CHANNEL);

    while(true) {
        /* Reset state */
        state = READING;
        extra_reads = EXTRA_READS;
        cir_buff_full = false;
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

            /* Copy data out of the FPGA */
            memcpy(cir_buff[A] + cir_buff_offset, last_addr + (0 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
            memcpy(cir_buff[B] + cir_buff_offset, last_addr + (1 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
            memcpy(cir_buff[C] + cir_buff_offset, last_addr + (2 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);
            memcpy(cir_buff[D] + cir_buff_offset, last_addr + (3 * SAMPLES_PER_CHANNEL), sizeof(adcsample) * SAMPLES_PER_CHANNEL);

            /* Don't look for a trigger until the buffer has been filled */
            if(state == READING && cir_buff_full) {
#if ACOUSTICS_DEBUG >= 2
                printf(".");
                fflush(stdout);
#endif

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
        printf("%-30s", "Linearizing data...");
        fflush(stdout);
#endif
        Timer_reset(t);

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
        printf("%5.3f\n", Timer_getDelta(t));

#if ACOUSTICS_DEBUG >= 2
        printf("%-30s", "Running FIR filters...");
        fflush(stdout);
#endif
        Timer_reset(t);

        /* Apply FIR filter to each buffer */
        fir(cir_buff[A], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[A]);
        memcpy(cir_buff[A], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

        fir(cir_buff[B], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[B]);
        memcpy(cir_buff[B], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

        fir(cir_buff[C], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[C]);
        memcpy(cir_buff[C], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);

        fir(cir_buff[D], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[D]);
        memcpy(cir_buff[D], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
        printf("%5.3f\n", Timer_getDelta(t));

#if ACOUSTICS_DEBUG >= 2
        printf("%-30s", "Running correlation...");
        fflush(stdout);
#endif

#if 0
        /* Correlation and delay detection */
        fast_correlate(cir_buff[A], cir_buff[B], temp_buff, BUFFER_SIZE_CHANNEL);
        delay_AB = find_max(temp_buff, BUFFER_SIZE_CHANNEL);

        fast_correlate(cir_buff[A], cir_buff[C], temp_buff, BUFFER_SIZE_CHANNEL);
        delay_AC = find_max(temp_buff, BUFFER_SIZE_CHANNEL);

        fast_correlate(cir_buff[A], cir_buff[D], temp_buff, BUFFER_SIZE_CHANNEL);
        delay_AD = find_max(temp_buff, BUFFER_SIZE_CHANNEL);
#else
        Timer_reset(t);

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
        printf("%5.3f\n\n", Timer_getDelta(t));
#endif

#ifdef USE_LIBSEAWOLF
        Var_set("Acoustics.Delays.AB", delay_AB);
        Var_set("Acoustics.Delays.AC", delay_AC);
        Var_set("Acoustics.Delays.AD", delay_AD);
#endif

#if ACOUSTICS_DEBUG >= 1
        /* Output pDelay values */
        /* printf("delay_AB: %d \n", delay_AB);
           printf("delay_AC: %d \n", delay_AC);
           printf("delay_AD: %d \n", delay_AD); */
#endif
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
