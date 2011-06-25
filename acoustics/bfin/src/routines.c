/**
 * \file
 * \brief Routines for user space acoustics code
 */

#include "acoustics.h"

#include <stdio.h>
#include <stdlib.h>

#include <math_bf.h>
#include <complex_bf.h>

/**
 * \ingroup userspace
 * \defgroup routines Routines
 * \brief Generic routines
 * \{
 */

/**
 * \brief Load FIR filter coefficients from a file
 *
 * Loads a list of FIR filter coefficents into the given array. Each line of the
 * file should give a single signed, fract16 (i.e. short) coefficient.
 *
 * \param coefs Array to store the coefficients to
 * \param coef_file_name File to read from
 * \param num_coefs Number of coefficients to read
 *
 * \todo Replace this with something more flexible. The number of coefficients
 *   shouldn't be hard coded even as a define and should probably just be a
 *   paramater read from the file (i.e. the first line of the coefficients file
 *   specifies the degree. If not enough, or too many coefficents are then read,
 *   throw and error and bomb out
 */
fract16* load_coefs(char* coef_file_name, int* num_coefs) {
    fract16* coefs = NULL;
    FILE* f;
    char buff[256];

    /* Open file */
    f = fopen(coef_file_name, "r");

    if(f == NULL) {
        printf("Could not open coefficients file: %s\n", coef_file_name);
        exit(1);
    }

    /* Read coefficients */
    (*num_coefs) = 0;
    while(fgets(buff, sizeof(buff) - 1, f) != NULL) {
        coefs = realloc(coefs, sizeof(fract16) * ((*num_coefs) + 1));
        coefs[*num_coefs] = atoi(buff);
        (*num_coefs) += 1;
    }

    /* Close File */
    fclose(f);

    return coefs;
}

/**
 * \brief Find a real part maximal complex number
 *
 * Scan the list of complex numbers and return the index of the one with the largest real part 
 *
 * \param w Pointer to the list of complex numbers
 * \param size Number of elements in w
 * \return Index of the maximum value in w
 *
 * \todo This should be renamed to reflect that it considers the real component
 */
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

/**
 * \brief Perform a pair-wise, complex multiplication
 *
 * Pairwise multiply the two arrays, storing the result in a third
 *
 * \param in1 The first array of complex values
 * \param in2 The second array of complex values
 * \param out Array in which to store the products
 * \param size Length of the array (in1, in2, and out must be at least this size)
 */
void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size) {
    while(size--) {
        *out++ = cmlt_fr16(*in1++, *in2++);
    }
}

/**
 * \brief Conjugate each element of the array
 *
 * Conjugate each element of the complex array in place
 *
 * \param w The array of complex values to conjugate
 * \param size Number of elements in w
 */
void conjugate(complex_fract16* w, int size) {
    while(size--) {
        *w = conj_fr16(*w);
        w++;
    }
}

/** \} */
