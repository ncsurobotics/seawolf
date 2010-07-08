
#define ACOUSTICS_DEBUG
#define ACOUSTICS_PROFILE
//#define ACOUSTICS_CORRELATE
#define ACOUSTICS_DUMP
//#define USE_LIBSEAWOLF

#include "seawolf.h"

#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>

#include <filter.h>
#include <math_bf.h>
#include <complex_bf.h>

#include "acoustics.h"

/* Circular buffer state */
static adcsample* cir_buff[4];
static unsigned int cir_buff_offset;

/* FIR Coefficients */
static fract16* coefs;

/* File handler associated with the opened device driver /dev/ppiadc */
static int driver_f = -1;

/* Flags to be written to the control device */
static const uint8_t RESET_FLAG = 1;

/* FIR Filter States */
static fir_state_fr16 fir_state[4];
static fir_state_fr16 fir_state_trig;

/* FIR delay lines */
static fract16* fir_delay[4];
static fract16* fir_delay_trig;

#ifdef ACOUSTICS_CORRELATE

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

#else

/* Time of arrival on each channel */
static int toa[4];

#endif

/* Misc */
static unsigned int i;
static adcsample* temp_buff;

/* Allocate and initialize all data structures */
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

#ifdef ACOUSTICS_CORRELATE
    /* Twiddle table for use in optimized correlation block */
    tt = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL / 2);

    /* Intialize twiddle table */
    twidfftrad2_fr16(tt, BUFFER_SIZE_CHANNEL);

    /* Initialize fft output buffers for use in correlation block */
    fft_ref = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
    fft_temp = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
    cmplx_buff = calloc(sizeof(complex_fract16), BUFFER_SIZE_CHANNEL);
#endif

    /* Temporary buffer used in linearization of circular buffers, to store
       output of the FIR filter applied to trigger samples, and to store the
       result from correlation */
    temp_buff = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL * 2);
}

/* 
 * Interface with the PPI/ADC driver to collect a "ping" sample
 *
 * This function reads in sample blocks for each channel from the drive until
 * the circular buffer has been filled. Once the circular buffer has been filled
 * each new channel sample set is checked for the presence of the target
 * frequence. Once the signal is located the recording process is "triggered". A
 * few additional padding samples (specified by EXTRA_READS) are completed and
 * the function exits.
 */
static void record_ping(void) {
    int state = READING;
    unsigned int extra_reads = EXTRA_READS;
    bool cir_buff_full = false;
    short* current_buffer = NULL;

    /* Place write offset back to beginning of the circular buffer */
    cir_buff_offset = 0x00;
    
    /* Signal the ADC driver that we have reset (new sampling set) */
    write(driver_f, &RESET_FLAG, 1);
    
    while(state != DONE) {
        /* Wait for the ADC driver to fill a buffer and return its address */
        read(driver_f, &current_buffer, sizeof(current_buffer));

#ifdef ACOUSTICS_DEBUG
        printf(".");
        fflush(stdout);
#endif

        /* Copy data out of driver. The data stored by the driver has samples
           interleaved, so we must un-interleave them when copying them out */
        for(unsigned int i = 0, j = cir_buff_offset; i < SAMPLES_PER_CHANNEL; i++, j++) {
            cir_buff[A][j] = current_buffer[(i * CHANNELS) + (0 * sizeof(adcsample))];
            cir_buff[B][j] = current_buffer[(i * CHANNELS) + (1 * sizeof(adcsample))];
            cir_buff[C][j] = current_buffer[(i * CHANNELS) + (2 * sizeof(adcsample))];
            cir_buff[D][j] = current_buffer[(i * CHANNELS) + (3 * sizeof(adcsample))];
        }
        
        /* Don't look for a trigger until the buffer has been filled */
        if(state == READING && cir_buff_full) {
            /* Run the FIR filter on the current sample from channel A */
            fir_fr16(cir_buff[A] + cir_buff_offset, temp_buff, SAMPLES_PER_CHANNEL, &fir_state_trig);
            
            for(i = 0; i < SAMPLES_PER_CHANNEL; i++) {
                if(temp_buff[i] > TRIGGER_VALUE ) {
                    state = TRIGGERED;
                    break;
                }
            }
        }
        
        /* Increment the offset into the circular buffer -- if we are going to
           be back to 0 within EXTRA_READS then set the buffer as filled to
           indicate that we have a full buffers worth of data */
        cir_buff_offset = (cir_buff_offset + SAMPLES_PER_CHANNEL) % BUFFER_SIZE_CHANNEL;
        if(BUFFER_SIZE_CHANNEL == (EXTRA_READS * SAMPLES_PER_CHANNEL) + cir_buff_offset) {
            cir_buff_full = true;
            /* PLS REMOVE LOL */
            state = TRIGGERED;
        }
        
        /* Handle padding once triggered so that the signal will (hopefully) be
           present in all channel bufferss if it wasn't already */
        if(state == TRIGGERED) {
            if(extra_reads > 0) {
                extra_reads--;
            } else {
                state = DONE;
            }
        }
    }
}

/*
 * Linearize each circular buffer using a temporary buffer. Output is stored
 * back into the circular buffer space
 *
 * The linearization is done in three stages,
 *
 *  1. Data from the current write position to the end of the channel buffer
 *     (the oldest data) is written to the beginning of a temporary buffer
 *  2. Data from the beginning of the channel buffer to the current write
 *     position (the newest data) in the channel buffer is placed at the end
 *     of the temporary buffer
 *  3. The temporary buffer's contents are copied back to the channel buffer
 */
static void linearize_buffers(void) {
    for(int channel = A; channel <= D; channel++) {
        memcpy(temp_buff, cir_buff[channel] + cir_buff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cir_buff_offset));
        memcpy(temp_buff + (BUFFER_SIZE_CHANNEL - cir_buff_offset), cir_buff[channel], sizeof(adcsample) * cir_buff_offset);
        memcpy(cir_buff[channel], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    }
}

/* 
 * Filter each linearized buffer
 *
 * Each channel buffer is run through the FIR filter and the result is stored
 * back into the channel buffer.
 */
static void filter_buffers(void) {
    for(int channel = A; channel <= D; channel++) {
        fir_fr16(cir_buff[channel], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[channel]);
        memcpy(cir_buff[channel], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    }
}

#ifdef ACOUSTICS_CORRELATE
/*
 * Perform correlations and compute delays in the signals between the channels
 *
 * The correlation alogirthm below is based on the identity,
 *
 *    Correlation(f, g) = ifft( conj(fft(f)) * fft(g))
 *
 * Where conj(...) is the complex conjugate and '*' normal multiplication. As an
 * optimization, conj(fft(f)) is only computed once, and is reused in computing
 * the correlations and delays between each channel and a reference channel.
 * Channel A is the reference channel, and the delays AB, AC, and AD correspond
 * to the delay between A and B, A and C, and A and D respectively.
 *
 * See http://en.wikipedia.org/wiki/Cross_correlation
 */
static void correlate_buffers(void) {
    /* Compute conjugate of the FFT of channel A */
    rfft_fr16(cir_buff[A], fft_ref, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    conjugate(fft_ref, BUFFER_SIZE_CHANNEL);
    
    /* Correlate and find the delay between channels A and B */
    rfft_fr16(cir_buff[B], fft_temp, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    multiply(fft_ref, fft_temp, fft_temp, BUFFER_SIZE_CHANNEL);
    ifft_fr16(fft_temp, cmplx_buff, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    delay_AB = find_max_cmplx(cmplx_buff, BUFFER_SIZE_CHANNEL);
    
    /* Correlate and find the delay between channels A and C */
    rfft_fr16(cir_buff[C], fft_temp, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    multiply(fft_ref, fft_temp, fft_temp, BUFFER_SIZE_CHANNEL);
    ifft_fr16(fft_temp, cmplx_buff, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    delay_AC = find_max_cmplx(cmplx_buff, BUFFER_SIZE_CHANNEL);
    
    /* Correlate and find the delay between channels A and D */
    rfft_fr16(cir_buff[D], fft_temp, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    multiply(fft_ref, fft_temp, fft_temp, BUFFER_SIZE_CHANNEL);
    ifft_fr16(fft_temp, cmplx_buff, tt, 1, BUFFER_SIZE_CHANNEL, &block_exponent, 3);
    delay_AD = find_max_cmplx(cmplx_buff, BUFFER_SIZE_CHANNEL);
}

#else

/*
 * Compute time of arrival for the signal on each channel
 *
 * Locate the leading each of the ping in each channel and use this to create
 * times of arrival for the ping on each channel. The time are then rezeroed so
 * that the time of arrival on channel A is 0.
 */
static void compute_toa(void) {
    /* Compute time of arrival for all channels */
    for(int channel = A; channel <= D; channel++) {
        /* Default to 5000 (a bogus value) */
        toa[channel] = 5000;
        for(int i = 0; i < BUFFER_SIZE_CHANNEL; i++) {
            if(cir_buff[channel][i] > TRIGGER_VALUE) {
                toa[channel] = i;
                break;
            }
        }
    }

    /* Rezero all the TOA values */
    for(int channel = A; channel <= D; channel++) {
        toa[channel] -= toa[A];
    }
}
#endif

/*
 * Output the delays
 *
 * The delays are output so that they can provide input to the acoustic's guided
 * controller running on the host system
 */
static void data_out(void) {
#ifdef USE_LIBSEAWOLF
# ifdef ACOUSTICS_CORRELATE
    Var_set("Acoustics.Delays.AB", delay_AB);
    Var_set("Acoustics.Delays.AC", delay_AC);
    Var_set("Acoustics.Delays.AD", delay_AD);
    Notify_send("UPDATED", "Acoustics.Delays");
# else
    Var_set("Acoustics.TOA.A", toa[A]);
    Var_set("Acoustics.TOA.B", toa[B]);
    Var_set("Acoustics.TOA.C", toa[C]);
    Var_set("Acoustics.TOA.D", toa[D]);
    Notify_send("UPDATED", "Acoustics.TOA");
# endif
#endif
    
#ifdef ACOUSTICS_DEBUG
# ifdef ACOUSTICS_CORRELATE
    /* Output pDelay values */
    printf("delay_AB: %d \n", delay_AB);
    printf("delay_AC: %d \n", delay_AC);
    printf("delay_AD: %d \n", delay_AD);
# else
    printf("A: %d\n", toa[A]);
    printf("B: %d\n", toa[B]);
    printf("C: %d\n", toa[C]);
    printf("D: %d\n", toa[D]);
# endif
#endif
}

#ifdef ACOUSTICS_DUMP
static void dump(int channel) {
    FILE* f = fopen("dump.txt", "w");
    for(int i = 0; i < BUFFER_SIZE_CHANNEL; i++) {
        fprintf(f, "%d\n", (signed short) cir_buff[channel][i]);
    }
    fclose(f);
}
#endif

int main(int argc, char** argv) {
#ifdef USE_LIBSEAWOLF
    Seawolf_loadConfig("seawolf.conf");
    Seawolf_init("Blackfin");
    Var_setAutoNotify(false);
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

    /* Open driver connection */
    driver_f = open("/dev/ppiadc", O_RDWR);
    if(driver_f < 0) {
        perror("Could not open character device to communicate with PPI/ADC driver");
        fprintf(stderr, "Make sure the module is loaded and that the device node has been created at /dev/ppiadc\n");
        exit(1);
    }
    
    /* Initialize all data structures */
    init(argv[1]);

    while(true) {
        TIME_PRE(t, "Collecting data...");
        record_ping();
        TIME_POST(t);

        TIME_PRE(t, "Linearizing buffers...");
        linearize_buffers();
        TIME_POST(t);

        TIME_PRE(t, "Filtering buffers...");
        filter_buffers();
        TIME_POST(t);

#ifdef ACOUSTICS_DUMP
        dump(A);
        break;
#endif

#ifdef ACOUSTICS_CORRELATE
        TIME_PRE(t, "Correlating buffers...");
        correlate_buffers();
        TIME_POST(t);
#else
        TIME_PRE(t, "Computing times of arrival...");
        compute_toa();
        TIME_POST(t);
#endif

        data_out();
    }

    /* Close driver connection */
    close(driver_f);

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
