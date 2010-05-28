#ifndef ACOUSTICS_MATH_H
#define ACOUSTICS_MATH_H

#include <math.h>
#include <math_bf.h>
#include <complex_bf.h>
#include <filter.h>

void flip(fract16*, int);
void fft(fract16*, complex_fract16*, int);
void ifft(complex_fract16*, fract16*, int);
void fir_inplace(fract16*, int, fir_state_fr16*);
void fir(fract16*, fract16*, int, fir_state_fr16*);
void convolve(fract16*, fract16*, fract16*, int);
void correlate(fract16*, fract16*, fract16*, int);
void fast_correlate(fract16*, fract16*, fract16*, int);
int find_max(fract16* f, int size);
int find_max_cmplx(complex_fract16* f, int size);
void conjugate(complex_fract16* input, int size);
void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size);
void real_part(complex_fract16* input, fract16* output, int size);

#endif // #ifndef CSV_IN_H
