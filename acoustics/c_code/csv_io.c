#include <complex.h>
#include <stdio.h>
#include <stdlib.h>

int readCSV(float* location, FILE *in)
{
	int count = 0;

	if(in == NULL)
	{
		printf("Error opening file\n");
		exit(EXIT_FAILURE);
	};
	
	while(fscanf(in, "%*d %*s %f", &location[count++]) != EOF);
	
	return count - 1;
}

int readCSVcmplx(complex* location, FILE *in)
{
	/*temp location for reading in data*/
	float r, i;
	int count = 0;
	
	if(in==NULL)
	{
		printf("Error opening file\n");
		exit(EXIT_FAILURE);
	};
	
	while(fscanf(in, "%*d %*s %f %*s %f", &r, &i) != EOF)
	{
		location[count++] = r + (I*i);
	};
	
	return count;
}

void printCSV(float* location, int size)
{
	for(int i = 0; i < size; i++)
	{
		printf("%d , %f\n", i + 1, location[i]);
	};
}

void printCSVcmplx(complex* location, int size)
{
	for(int i = 0; i < size; i++)
	{
		printf("%d , %f , %f\n", i + 1, creal(location[i]), cimag(location[i]));
	};
}

