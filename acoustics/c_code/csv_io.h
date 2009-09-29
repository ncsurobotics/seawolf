#ifndef CSV_IN_H
#define CSV_IN_H

#include <complex.h>

int readCSV(float*, FILE*);
int readCSVcmplx(complex*, FILE*);
void printCSV(float*, int);
void printCSVcmplx(complex*, int);

//#define ARRAY_SIZE 8192

#endif // #ifndef CSV_IN_H
