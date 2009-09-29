/*main.c - The entry point of the sdsp vision program
 *
 * Author: Robert Brooks Stephenson
 * Date: 7.1.2009
 *
 */


//Import standard libraries
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <strings.h>

//Use custom header file
#include "bitmap.h"


//sdsp main function

int main(int argc, char* argv[])
{
	
	
	
    //---Local Variables---//
		
	//General Purpose Variiables
	int i,j,k;
	
	//Input Filename
	char* input_filename = (char*)malloc(sizeof(char)*255);
	
	//Output Filename
	char* output_filename = (char*)malloc(sizeof(char)*255);
	
	//Character Buffer
	char buffer[1024];
	
	//System output string
	char* str_system;
	
	//Bitmap header
	BITMAPFILEHEADER header;
	
	//2nd Bitmap header
	BITMAPINFOHEADER info_header;	
	
	//Image array
	IMAGE* input_image = (IMAGE*)malloc(sizeof(IMAGE));
		
	//Output array
	IMAGE* output_image = (IMAGE*)malloc(sizeof(IMAGE));
	
	//Brightness Threshold
	SINGLE_PIXEL* threshold = (SINGLE_PIXEL*)malloc(sizeof(SINGLE_PIXEL));
	
	//Allocate system string
	str_system = (char*)calloc(255,sizeof(char));
	
	//Size numberToFind
	int numberToFind;
	
	
	
	
	//-------Check for command line variables-------//
	
	if(argc!=7)
	{
		printf("\nIncorrect Syntax\n\nSYNTAX:\n./vision -f [filename] -o [output filename] -n [number of lines]\n\n");
		return EXIT_FAILURE;
	}
	else
	{
		//find input filename
		for(i=0; i<6; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='f')
			{
				strcpy(input_filename,argv[i+1]);
			}
		}
		
		
		//find output filename
		for(i=0; i<6; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='o')
			{
				strcpy(output_filename, argv[i+1]);
			}
		}
		
		//find number of lines - not implimented yet!
		for(i=0; i<6; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='n')
			{
				numberToFind=atoi(argv[i+1]);
			}
		}			
				
	}
	
	printf("\nInput Filename:\t\t%s", input_filename);
	printf("\nOutput Filename:\t%s", output_filename);
    
	//Force console output
	fflush(NULL);
	
	
	
	
	
	
	
	//-------Populate Bitmap Array-------//
	
	get_bitmap(input_filename, input_image);
	
	//Copy header information (used to produce the output image)
	copy_header(input_image, output_image);
	
	//Allocate memory for the x-dimention of the bitmap
	output_image->bitmap = (SINGLE_PIXEL**)calloc(sizeof(SINGLE_PIXEL*),output_image->info_header.width);
	
	//Allocate memory for the y-dimention of the bitmap
	for(i=0; i<(output_image->info_header.width); i++)
	{
		output_image->bitmap[i] = (SINGLE_PIXEL*)calloc(sizeof(SINGLE_PIXEL),output_image->info_header.height);
	}
	
	
	
	
	
	
	//------Process Image-------//
	
	printf("\nNumber of objects found: %d", process_image(input_image, output_image, numberToFind));
	
	printf("\n\n");
	
	
	
	
	
	
	
	//---Create output images---//	
	
	//Final output
	write_bitmap(output_filename, input_image);
	
	
	
	//Show output (*******MAC OSX ONLY!!!*******)
	//Concatinate system string
	strcpy(str_system, "open ");
	str_system = strcat(str_system, input_filename);
	str_system = strcat(str_system, " output.bmp 1.bmp 3.bmp 4.bmp 5.bmp 6.bmp 7.bmp 8.bmp 9.bmp -a preview");
	
	system(str_system);
	
	
	
	
	
	
	
	//-------Free up resources-------//
	for(i=0; i<input_image->info_header.width; i++)
	{
		free(input_image->bitmap[i]);
	}
	free(input_image->bitmap);
	
	
	for(i=0; i<output_image->info_header.width; i++)
	{
		free(output_image->bitmap[i]);
	}
	free(output_image->bitmap);
	
	return 0;
    
}

