//Commandfun

#include <stdio.h>

#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	/*for CSV storage*/
	fract16 data[ARRAY_SIZE];
	int count;
	
	/*open the file*/
	FILE *in=stdin;
	
	count = readCSV(data, in);
	
	//flip the array
	flip(data, count);
	
	printCSV(data, count);
	
	return(EXIT_SUCCESS);
}
