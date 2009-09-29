#ifndef ACOUSTICS_MATH_H
#define ACOUSTICS_MATH_H

#include <complex.h>

void flip(float*, int);
void fft(float*, complex*, int);
void ifft(complex*, float*, int);
void multiply(complex*, complex*, complex*, int);
void convolve(float*, float*, float*, int);
void correlate(float*, float*, float*, int);

#define ARRAY_SIZE 2097152

#endif // #ifndef CSV_IN_H
