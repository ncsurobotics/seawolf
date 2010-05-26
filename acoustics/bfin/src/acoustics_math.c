
#include <math.h>
#include <stdlib.h>
#include <string.h>

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

void fft(fract16* data, complex_fract16* cmplx, int ending) {
    /* Control variables */
    /* int twiddleSize = ending;
       int wst = ending;
       int scale=0;
       int *blockExp = 0; */

    /* FFT stuff */
    complex_fract16 w[ending];

    /* Set up twiddle tables */
    twidfftrad2_fr16(w,ending);

    /* Execute FFT */
    rfft_fr16(data, cmplx, w, 1, ending, 0 , 0);
}

void ifft(complex_fract16* cmplx, fract16* data, int ending) {
    /* Control variables */
    int twiddleSize = ending / 2;
    int wst = 2 * twiddleSize / ending;
    int scale;

    /* FFT stuff */
    complex_fract16 w[ending];
    complex_fract16 o[ending];
    complex_fract16* o_ptr = (complex_fract16*) o;

    /* Set up twiddle tables */
    twidfftrad2_fr16(w,ending/2);

    /* Execute IFFT */
    ifft_fr16(cmplx, (complex_fract16*) o, (complex_fract16*) w, wst, ending, &scale, 2);

    /* Convert complex to real */
    for(int i = 0; i < ending; i++) {
        /* This works, data is a local copy of the data pointer being passed to it */
        *(data++) = (o_ptr++)->re;
    }
}

/* FIR filter (send it down the zipline) */
void firfly(fract16* data, int size, fir_state_fr16* firState) {
    fract16* tempData;

    /* Create Temporary Data array */
    tempData = calloc(sizeof(fract16), size);

    /* Execute fir */
    fir_fr16(data, tempData, size, firState);

    /* overwrite input data */
    memcpy(data, tempData, sizeof(fract16)*size );
}

void convolve(fract16* f, fract16*g, fract16* out, int size) {
    convolve_fr16(f, size, g, size, out);
}

void fast_convolve(fract16* f, fract16* g, fract16* out, int size) {
    /* Implements fast convolution */
    complex_fract16 f_fft[size];
    complex_fract16 g_fft[size];
    complex_fract16 out_fft[size];

    fft(f, f_fft, size);
    fft(g, g_fft, size);
    multiply(f_fft, g_fft, out_fft, size);
    ifft(out_fft, out, size);
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
