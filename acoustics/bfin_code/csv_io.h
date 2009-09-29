#ifndef CSV_IN_H
#define CSV_IN_H

#include <math.h>
#include <math_bf.h>
#include <complex_bf.h>
#include <stdlib.h>

int readCSV(fract16*, FILE*);
int readCSVcmplx(complex_fract16*, FILE*);
void printCSV(fract16*, int);
void printCSVcmplx(complex_fract16*, int);
void pullCoefs( fract16* , char* , int);

#define ARRAY_SIZE 8192

#endif // #ifndef CSV_IN_H
