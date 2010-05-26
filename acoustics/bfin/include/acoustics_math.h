#ifndef ACOUSTICS_MATH_H
#define ACOUSTICS_MATH_H

#include <math.h>
#include <math_bf.h>
#include <complex_bf.h>
#include <filter.h>

void flip(fract16*, int);
void fft(fract16*, complex_fract16*, int);
void ifft(complex_fract16*, fract16*, int);
void firfly(fract16*, int, fir_state_fr16*);
void multiply(complex_fract16*, complex_fract16*, complex_fract16*, int);
void convolve(fract16*, fract16*, fract16*, int);
void fast_convolve(fract16*, fract16*, fract16*, int);
void correlate(fract16*, fract16*, fract16*, int);
void fast_correlate(fract16*, fract16*, fract16*, int);
int findMax(fract16* f, int size);

#define ARRAY_SIZE 8192

#endif // #ifndef CSV_IN_H
