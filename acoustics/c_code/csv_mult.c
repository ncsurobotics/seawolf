//filefun

#include <complex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	/*for CSV storage*/
	complex data_stdin[ARRAY_SIZE];
	complex data_file[ARRAY_SIZE];
	complex data_product[ARRAY_SIZE];
	int count_stdin, count_file, count_min;

	/*open the file*/
	FILE *file=fopen(argv[1],"r");
	
	count_file = readCSVcmplx(data_file, file);
	count_stdin = readCSVcmplx(data_stdin, stdin);
	count_min = (count_file < count_stdin) ? count_file : count_stdin;

	// Perform the multiply
	multiply(data_stdin, data_file, data_product, count_min);

	printCSVcmplx(data_product, count_min);
	
	return(EXIT_SUCCESS);
}
