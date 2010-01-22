/*main.c - part of the vision program
 *
 * Author: Robert Brooks Stephenson
 * Date: 1.30.2009
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <strings.h>
#include "bitmap.h"

/*TODO:
 *add command line support
 */

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
	
	//Size Threshold
	int size;
	
	//Deviation
	SINGLE_PIXEL* deviation = (SINGLE_PIXEL*)malloc(sizeof(SINGLE_PIXEL));
	
	//Multiplier
	SINGLE_PIXEL* multiplier = (SINGLE_PIXEL*)malloc(sizeof(SINGLE_PIXEL));
	
	//Check for command line variables
	if(argc!=13)
	{
		printf("\nIncorrect Syntax\n\nSYNTAX:\n./vision -f [filename] -o [output filename] -t [brightness threshold (8-bit number)] -s [size threshold (8-bit number)] -d [deviation (8 bit number)] -m [multiplier (8 bit number)]\n\n");
		return EXIT_FAILURE;
	}
	else
	{
		//find input filename
		for(i=0; i<12; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='f')
			{
				strcpy(input_filename,argv[i+1]);
			}
		}
		
		
		//find output filename
		for(i=0; i<12; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='o')
			{
				strcpy(output_filename, argv[i+1]);
			}
		}
		
		//find brightness threshold
		for(i=0; i<12; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='t')
			{
				threshold->blue = (unsigned char)atoi(argv[i+1]);
				threshold->green = (unsigned char)atoi(argv[i+1]);
				threshold->red = (unsigned char)atoi(argv[i+1]);
			}
		}
		
		//find size threshold
		for(i=0; i<12; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='s')
			{
				size = atoi(argv[i+1]);
			}
		}
		
		//find deviation
		for(i=0; i<12; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='d')
			{
				deviation->blue = (unsigned char)atoi(argv[i+1]);
				deviation->green = (unsigned char)atoi(argv[i+1]);
				deviation->red = (unsigned char)atoi(argv[i+1]);
			}
		}
		
		//find multiplier
		for(i=0; i<12; i++)
		{
			if(argv[i][0]=='-' && argv[i][1]=='m')
			{
				multiplier->blue = (unsigned char)atoi(argv[i+1]);
				multiplier->green = (unsigned char)atoi(argv[i+1]);
				multiplier->red = (unsigned char)atoi(argv[i+1]);
			}
		}
			
				
	}
	
	printf("\nInput Filename:\t\t%s", input_filename);
	printf("\nOutput Filename:\t%s", output_filename);
    
	//Force console output
	fflush(NULL);
	
	
	//Populate Bitmap Array
	get_bitmap(input_filename, input_image);
	
	//Copy header information
	copy_header(input_image, output_image);
	
	//Allocate memory for the x-dimention bitmap
	output_image->bitmap = (SINGLE_PIXEL**)malloc(sizeof(SINGLE_PIXEL*)*output_image->info_header.width);
	
	//Allocate memory for the y-dimentino bitmap
	for(i=0; i<(output_image->info_header.width); i++)
	{
		output_image->bitmap[i] = (SINGLE_PIXEL*)malloc(sizeof(SINGLE_PIXEL)*output_image->info_header.height);
	}
			
	//Clear the output array
	for(j=0; j<output_image->info_header.height; j++)
	{
		for(i=0;i<output_image->info_header.width; i++)
		{
			output_image->bitmap[i][j].blue = 0x00;
			output_image->bitmap[i][j].green = 0x00;
			output_image->bitmap[i][j].red = 0x00;
		}
	}

	
	//Process Image
	printf("\nNumber of objects found: %d", process_image(input_image, output_image, threshold, size, deviation, multiplier));
	
	printf("\n\n");
	
	//---Create output images---//	
	//Final output
	write_bitmap(output_filename, input_image);
	
	//Show output (*******MAC OSX ONLY!!!*******)
	system("open test_4.bmp output.bmp 1_edge_detect.bmp 2_multiply.bmp 3_threshold.bmp 4_dirty_box.bmp -a preview");
	
	
	//Free up resources
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

