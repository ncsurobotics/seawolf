//Commandfun

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "csv_io.h"
#include "acoustics_math.h"

int main(int argc, char *argv[])
{
	/*for CSV storage*/
	float data[ARRAY_SIZE];
	int count;
	
	/*open the file*/
	FILE *in=stdin;
	
	count = readCSV(data, in);
	
	//flip the array
	flip(data, count);
	
	printCSV(data, count);
	
	return(EXIT_SUCCESS);
}
