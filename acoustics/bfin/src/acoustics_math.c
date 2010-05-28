
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <complex_bf.h>
#include <filter.h>
#include <math_bf.h>

#include "acoustics_math.h"

void flip(fract16* data, int size) {
    fract16* data_end = data + size - 1;
    fract16 tmp;

    while(data_end > data) {
        /* Swap */
        tmp = *data;
        *data++ = *data_end;
        *data_end-- = tmp;
    }
}

void fft(fract16* input, complex_fract16* output, int size) {
    /* Create space for twiddle table */
    complex_fract16* tt;
    int block_exponent;

    tt = malloc(sizeof(complex_fract16) * (size / 2));

    /* Populate twiddle table */
    twidfftrad2_fr16(tt, size);

    /* Execute FFT */
    rfft_fr16(input, output, tt, 1, size, &block_exponent, 1);

    /* Free twiddle table */
    free(tt);
}

void ifft(complex_fract16* cmplx, fract16* data, int size) {
    /* Control variables */
    int tt_size = (size / 2) + 1;
    int block_exponent;

    /* FFT stuff */
    complex_fract16* tt;
    complex_fract16* temp_out;

    tt = malloc(sizeof(complex_fract16) * tt_size);
    temp_out = malloc(sizeof(complex_fract16) * size);

    /* Set up twiddle table */
    twidfftrad2_fr16(tt, size);

    /* Execute IFFT */
    ifft_fr16(cmplx, temp_out, tt, 1, size, &block_exponent, 1);

    /* Convert complex to real */
    for(int i = 0; i < size; i++) {
        /* This works, data is a local copy of the data pointer being passed to it */
        *(data++) = temp_out[i].re;
    }

    free(tt);
    free(temp_out);
}

/* FIR filter (send it down the zipline) */
void fir_inplace(fract16* data, int size, fir_state_fr16* firState) {
    fract16* tempData;

    /* Create Temporary Data array */
    tempData = calloc(sizeof(fract16), size);

    /* Execute fir */
    fir_fr16(data, tempData, size, firState);

    /* overwrite input data */
    memcpy(data, tempData, sizeof(fract16) * size);

    /* Free temporary buffer */
    free(tempData);
}

void fir(fract16* input, fract16* output, int size, fir_state_fr16* fir_state) {
    fir_fr16(input, output, size, fir_state);
}

void convolve(fract16* f, fract16*g, fract16* out, int size) {
    convolve_fr16(f, size, g, size, out);
}

void correlate(fract16* f, fract16* g, fract16* out, int size) {
    /* Cross Correlation = Convolution(f(-t), g(t)) */
    flip(f, size);
    convolve(f, g, out, size);
}

void conjugate(complex_fract16* input, int size) {
    for(int i = 0; i < size; i++) {
        input[i] = conj_fr16(input[i]);
    }
}

void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size) {
    while(size--) {
        *out++ = cmlt_fr16(*in1++, *in2++);
    }
}

void real_part(complex_fract16* input, fract16* output, int size) {
    for(int i = 0; i < size; i++) {
        *(output++) = (input++)->re;
    }
}

void fast_correlate(fract16* f, fract16* g, fract16* out, int size) {
    /* Cross correlation = ifft(fft(f)* . fft(g))
       Where the asterisk denotes the complex conjegate
       
       See http://en.wikipedia.org/wiki/Cross_correlation */

    complex_fract16* f_fft;
    complex_fract16* g_fft;

    f_fft = malloc(sizeof(complex_fract16) * size);
    g_fft = malloc(sizeof(complex_fract16) * size);

    /* Compute both fourier transforms */
    fft(f, f_fft, size);
    fft(g, g_fft, size);

    /* Conjugate the fourier transform of f */
    conjugate(f_fft, size);

    /* Multiply the transforms and store result back to f_fft */
    multiply(f_fft, g_fft, f_fft, size);

    /* Compute the inverse fourier transform. This output is the correlation of
       f and g */
    ifft(f_fft, out, size);

    free(f_fft);
    free(g_fft);
}

int find_max(fract16* f, int size) {
    fract16 max_y = 0;
    int max_x = 0;

    for(int i = 0; i < size; i++) {
        if(f[i] > max_y) {
            max_y = f[i];
            max_x = i;
        } 
    }

    return max_x;
}

int find_max_cmplx(complex_fract16* f, int size) {
    fract16 max_y = 0;
    int max_x = 0;

    for(int i = 0; i < size; i++) {
        if(f[i].re > max_y) {
            max_y = f[i].re;
            max_x = i;
        } 
    }

    return max_x;
}
