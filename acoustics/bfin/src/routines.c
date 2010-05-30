
#include "acoustics.h"

#include <stdio.h>
#include <stdlib.h>

#include <math_bf.h>
#include <complex_bf.h>

/* Pull in coefficient values from a file */
void load_coefs(fract16* coefs, char* coef_file_name, int num_coefs) {
    FILE* f;
    char buff[256];

    /* Open file */
    f = fopen(coef_file_name, "r");

    if(f == NULL) {
        printf("Could not open coefficients file: %s\n", coef_file_name);
        exit(1);
    }

    /* Read coefficients */
    for(int i = 0; i < num_coefs; i++) {
        fgets(buff, 255, f);
        coefs[i] = atoi(buff);
    }

    /* Close File */
    fclose(f);
}

/* Return the index of the real part maximum of the array */
int find_max_cmplx(complex_fract16* w, int size) {
    fract16 max_y = 0;
    int max_x = 0;

    for(int i = 0; i < size; i++) {
        if(w[i].re > max_y) {
            max_y = w[i].re;
            max_x = i;
        }
    }

    return max_x;
}

/* Perform a pointwise product of the complex valued arrrays in1 and in2 storing
   the result in out */
void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size) {
    while(size--) {
        *out++ = cmlt_fr16(*in1++, *in2++);
    }
}

/* Conjugate every element in the given complex valued array */
void conjugate(complex_fract16* w, int size) {
    while(size--) {
        *w = conj_fr16(*w);
        w++;
    }
}
