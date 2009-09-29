//filefun

#include <stdio.h>

#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	// for CSV storage
	fract16 data_stdin[ARRAY_SIZE];
	fract16 data_file[ARRAY_SIZE];
	fract16 data_correlation[ARRAY_SIZE];
	int count_stdin, count_file, count_min;

	// open the file
	FILE *file=fopen(argv[1],"r");
	
	count_file = readCSV(data_file, file);
	count_stdin = readCSV(data_stdin, stdin);
	count_min = (count_file < count_stdin) ? count_file : count_stdin;

	// Perform the multiply
	correlate(data_stdin, data_file, data_correlation, count_min);

	printCSV(data_correlation, count_min);
	
	return(EXIT_SUCCESS);
}
