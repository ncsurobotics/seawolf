#ifndef __SEAWOLF3_ACOUSTICS_INCLUDE_H
#define __SEAWOLF3_ACOUSTICS_INCLUDE_H

#include <math_bf.h>
#include <complex_bf.h>

/* A sample from the FPGA/ADC is 16 bits */
typedef fract16 adcsample;

/* Channels */
#define A 0
#define B 1
#define C 2
#define D 3

/* Input data configuration */
#define CHANNELS 4

/* Samples per second generated by the ADC for each channel */
#define SAMPLES_PER_SECOND (96 * 1024)

/* The ADC driver produces data in 8k sample chunks per channel */
#define SAMPLES_PER_CHANNEL (8 * 1024) 

/* Size of a circular buffer for a single channel. This must be a power of 2
   multiple of SAMPLES_PER_CHANNEL */
#define BUFFER_SIZE_CHANNEL (32 * 1024)

/* FIR filter coefficient count */
#define FIR_COEF_COUNT 614

/* Minimum value to trigger on */
#define TRIGGER_VALUE ((short)(500))

/* Circular buffer state */
#define READING   0x00
#define TRIGGERED 0x01
#define DONE      0x02

/* Extra number of read cyles to perform after trigger. This can be used to
   "pad" the other channels and ensure that the trigger is present in all
   channels */
#define EXTRA_READS 1

/* Profiling helpers */
#ifdef ACOUSTICS_PROFILE
# define TIME_PRE(t, text) do {                    \
        printf("%-30s", (text));                   \
        fflush(stdout);                            \
        Timer_reset(t);                            \
    } while(false)
# define TIME_POST(t) do {                      \
        printf("%5.3f\n", Timer_getDelta(t));   \
    } while(false)
#else
# define TIME_PRE(t, text) do { } while(false)
# define TIME_POST(t) do { } while(false)
#endif

/* Support routines */
void load_coefs(fract16* coefs, char* coef_file_name, int num_coefs);
int find_max_cmplx(complex_fract16* w, int size);
void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size);
void conjugate(complex_fract16* w, int size);

#endif // #ifndef __SEAWOLF3_ACOUSTICS_INCLUDE_H
