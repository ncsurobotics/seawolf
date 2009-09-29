//Commandfun

#include <stdio.h>

#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	// for CSV storage
	fract16 data[ARRAY_SIZE];
	complex_fract16 imag[ARRAY_SIZE];
	int count;
	
	// open the file
	FILE *in=stdin;
	
	count = readCSV(data, in);
	
	// fft the array
	fft(data, imag, count);
	
	printCSVcmplx(imag, count);
	
	return(EXIT_SUCCESS);
}


