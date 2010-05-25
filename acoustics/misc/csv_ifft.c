//Commandfun

#include <stdio.h>

#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	// for CSV storage
	fract16 data[ARRAY_SIZE];
	complex_fract16 cmplx[ARRAY_SIZE];
	int count;
	
	// open the file
	FILE *in=stdin;
	
	count = readCSVcmplx(cmplx, in);
	
	// ifft the array
	ifft(cmplx, data, count);

	printCSV(data, count);
	
	return(EXIT_SUCCESS);
}
