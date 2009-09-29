/*bitmap_io.c - part of the vision program
 *
 *
 * Opens a bitmap and returns the information.  Also can save a bitmap given the correct information
 *
 * Author: Robert Brooks Stephenson
 * Date: 7.1.2009
 *
 */







#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "bitmap.h"







/*get_bitmap function
 *
 * This function will attempt to open a 24-bit bitmap and store it into the IMAGE structure that is passed to it
 *
 * Return:	0 - Succeeded
 *			1 - Failure
 */

int get_bitmap(char* filename, IMAGE* input_image)
{
	//Input Image File Pointer
    FILE* ip;
	
	//Buffer
	unsigned char buffer[1024];
	
	//General variables
	int i,j;
	
	//Open file pointer
    ip=fopen(filename,"rb");
	
	//Open the header
	fread(&input_image->file_header.type,sizeof(unsigned short),1, ip);
	fread(&input_image->file_header.size, sizeof(unsigned long),1, ip);
	fread(&input_image->file_header.reserved1, sizeof(unsigned short),1, ip);
	fread(&input_image->file_header.reserved2, sizeof(unsigned short),1, ip);
	fread(&input_image->file_header.offsetbits, sizeof(unsigned long),1, ip);
	
	//Read in the Bitmap informaiton
	fread(&input_image->info_header.size, sizeof(input_image->info_header.size), 1, ip);	
	fread(&input_image->info_header.width, sizeof(input_image->info_header.width), 1, ip);	
	fread(&input_image->info_header.height, sizeof(input_image->info_header.height), 1, ip);	
	fread(&input_image->info_header.planes, sizeof(input_image->info_header.planes), 1, ip);	
	fread(&input_image->info_header.bitcount, sizeof(input_image->info_header.bitcount), 1, ip);	
	fread(&input_image->info_header.compression, sizeof(input_image->info_header.compression), 1, ip);	
	fread(&input_image->info_header.sizeimage, sizeof(input_image->info_header.sizeimage), 1, ip);	
	fread(&input_image->info_header.xpelspermeter, sizeof(input_image->info_header.xpelspermeter), 1, ip);	
	fread(&input_image->info_header.ypelspermeter, sizeof(input_image->info_header.ypelspermeter), 1, ip);	
	fread(&input_image->info_header.colorsused, sizeof(input_image->info_header.colorsused), 1, ip);
	fread(&input_image->info_header.colorsimportant, sizeof(input_image->info_header.colorsimportant), 1, ip);
	
	//Allocate memory for the x-dimention bitmap
	input_image->bitmap = (SINGLE_PIXEL**)malloc(sizeof(SINGLE_PIXEL*)*input_image->info_header.width);
	
	//Allocate memory for the y-dimention bitmap
	for(i=0; i<(input_image->info_header.width); i++)
	{
		input_image->bitmap[i] = (SINGLE_PIXEL*)malloc(sizeof(SINGLE_PIXEL)*input_image->info_header.height);
	}
	
	//Clost the bitmap file pointer
	fclose(ip);
		
	//Reopen the bitmap (to read from beginning)
	ip=fopen(filename,"rb");
	
	//Sktip info part of file and proceed to bitmap
	fread(buffer,sizeof(char),input_image->file_header.offsetbits,ip);
	
	//Begin reading in the pixel data
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<(input_image->info_header.width); i++)
		{
			fread(&input_image->bitmap[i][j].blue, sizeof(unsigned char), 1, ip);
			fread(&input_image->bitmap[i][j].green, sizeof(unsigned char), 1, ip);
			fread(&input_image->bitmap[i][j].red, sizeof(unsigned char), 1, ip);			
		}
		
		//Ignore the padding bits at the end of the line
		fread(buffer, sizeof(unsigned char),((input_image->info_header.width%4)),ip);
	}
	
	//Close the file
	fclose(ip);
	
	return 0;
	
}







/* write_bitmap functino
 *
 * This functino takes an IMAGE stuct and a char string and writes a bitmap
 *
 * NOTE: THE WIDTH, HEIGHT, AND COLOR DEPTH MUST ALREADY BE KNOWN (i.e. set the corresponding stuct values and make sure they match the bitmap array size)!!!!
 * NOTE:	If the color depth is not specified (or invalid) it will default to 24-bit color depth
 *
 *	IMPORTANT: Although color depths other than 24-bit are supported, they have not been tested!!!  Use at own risk!!
 */

int write_bitmap(char* filename, IMAGE* input_image)
{
	//Output Image File Pointer
	FILE* op;
	
	//Buffer
	unsigned char buffer[1024];
	
	//General variables
	int i,j;
	
	//Get file pointer
	op = fopen(filename, "wb");
	
	//Set header parameters
	//NOTE: THE WIDTH, HEIGHT, AND COLOR DEPTH MUST ALREADY BE KNOWN!!!!
	//NOTE:	If the color depth is not specified (or invalid) it will default to 24
	
	//Check for color depth
	if(input_image->info_header.bitcount!=32 || input_image->info_header.bitcount!=24 || input_image->info_header.bitcount!=16 || input_image->info_header.bitcount!=8)
	{
		input_image->info_header.bitcount = 24;
	}
	
	
	input_image->file_header.type = 0x4d42;	//0x4d42 in reverse order is ASCII "BM" to designate the file is of type "bitmap"
	input_image->file_header.size = (54 + ((input_image->info_header.width*input_image->info_header.bitcount)+input_image->info_header.width%32)*(input_image->info_header.height));
	input_image->file_header.reserved1 = 0;
	input_image->file_header.reserved2 = 0;
	input_image->file_header.offsetbits = 54;
	
	input_image->info_header.size = 40;
	input_image->info_header.width = input_image->info_header.width;
	input_image->info_header.height = input_image->info_header.height;
	input_image->info_header.planes = 1;
	input_image->info_header.compression = 0;
	input_image->info_header.sizeimage = (((input_image->info_header.width*input_image->info_header.bitcount)+input_image->info_header.width%32)*(input_image->info_header.height));
	input_image->info_header.xpelspermeter = 2835;
	input_image->info_header.ypelspermeter = 2835;
	input_image->info_header.colorsused = 0;
	input_image->info_header.colorsimportant = 0;

	
	//Write DIB Header
	fwrite(&input_image->file_header.type, sizeof(input_image->file_header.type), 1, op);
	fwrite(&input_image->file_header.size, sizeof(input_image->file_header.size), 1, op);
	fwrite(&input_image->file_header.reserved1, sizeof(input_image->file_header.reserved1), 1, op);
	fwrite(&input_image->file_header.reserved2, sizeof(input_image->file_header.reserved2), 1, op);
	fwrite(&input_image->file_header.offsetbits, sizeof(input_image->file_header.offsetbits), 1, op);
	
	//Write Bitmap header
	fwrite(&input_image->info_header.size, sizeof(input_image->info_header.size), 1, op);
	fwrite(&input_image->info_header.width, sizeof(input_image->info_header.width), 1, op);
	fwrite(&input_image->info_header.height, sizeof(input_image->info_header.height), 1, op);
	fwrite(&input_image->info_header.planes, sizeof(input_image->info_header.planes), 1, op);
	fwrite(&input_image->info_header.bitcount, sizeof(input_image->info_header.bitcount), 1, op);
	fwrite(&input_image->info_header.compression, sizeof(input_image->info_header.compression), 1, op);
	fwrite(&input_image->info_header.sizeimage, sizeof(input_image->info_header.sizeimage), 1, op);
	fwrite(&input_image->info_header.xpelspermeter, sizeof(input_image->info_header.xpelspermeter), 1, op);
	fwrite(&input_image->info_header.ypelspermeter, sizeof(input_image->info_header.ypelspermeter), 1, op);
	fwrite(&input_image->info_header.colorsused, sizeof(input_image->info_header.colorsused), 1, op);
	fwrite(&input_image->info_header.colorsimportant, sizeof(input_image->info_header.colorsimportant), 1, op);
	
	//Write the actual bitmap data
	
	//Clear the buffer so that it can be used to "pad" the ends of the scanline if needed
	buffer[0]=0xFF;
	buffer[1]=0xFF;
	buffer[2]=0xFF;
	buffer[3]=0xFF;
	
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<input_image->info_header.width; i++)
		{
			fwrite(&input_image->bitmap[i][j].blue, sizeof(unsigned char), 1, op);
			fwrite(&input_image->bitmap[i][j].green, sizeof(unsigned char), 1, op);
			fwrite(&input_image->bitmap[i][j].red, sizeof(unsigned char), 1, op);			
		}
		
		//Add the padding bits at the end of the line, if needed
		fwrite(buffer, sizeof(unsigned char),((input_image->info_header.width%4)),op);
	}
	
	
	fclose(op);
	
	return 0;
	
}







/* copy_header functino
 *
 * This function copies the header information of one bitmap to another.
 * Useful when you want to duplicate the an image, but don't want to set the bitmap parameters by hand.
 */

 int copy_header(IMAGE* input_image, IMAGE* output_image)
{
	output_image->file_header.type = input_image->file_header.type;
	output_image->file_header.size = input_image->file_header.size;
	output_image->file_header.reserved1 = input_image->file_header.reserved1;
	output_image->file_header.reserved2 = input_image->file_header.reserved2;
	output_image->file_header.offsetbits = input_image->file_header.offsetbits;
	
	output_image->info_header.size = input_image->info_header.size;
	output_image->info_header.width = input_image->info_header.width;
	output_image->info_header.height = input_image->info_header.height;
	output_image->info_header.planes = input_image->info_header.planes;
	output_image->info_header.bitcount = input_image->info_header.bitcount;
	output_image->info_header.compression = input_image->info_header.compression;
	output_image->info_header.sizeimage = input_image->info_header.sizeimage;
	output_image->info_header.xpelspermeter = input_image->info_header.xpelspermeter;
	output_image->info_header.ypelspermeter = input_image->info_header.ypelspermeter;
	output_image->info_header.colorsused = input_image->info_header.colorsused;
	output_image->info_header.colorsimportant = input_image->info_header.colorsimportant;
	
	return 0;
}
	
	
	



/* print_image_header function
 *
 * Prints the header prperties to the console.
 * Useful for debugging.
 */
void print_image_header(IMAGE* input_image)
{
	//Print out the header of the input image
	//Write DIB Header
	printf("\ntype: %x",input_image->file_header.type);
	printf("\nsize: %d",input_image->file_header.size);
	printf("\nreserved1: %d",input_image->file_header.reserved1);
	printf("\nreserved2: %d",input_image->file_header.reserved2);
	printf("\noffsetbits: %d",input_image->file_header.offsetbits);
	
	//Write Bitmap header
	printf("\n\nsize: %d",input_image->info_header.size);
	printf("\nwidth: %d",input_image->info_header.width);
	printf("\nheight: %d",input_image->info_header.height);
	printf("\nplanes: %d",input_image->info_header.planes);
	printf("\nbitcount: %d",input_image->info_header.bitcount);
	printf("\ncompression: %d",input_image->info_header.compression);
	printf("\nsizeimage: %d",input_image->info_header.sizeimage);
	printf("\nxpelspermeter: %d",input_image->info_header.xpelspermeter);
	printf("\nypelspermeter: %d",input_image->info_header.ypelspermeter);
	printf("\ncolorsused: %d",input_image->info_header.colorsused);
	printf("\ncolorsimportant: %d",input_image->info_header.colorsimportant);
	
}

