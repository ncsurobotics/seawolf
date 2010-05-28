
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

void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size) {
    while(size--) {
        *out++ = cmlt_fr16(*in1++, *in2++);
    }
}

void fft(fract16* input, complex_fract16* output, int size) {
    /* Create space for twiddle table */
    complex_fract16* tt;
    int block_exponent;

    printf(" Allocating buffers\n");
    tt = malloc(sizeof(complex_fract16) * (size / 2));

    /* Populate twiddle table */
    printf(" Setting up twiddle table\n");
    twidfftrad2_fr16(tt, size);

    /* Execute FFT */
    printf(" Doing FFT\n");
    rfft_fr16(input, output, tt, 1, size, &block_exponent, 1);

    /* Free twiddle table */
    printf(" Freeing\n");
    free(tt);
}

void ifft(complex_fract16* cmplx, fract16* data, int size) {
    /* Control variables */
    int tt_size = (size / 2) + 1;
    int block_exponent;

    /* FFT stuff */
    complex_fract16* tt;
    complex_fract16* temp_out;

    printf(" Allocating buffers\n");
    tt = malloc(sizeof(complex_fract16) * tt_size);
    temp_out = malloc(sizeof(complex_fract16) * size);

    /* Set up twiddle table */
    printf(" Setting up twiddle table\n");
    twidfftrad2_fr16(tt, size);

    /* Execute IFFT */
    printf(" Doing IFFT\n");
    ifft_fr16(cmplx, temp_out, tt, 1, size, &block_exponent, 1);

    /* Convert complex to real */
    printf(" Converting complex to real\n");
    for(int i = 0; i < size; i++) {
        /* This works, data is a local copy of the data pointer being passed to it */
        *(data++) = temp_out[i].re;
    }

    free(tt);
    free(temp_out);
}

/* FIR filter (send it down the zipline) */
void firfly(fract16* data, int size, fir_state_fr16* firState) {
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

void convolve(fract16* f, fract16*g, fract16* out, int size) {
    convolve_fr16(f, size, g, size, out);
}

void fast_convolve(fract16* f, fract16* g, fract16* out, int size) {
    /* Implements fast convolution */
    complex_fract16* f_fft;
    complex_fract16* g_fft;
    complex_fract16* out_fft;

    f_fft = malloc(sizeof(complex_fract16) * size);
    g_fft = malloc(sizeof(complex_fract16) * size);
    out_fft = malloc(sizeof(complex_fract16) * size);

    printf("FFT 1\n");
    fft(f, f_fft, size);

    printf("FFT 2\n");
    fft(g, g_fft, size);

    printf("Multiply\n");
    multiply(f_fft, g_fft, out_fft, size);

    printf("IFFT\n");
    ifft(out_fft, out, size);

    free(f_fft);
    free(g_fft);
    free(out_fft);
}

void correlate(fract16* f, fract16* g, fract16* out, int size) {
    /* Cross Correlation = Convolution(f(-t), g(t)) */
    flip(f, size);
    convolve(f, g, out, size);
}

void fast_correlate(fract16* f, fract16* g, fract16* out, int size) {
    /* Cross Correlation = Convolution(f(-t), g(t)) */
    flip(f, size);
    fast_convolve(f, g, out, size);
}

int findMax(fract16* f, int size) {
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
