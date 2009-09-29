/*bitmap_io.c - part of the vision program
 *
 *
 * Opens a bitmap and returns the information.  Also can save a bitmap given the correct information
 *
 * Author: Robert Brooks Stephenson
 * Date: 1.30.2009
 *
 */
 
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "bitmap.h"

//Get bitmap
int get_bitmap(char* filename, IMAGE* input_image)
{
	//Input Image File Pointer
    FILE* ip;
	
	//Open file pointer
    ip=fopen(filename,"rb");
	
	//Buffer
	char buffer[1024];
	
	//General variables
	int i,j;
	
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
	
	//Allocate memory for the y-dimentino bitmap
	for(i=0; i<(input_image->info_header.width); i++)
	{
		input_image->bitmap[i] = (SINGLE_PIXEL*)malloc(sizeof(SINGLE_PIXEL)*input_image->info_header.height);
	}
	
	//Clost the bitmap
	fclose(ip);
		
	//Reopen the bitmap
	ip=fopen(filename,"rb");
	
	//go to bitmap
	fread(buffer,sizeof(char),input_image->file_header.offsetbits,ip);
	
	//Begin reading in the pixel data
	for(j=(input_image->info_header.height)-1; j>=0; j--)
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




int write_bitmap(char* filename, IMAGE* input_image)
{
	//Output Image File Pointer
	FILE* op;
	
	//Buffer
	char buffer[1024];
	
	//General variables
	int i,j;
	
	//Get file pointer
	op = fopen(filename, "wb");
	
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
	
	for(j=input_image->info_header.height; j>=0; j--)
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



//Copy one image header to another
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
	
	
	

