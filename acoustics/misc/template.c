//filefun

#include <stdio.h>

#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	/*for CSV storage*/
	fract16 data[ARRAY_SIZE];
	int count;

	/*open the file*/
	FILE *in=fopen(argv[1],"r"); /* stdin for pipeable command */
	
	count = readCSV(data, in);

	//Do stuff here

	printCSV(data, count);
	
	return(EXIT_SUCCESS);
}