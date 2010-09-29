/**
 * \file
 * \brief Main user space program
 */

/**
 * \addtogroup usermain
 * \{
 */

/** If defined enable debugging code */
#define ACOUSTICS_DEBUG

/** If defined, enable profiling (prints timing information for blocks) */
#define ACOUSTICS_PROFILE

/** If defined, dump channel data pre and post filtering */
#define ACOUSTICS_DUMP

/** If defined, use libseawolf to store the computed delay values */
#define USE_LIBSEAWOLF

/** \} */

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
#include <stats.h>

#include "acoustics.h"

/**
 * \defgroup usermain Main
 * \ingroup userspace
 * \brief Main userspace routines
 * \{
 */

/** Circular buffers for each channel */
static adcsample* cir_buff[CHANNELS];

/** Current (write) offset in the circular buffers */
static unsigned int cir_buff_offset;

/** FIR Coefficients */
static fract16* coefs;

/** File handler associated with the opened device driver /dev/ppiadc */
static int driver_f = -1;

/** Reset flag to be written to the kernel device driver */
static const uint8_t RESET_FLAG = 1;

/** FIR filter state for each channel */
static fir_state_fr16 fir_state[CHANNELS];

/** State for the FIR filter used to detect the incoming ping (trigger) */
static fir_state_fr16 fir_state_trig;

/** FIR delay lines for each channel */
static fract16* fir_delay[CHANNELS];

/** Delay line for the FIR filter used to detect the incoming ping (trigger) */
static fract16* fir_delay_trig;

/**
 * Computed mean of the signal. Used to centered filtered data about 0.
 *
 * \see AVG_COUNT
 */
static long int signal_mean = 0;

/**
 * Time (in samples) at which the trigger (ping) is detected
 *
 * \see TRIGGER_VALUE
 * \see TRIGGER_POINT_OFFSET
 * \see TRIGGER_CHANNEL
 */
static int trigger_point = -1;

/** Computed delay (in samples) of signal arrival from channel A to C */
static int delay_AC;

/** Computed delay (in samples) of signal arrival from channel B to D */
static int delay_BD;

#ifdef ACOUSTICS_PROFILE
Timer* t;
#endif

/* Misc */
static unsigned int i, j;
static adcsample* temp_buff;

/* Dump fract16 data to a flat file */
#ifdef ACOUSTICS_DUMP
/**
 * \brief Dump data to flat file
 *
 * Dump a buffer to a file with each fract16 dumped as an integer, one per line.
 *
 * \param buff Buffer to dump
 * \param size Size of the buffer
 * \param file Name of file to dump to
 */
static void dump(fract16* buff, int size, const char* file) {
    FILE* f = fopen(file, "w");
    for(int i = 0; i < size; i++) {
        fprintf(f, "%d\n", (signed short) buff[i]);
    }
    fclose(f);
}
#endif

/**
 * \brief Allocate memory and initialize all data structures
 *
 * Allocates memory for buffers and filter delay lines, reads FIR filter
 * coefficients from disk, and initilizes FIR filters
 *
 * \param coefs_file_name File to read FIR filter coefficients from
 */
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

    /* Temporary buffer used in linearization of circular buffers, to store
       output of the FIR filter applied to trigger samples, and to store the
       result from correlation */
    temp_buff = calloc(sizeof(adcsample), BUFFER_SIZE_CHANNEL * 2);
}

/**
 * \brief Convert a signed 14 value to a signed 16 bit value
 *
 * Convert a signed 14 value to a signed 16 bit value
 *
 * \param v The 14 bit signed value
 * \return An 16 bit extended version of the given number
 */
static inline short expand_complement(short v) {
    if(v & (1 << 13)) {
        /* Negative value */
        return -(((1 << 14) - 1) & ((~v) + 1));
    } else {
        /* Already positive */
        return v;
    }
}

/**
 * \brief Interact with the PPI/ADC driver to collect a "ping" sample
 *
 * This function reads in sample blocks for each channel from the driver until
 * the circular buffer has been filled. Once the circular buffer has been filled
 * each new channel sample set is checked for the presence of the target
 * frequence on the trigger channel (see \ref TRIGGER_CHANNEL). Once the signal
 * is located the recording process is "triggered". A few additional padding
 * samples (specified by \ref EXTRA_READS) are completed and the function exits.
 */
static void record_ping(void) {
    int state = READING;
    unsigned int extra_reads = EXTRA_READS;
    bool cir_buff_full = false;
    short* current_buffer = NULL;
    short* current_buffer_copy;

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
        current_buffer_copy = current_buffer + 0;
        for(i = 0, j = cir_buff_offset; i < SAMPLES_PER_CHUNK; i++, j++, current_buffer_copy += CHANNELS) {
            cir_buff[A][j] = expand_complement(*current_buffer_copy);
        }

        current_buffer_copy = current_buffer + 1;
        for(i = 0, j = cir_buff_offset; i < SAMPLES_PER_CHUNK; i++, j++, current_buffer_copy += CHANNELS) {
            cir_buff[B][j] = expand_complement(*current_buffer_copy);
        }

        current_buffer_copy = current_buffer + 2;
        for(i = 0, j = cir_buff_offset; i < SAMPLES_PER_CHUNK; i++, j++, current_buffer_copy += CHANNELS) {
            cir_buff[C][j] = expand_complement(*current_buffer_copy);
        }

        current_buffer_copy = current_buffer + 3;
        for(i = 0, j = cir_buff_offset; i < SAMPLES_PER_CHUNK; i++, j++, current_buffer_copy += CHANNELS) {
            cir_buff[D][j] = expand_complement(*current_buffer_copy);
        }

        /* Don't look for a trigger until the buffer has been filled */
        if(state == READING) {
            /* Run the FIR filter on the current sample from channel A */
            fir_fr16(cir_buff[TRIGGER_CHANNEL] + cir_buff_offset, temp_buff, SAMPLES_PER_CHUNK, &fir_state_trig);

            for(i = 0; i < AVG_COUNT; i++) {
                signal_mean += temp_buff[i];
            }
            signal_mean /= AVG_COUNT;

            /* If the circular buffer is full, check the current sample for the trigger */
            if(cir_buff_full) {
                for(i = 0; i < SAMPLES_PER_CHUNK; i++) {
                    if(temp_buff[i] - signal_mean > TRIGGER_VALUE) {
                        /* Store the index of the trigger point as it will be once the buffers are linearized */
                        trigger_point = (SAMPLES_PER_CHUNK * (BUFFER_CHUNK_COUNT - 1 - EXTRA_READS)) + i + TRIGGER_POINT_OFFSET;
                        state = TRIGGERED;
                        break;
                    }
                }
            }
        }                
        
        /* Increment the offset into the circular buffer -- if we are going to
           be back to 0 within EXTRA_READS then set the buffer as filled to
           indicate that we have a full buffers worth of data */
        cir_buff_offset = (cir_buff_offset + SAMPLES_PER_CHUNK) % BUFFER_SIZE_CHANNEL;
        if((cir_buff_offset + SAMPLES_PER_CHUNK + (EXTRA_READS * SAMPLES_PER_CHUNK)) % BUFFER_SIZE_CHANNEL == 0) {
            cir_buff_full = true;
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

/**
 * \brief Linearize the circular buffers
 *
 * Linearize each circular buffer using a temporary buffer. Output is stored
 * back into the circular buffer space
 *
 * The linearization is done in three stages,
 *
 *  -# Data from the current write position to the end of the channel buffer
 *     (the oldest data) is written to the beginning of a temporary buffer
 *  -# Data from the beginning of the channel buffer to the current write
 *     position (the newest data) in the channel buffer is placed at the end
 *     of the temporary buffer
 *  -# The temporary buffer's contents are copied back to the channel buffer
 */
static void linearize_buffers(void) {
    for(int channel = A; channel <= D; channel++) {
        memcpy(temp_buff, cir_buff[channel] + cir_buff_offset, sizeof(adcsample) * (BUFFER_SIZE_CHANNEL - cir_buff_offset));
        memcpy(temp_buff + (BUFFER_SIZE_CHANNEL - cir_buff_offset), cir_buff[channel], sizeof(adcsample) * cir_buff_offset);
        memcpy(cir_buff[channel], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
    }
}

/** 
 * \brief Filter each linearized buffer
 *
 * Each channel buffer is run through the FIR filter and the result is stored
 * back into the channel buffer. Before returning, the output from the FIR
 * filters is adjusted so that it is centered approximately at 0.
 */
static void filter_buffers(void) {
    for(int channel = A; channel <= D; channel++) {
        fir_fr16(cir_buff[channel], temp_buff, BUFFER_SIZE_CHANNEL, &fir_state[channel]);
        memcpy(cir_buff[channel], temp_buff, sizeof(adcsample) * BUFFER_SIZE_CHANNEL);
        
        /* Center and scale the signal */
        for(int i = 0; i < BUFFER_SIZE_CHANNEL; i++) {
            cir_buff[channel][i] -= signal_mean;
            cir_buff[channel][i] *= 10;
        }

        /* Remove invalid data points from when the FIR filter is ramping up */
        for(int i = FIR_COEF_COUNT; i >= 0; i--) {
            cir_buff[channel][i] = cir_buff[channel][FIR_COEF_COUNT];
        }
    }
}

/**
 * \brief Perform an optimized cross-correlation-like operation
 * 
 * Perform a cross correlation and return the lag value resulting in the largest
 * resulting correlation. Note that this algorithm is meant to be applied to
 * subsets of existing buffers. Buffer 'a' must be accessible from a[0] to
 * a[size]. Buffer 'b' must be accessible from b[min_lag] to b[size + max_lag];
 *
 * \param a The first buffer
 * \param b The second buffer
 * \param size The size of region to include from each buffer
 * \param min_lag The smallest lag value to check
 * \param max_lag The largest lag value to check
 * \return The lag corresponding to the largest numerical correlation
 */
static int crosscor_max(fract16* a, fract16* b, int size, int min_lag, int max_lag) {
    fract16* c = malloc(sizeof(fract16) * (max_lag - min_lag));
    int max_x;
    int max_y;
    complex_fract16 s, t;

    s.im = 0;
    t.im = 0;

    for(int lag = min_lag; lag < max_lag; lag++) {
        c[lag - min_lag] = 0;
        for(int n = 0; n < size; n++) {
            s.re = a[n];
            t.re = b[n + lag];
            c[lag - min_lag] += cmlt_fr16(s, t).re;
        }
    }

    max_x = 0;
    max_y = c[0];
    for(int i = 0; i < max_lag - min_lag; i++) {
        if(c[i] > max_y) {
            max_x = i;
            max_y = c[i];
        }
    }

    free(c);
    return max_x + min_lag;
}

/**
 * \brief Perform correlations and compute delays in the signals between the channels
 *
 * This correlation block is optimized by only working on a subset of the
 * buffers which all center around the trigger_point which is set when the ping
 * is captured. It also differs from a standard correlation in that is checks
 * negative and positive lag values in a single pass. Most of the work here is
 * done by \ref crosscor_max.
 *
 * See http://en.wikipedia.org/wiki/Cross_correlation
 */
static void correlate_buffers(void) {
    delay_AC = crosscor_max(cir_buff[A] + trigger_point - CORR_RANGE,
                            cir_buff[C] + trigger_point - CORR_RANGE,
                            CORR_RANGE * 2, -CORR_LAG_MAX, CORR_LAG_MAX);

    delay_BD = crosscor_max(cir_buff[B] + trigger_point - CORR_RANGE,
                            cir_buff[D] + trigger_point - CORR_RANGE,
                            CORR_RANGE * 2, -CORR_LAG_MAX, CORR_LAG_MAX);
}

/**
 * \brief Output the delays
 *
 * The delays are output so that they can provide input to the acoustic's guided
 * controller running on the host system. If \ref USE_LIBSEAWOLF is defined,
 * then these values will be saved to their corresponding libseawolf variables.
 */
static void data_out(void) {
#ifdef USE_LIBSEAWOLF
    Var_set("Acoustics.Delays.AC", delay_AC);
    Var_set("Acoustics.Delays.BD", delay_BD);
    Notify_send("UPDATED", "Acoustics.Delays");
#endif
    
#ifdef ACOUSTICS_DEBUG
    /* Output delay values */
    printf("delay_AC: %d \n", delay_AC);
    printf("delay_BD: %d \n", delay_BD);
#endif
}

/**
 * \brief Manage and process acoustics data
 *
 * This top-level function orchestrates the operation of the acoustics signal
 * processing. Upon starting, data structures are initiliazed and a connection
 * is opened to the kernel driver through the /dev/ppiadc device. Once this is
 * established the standard processing loop is entered consisting of the
 * following steps,
 *
 * -# \ref record_ping is called to capture a full ping. Once a full ping has
 *    been captured and is stored in the circular buffers, record_ping will
 *    return.
 * -# \ref linearize_buffers is called to unroll (linearize) the circular
 *    buffers so they can be manipulated
 * -# \ref filter_buffers is called to apply the FIR filter inplace onto each
 *    channel. The output from the FIR filters is normalized before returning.
 * -# \ref correlate_buffers is called to perform a correlation on the filtered
 *    buffers to generate delay values.
 * -# \ref data_out is called to output the delay values
 * -# Process begings again at step 1
 *
 * \param argc Argument count
 * \param argv Arguments
 * \return 0 on success
 */
int main(int argc, char** argv) {
    short* tmp;

#ifdef USE_LIBSEAWOLF
    Seawolf_loadConfig("seawolf.conf");
    Seawolf_init("Blackfin");
    Var_setAutoNotify(false);
#endif


#ifdef ACOUSTICS_PROFILE
    /* Timer for profiling */
    t = Timer_new();
#endif

    /* Missing coefficients file argument */
    if(argc <= 1) {
        printf("Missing required argument. Please provide a FIR filter coefficients file\n");
        exit(1);
    }

    /* Open driver connection */
    TIME_PRE(t, "Opening device...");
    driver_f = open("/dev/ppiadc", O_RDWR);
    if(driver_f < 0) {
        perror("Could not open character device to communicate with PPI/ADC driver");
        fprintf(stderr, "Make sure the module is loaded and that the device node has been created at /dev/ppiadc\n");
        exit(1);
    }
    TIME_POST(t);

    /* Do a fake ready to throw out the first data block as the ADC turns on */
    write(driver_f, &RESET_FLAG, 1);
    read(driver_f, &tmp, sizeof(tmp));

    /* Initialize all data structures */
    init(argv[1]);

    while(true) {
        TIME_PRE(t, "Collecting data...");
        record_ping();
        TIME_POST(t);

        TIME_PRE(t, "Linearizing buffers...");
        linearize_buffers();
        TIME_POST(t);

#ifdef ACOUSTICS_DUMP
        TIME_PRE(t, "Dumping raw buffers...");
        dump(cir_buff[A], BUFFER_SIZE_CHANNEL, "dump_a_raw.txt");
        dump(cir_buff[B], BUFFER_SIZE_CHANNEL, "dump_b_raw.txt");
        dump(cir_buff[C], BUFFER_SIZE_CHANNEL, "dump_c_raw.txt");
        dump(cir_buff[D], BUFFER_SIZE_CHANNEL, "dump_d_raw.txt");
        TIME_POST(t);
#endif

        TIME_PRE(t, "Filtering buffers...");
        filter_buffers();
        TIME_POST(t);

#ifdef ACOUSTICS_DUMP
        TIME_PRE(t, "Dumping filtered buffers...");
        dump(cir_buff[A], BUFFER_SIZE_CHANNEL, "dump_a_filtered.txt");
        dump(cir_buff[B], BUFFER_SIZE_CHANNEL, "dump_b_filtered.txt");
        dump(cir_buff[C], BUFFER_SIZE_CHANNEL, "dump_c_filtered.txt");
        dump(cir_buff[D], BUFFER_SIZE_CHANNEL, "dump_d_filtered.txt");
        TIME_POST(t);

        /* Exit after dumping buffers */
        break;
#endif

        TIME_PRE(t, "Correlating buffers...");
        correlate_buffers();
        TIME_POST(t);

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

/** \} */
