//Commandfun

#include <complex.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fftw3.h>
#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	/*for CSV storage*/
	float data[ARRAY_SIZE];
	complex cmplx[ARRAY_SIZE];
	int count;
	
	/*open the file*/
	FILE *in=stdin;
	
	count = readCSVcmplx(cmplx, in);
	
	//ifft the array
	ifft(cmplx, data, count);
	

	printCSV(data, count);

	
	return(EXIT_SUCCESS);
}
