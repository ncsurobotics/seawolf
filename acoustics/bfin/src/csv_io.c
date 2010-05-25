
#include <math.h>
#include <math_bf.h>
#include <complex_bf.h>
#include <fract.h>
#include <ctype.h>
#include <filter.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//define _flip(s) (((unsigned short)(s)) ^ (1 << 15))
#define short_to_fr16(s) ((fract16)(s))
#define fr16_to_short(s) ((signed short)(s))

int my_atoi(const char* s) {
	int n = 0;

	while(isspace(*s)) {
		s++;
	}

	while(isdigit(*s) && *s != '\0') {
		n = (n * 10) + ((*s) - '0');
		s++;
	}

	return n;
}



//String Tokenizer version of readCSV
int readCSV(fract16* location, FILE *in)
{
	char temp_string[256];
	int count = 0;
	
	if(in == NULL)
	{
		printf("Error opening file\n");
		exit(EXIT_FAILURE);
	}
	
	while(fgets(temp_string, 256, in) != NULL)
	{
		strtok(temp_string, ",");
		location[count++] = my_atoi(strtok(NULL, ","));
	}
	
	return count;	
}

int readCSVcmplx(complex_fract16* location, FILE *in)
{
	/*temp location for reading in data*/
	char temp_string[256];
	int count = 0;
	
	if(in == NULL)
	{
		printf("Error opening file\n");
		exit(EXIT_FAILURE);
	};
	
	while(fgets(temp_string, 256, in) != NULL)
	{
		strtok(temp_string, ",");
		location[count].re = short_to_fr16(my_atoi(strtok(NULL, ",")));
		location[count].im = short_to_fr16(my_atoi(strtok(NULL, ",")));
		count++;
	};
	
	return count;
}


void printCSV(fract16* location, int size)
{
	for(int i = 0; i < size; i++)
	{
		printf("%d , %hd\n", i + 1, fr16_to_short(location[i]));
	};
}

void printCSVcmplx(complex_fract16* location, int size)
{
	for(int i = 0; i < size; i++)
	{
		printf("%d , %hd , %hd\n", i + 1, fr16_to_short(location[i].re), fr16_to_short(location[i].im));
	};
}

//Pull in coefficient values from a file
void pullCoefs( fract16* coefs, char* coefFilename, int numCoef )
{
	//Control integer
	int i = 0;
	char* str="AAAAAAAAAAAAAA";	

	//Open file
	FILE* coefFile = fopen(coefFilename, "r");	

	//Read coefficients
	for( i = 0; i < numCoef; i++ )
	{
	    fgets( str, 255, coefFile );
	    coefs[i] = my_atoi(str);
	}

	//Close File
	fclose(coefFile);
}
