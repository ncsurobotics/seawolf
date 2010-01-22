/*process_image.c
 *
 *Author: R. Brooks Stephenson
 *Date: 2.21.2009
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include "bitmap.h"

#define DEVIATION 0x20
#define YES 1
#define NO 0
#define PI 3.1415927f

#define REDUCED 0
#define ALL 1

#define INTENSITY_ADDED 1
#define SAMPLES_PER_UNIT 8.0f
#define HOUGH_ANGLE 180



//---Globals---//

//Number of objects so far
unsigned int num_objects;

//---The main image processing function by which all other processes are called---//
int process_image(IMAGE* input_image, IMAGE* output_image, SINGLE_PIXEL* threshold, int size, SINGLE_PIXEL* deviation, SINGLE_PIXEL* multiplier)
{
	
	//---Local Variables---//
	
	//General purpose variables
	int i,j,k;
	
	//Generic pixel for holding temporary 
	unsigned char average;	
	
	//Hough Transform image
	IMAGE* hough_image;
	
	//Array of objects
	OBJECT* objects;
	
	//Hough Treshold
	SINGLE_PIXEL hough_threshold;
	

	//---The order of these operations is best suited to find lines in images---//
	
		
	//First stage output - edge detection
	edge_detect(input_image, output_image);
	write_bitmap("1_edge_detect.bmp", output_image);
	
	//Second stage output - multiplier
	multiply_image(output_image, multiplier);
	write_bitmap("2_multiply.bmp", output_image);

	//Third stage output - convert to black and white
	bw(output_image, output_image, 1);
	write_bitmap("3_bw.bmp", output_image);
	
	//Fourth Stage Perform hough transform
	hough_image = hough(output_image, threshold);
	write_bitmap("4_hough.bmp", hough_image);
	
	//---Manipulate hough transform---//
	hough_threshold.red = 80;
	hough_threshold.green = 0x00;//histogram(hough_image);
	hough_threshold.blue = 0x00;
	
	
	//Fifth stage output - threshold
	threshold_image(output_image, threshold);
	write_bitmap("5_threshold.bmp", output_image);
	
	
	
	
	//---Check for objects---//
	objects = find_objects(hough_image, &hough_threshold, deviation);
	write_bitmap("6_dirty_box.bmp",hough_image);
	
	
	//---Size Threshold---//
	for(i=1; i< MAX_NUMBER_OF_OBJECTS && objects[i].number!=0 ;i++)
	{
		if((objects[i].right - objects[i].left) < size || (objects[i].bottom - objects[i].top) < size)
		{
			objects[i].active=0;
		}
	}
	
	box_objects(objects, hough_image, REDUCED);
	//Sixth stage output - object detection
	//write_bitmap("6_dirty_box.bmp", hough_image);
	
	hough_lines(objects, input_image, hough_image->info_header.height);
		
	//Free resources
	free(objects);
	
	//Return the number of objects found
	return num_objects;
}















//---Check pixel to see if it's part of an object---//
OBJECT* find_objects(IMAGE* input_image, SINGLE_PIXEL* threshold, SINGLE_PIXEL* deviation)
{
	//Local Vairbales
	
	//Array to keep track of objects that have been found.  Size of this is designated by x, y arguments.
	unsigned int** obj;
	
	OBJECT* objects;
	
	//General Purpose Variables
	int i,j,k1,k2,x,y;
	
	//No duplicates tag
	short no_dup;
	
	//Set width and height
	x = input_image->info_header.width;
	y = input_image->info_header.height;
	
	//Allocate memory for object variable
	objects = (OBJECT*)calloc(MAX_NUMBER_OF_OBJECTS,sizeof(OBJECT));
	
	//Allocate array of pointers
	obj = (unsigned int**)malloc(sizeof(unsigned int*)*x);
	
	//Allocate the width dimention of the array
	for(i=0; i<x; i++)
	{
		obj[i] = (unsigned int*)malloc(sizeof(unsigned int)*y);
	}
	
	//Set the number of objects to zero
	num_objects=0;
	
	//clear the map
	for(j=0; j<y; j++)
	{
		for(i=0; i<x; i++)
		{
			obj[i][j]=0;
		}
	}

	
	//Iterate through image to find all the objects
	for(j=0; j<y; j++)
	{
		for(i=0; i<x; i++)
		{
			//Check to see if the pixel is above the threshold value
			if(  input_image->bitmap[i][j].blue >threshold->blue || input_image->bitmap[i][j].green > threshold->green || input_image->bitmap[i][j].red > threshold->red  )
			{						
				//Check to see if a surrounding pixel is a member of an object
				
				//Check the left pixel
				if(i>0 && obj[i-1][j]!=0)
				{
					if(objects[obj[i-1][j]].right < i)
					{
						objects[obj[i-1][j]].right = i;
					}
					
					obj[i][j] = obj[i-1][j];
					
				}
				//Check the upper left pixel
				else if(i>0 && j>0 && obj[i-1][j-1]!=0)
				{
					if(objects[obj[i-1][j-1]].right < i)
					{
						objects[obj[i-1][j-1]].right = i;
					}
					
					if(objects[obj[i-1][j-1]].bottom < j)
					{
						objects[obj[i-1][j-1]].bottom = j;
					}
					
					obj[i][j] = obj[i-1][j-1];
					
				}
				//Check the upper pixel
				else if(j>0 && obj[i][j-1]!=0)
				{
				
					if(objects[obj[i][j-1]].bottom < j)
					{
						objects[obj[i][j-1]].bottom = j;
					}
					
					obj[i][j] = obj[i][j-1];
					
				}
				//Check the upper right pixel
				else if(i<(x-1) && j>0 && obj[i+1][j-1]!=0)
				{
					if(objects[obj[i+1][j-1]].left > i)
					{
						objects[obj[i+1][j-1]].left = i;
					}
					
					if(objects[obj[i+1][j-1]].bottom < j)
					{
						objects[obj[i+1][j-1]].bottom = j;
					}
					
					obj[i][j] = obj[i+1][j-1];
					
				}
				//Check the right pixel
				else if(i<(x-1) && obj[i+1][j]!=0)
				{
					if(objects[obj[i+1][j]].right > i)
					{
						objects[obj[i+1][j]].right = i;
					}
					
					obj[i][j] = obj[i+1][j];
				}
				//Check the lower right pixel
				else if(i<(x-1) && j<(y-1) && obj[i+1][j+1]!=0)
				{
					if(objects[obj[i+1][j+1]].left > i)
					{
						objects[obj[i+1][j+1]].left = i;
					}
					
					if(objects[obj[i+1][j+1]].top > j)
					{
						objects[obj[i+1][j+1]].top = j;
					}
					
					obj[i][j] = obj[i+1][j+1];
					
				}
				//Check the lower pixel
				else if(j<(y-1) && obj[i][j+1]!=0)
				{
				
					if(objects[obj[i][j+1]].top > j)
					{
						objects[obj[i][j+1]].top = j;
					}
					
					obj[i][j] = obj[i][j+1];
					
				}
				//Check the lower left pixel
				else if(i<0 && j<(y-1) && obj[i-1][j+1]!=0)
				{
					if(objects[obj[i-1][j+1]].left > i)
					{
						objects[obj[i-1][j+1]].left = i;
					}
					
					if(objects[obj[i-1][j+1]].top > j)
					{
						objects[obj[i-1][j+1]].top = j;
					}
					
					obj[i][j] = obj[i-1][j+1];
					
				}
				else
				{
					num_objects++;
					obj[i][j]=num_objects;
					objects[num_objects].number=num_objects;
					objects[num_objects].top=j;
					objects[num_objects].bottom=j;
					objects[num_objects].left=i;
					objects[num_objects].right=i;
					objects[num_objects].active=YES;
				}
				
			}
			
		}
	}
	
	
	//Eleimate multiple taggings of the same object
	printf("\nRunning cleanup...");
	
	//Set the no_dup flag to the while loop will run at least once
	no_dup = 1;
	
	while(no_dup>0)
	{
	
		//printf(".");
		fflush(NULL);
		//Reset the flag before iterating through image
		no_dup=0;
	
		for(j=0; j<y; j++)
		{
			for(i=0; i<x; i++)
			{
				//Check to see if the current pixel is a member of an object
				if(obj[i][j]!=0)
				{
				
					//Check to see if a surrounding pixel is a member of an object
					
					//Check the left pixel
					if(i>0 && obj[i-1][j]!=0 && (k1=obj[i-1][j])!=(k2=obj[i][j]))
					{
						
						combine_objects(obj[i][j], obj[i-1][j], objects);
						
						if(k1>k2)
							obj[i-1][j]=k2;
						else
							obj[i][j]=k1;
							
						no_dup = 1;
						
					}
					//Check the upper left pixel
					else if(i>0 && j>0 && obj[i-1][j-1]!=0 && (k1=obj[i-1][j-1])!=(k2=obj[i][j]))
					{
					
						combine_objects(obj[i][j], obj[i-1][j-1], objects);
						
						if(k1>k2)
							obj[i-1][j-1]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
						
					}
					//Check the upper pixel
					else if(j>0 && obj[i][j-1]!=0 && (k1=obj[i][j-1])!=(k2=obj[i][j]))
					{
					
						combine_objects(obj[i][j], obj[i][j-1], objects);
						
						if(k1>k2)
							obj[i][j-1]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
						
					}
					//Check the upper right pixel
					else if(i<(x-1) && j>0 && obj[i+1][j-1]!=0 && (k1=obj[i+1][j-1])!=(k2=obj[i][j]))
					{
					
						combine_objects(obj[i][j], obj[i+1][j-1], objects);
						
						if(k1>k2)
							obj[i+1][j-1]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
						
					}
					//Check the right pixel
					else if(i<(x-1) && obj[i+1][j]!=0 && (k1=obj[i+1][j])!=(k2=obj[i][j]))
					{
						
						combine_objects(obj[i][j], obj[i+1][j], objects);
						
						if(k1>k2)
							obj[i+1][j]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
						
					}
					//Check the lower right pixel
					else if(i<(x-1) && j<(y-1) && obj[i+1][j+1]!=0 && (k1=obj[i+1][j+1])!=(k2=obj[i][j]))
					{
						
						combine_objects(obj[i][j], obj[i+1][j+1], objects);
						
						if(k1>k2)
							obj[i+1][j+1]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
						
					}
					//Check the lower pixel
					else if(j<(y-1) && obj[i][j+1]!=0 && (k1=obj[i][j+1])!=(k2=obj[i][j]))
					{
					
						combine_objects(obj[i][j], obj[i][j+1], objects);
						
						if(k1>k2)
							obj[i][j+1]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
						
					}
					//Check the lower left pixel
					else if(i<0 && j<(y-1) && obj[i-1][j+1]!=0 && (k1=obj[i-1][j+1])!=(k2=obj[i][j]))
					{
						
						combine_objects(obj[i][j], obj[i-1][j+1], objects);
						
						if(k1>k2)
							obj[i-1][j+1]=k2;
						else
							obj[i][j]=k1;
						
						no_dup = 1;
					}
				}

			}
			
		}
				
	}
	
	
	
	printf("Done\n\nNumber of objects found before cleanup: %d",num_objects);
	
	//Release resources
	free(obj);
	
	return objects;
}


















//---Box the region of interest---//
int boxbound(int top, int bottom, int left, int right, IMAGE* input_image, SINGLE_PIXEL bndbox)
{
	//---Local Variables---//
	int i,j;
	
	//Draw top
	for(i=left; i<=right; i++)
	{
		input_image->bitmap[i][top].blue=bndbox.blue;
		input_image->bitmap[i][top].green=bndbox.green;
		input_image->bitmap[i][top].red=bndbox.red;
	}
	
	//Draw Bottom
	for(i=left; i<=right; i++)
	{
		input_image->bitmap[i][bottom].blue=bndbox.blue;
		input_image->bitmap[i][bottom].green=bndbox.green;
		input_image->bitmap[i][bottom].red=bndbox.red;
	}
	
	//Draw left
	for(j=top; j<=bottom; j++)
	{
		input_image->bitmap[left][j].blue=bndbox.blue;
		input_image->bitmap[left][j].green=bndbox.green;
		input_image->bitmap[left][j].red=bndbox.red;
	}
	
	//Draw right
	for(j=top; j<=bottom; j++)
	{
		input_image->bitmap[right][j].blue=bndbox.blue;
		input_image->bitmap[right][j].green=bndbox.green;
		input_image->bitmap[right][j].red=bndbox.red;
	}
}






//Performs x-axis and y-axis differentiation on objects to detect edges based on change in color brightness
void edge_detect(IMAGE* input_image, IMAGE* output_image)
{

	//Local Variables
	int i,j;
	
	/*New edge-detected-image
	IMAGE* output_image;
	
	//Allocate memory for image
	output_image = (IMAGE*)calloc(1, sizeof(IMAGE));
	
	//Allocate memory for x-axis
	output_image->bitmap = (SINGLE_PIXEL**)calloc((int)(input_image->info_header.width), sizeof(SINGLE_PIXEL*));
		
	//Allocate memory for the other rows of the lookup table
	for(i=0; i< (input_image->info_header.width); i++)
	{
		output_image->bitmap[i] = (SINGLE_PIXEL*)calloc((int)(input_image->info_header.height), sizeof(SINGLE_PIXEL));
	}
	
	//Set output image dimentions to be the same as the input image
	output_image->info_header.width =input_image->info_header.width;
	output_image->info_header.height = input_image->info_header.height;
	*/
	
	

	//---Perform blue X-axis differentiation---//
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<input_image->info_header.width; i++)
		{
			//If the current pixel is the last pixel, set the output to be the zero there, and do not diffentiate it
			if(i==input_image->info_header.width-1)
			{
				output_image->bitmap[i][j].blue = 0x00;
				continue;
			}
			
			//Get the positive difference of the current pixel and the next
			if(input_image->bitmap[i][j].blue >= input_image->bitmap[i+1][j].blue)
			{
				output_image->bitmap[i][j].blue = (input_image->bitmap[i][j].blue - input_image->bitmap[i+1][j].blue);
			}
			else
			{
				output_image->bitmap[i][j].blue = (input_image->bitmap[i+1][j].blue - input_image->bitmap[i][j].blue);
			}
	
		}
	}
	
	
	//---Perform blue Y-axis differentiation---//
	for(i=0; i<input_image->info_header.width; i++)
	{
		for(j=0;j<input_image->info_header.height; j++)
		{
			//If the current pixel is the last pixel, set the output to be the zero there, and do not diffentiate it
			if(j==input_image->info_header.height-1)
			{
				output_image->bitmap[i][j].blue = 0x00;
				continue;
			}
			
			//Get the positive difference of the current pixel and the next
			if(input_image->bitmap[i][j].blue >= input_image->bitmap[i][j+1].blue)
			{
				output_image->bitmap[i][j+1].blue = output_image->bitmap[i][j+1].blue + (input_image->bitmap[i][j].blue - input_image->bitmap[i][j+1].blue);
			}
			else
			{
				output_image->bitmap[i][j].blue = output_image->bitmap[i][j+1].blue + (input_image->bitmap[i][j+1].blue - input_image->bitmap[i][j].blue);
			}
	
		}
	}	
	
	
	//---Perform Green X-axis differentiation---//
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<input_image->info_header.width; i++)
		{
			//If the current pixel is the last pixel, set the output to be the zero there, and do not diffentiate it
			if(i==input_image->info_header.width-1)
			{
				output_image->bitmap[i][j].green = 0x00;
				continue;
			}
			
			//Get the positive difference of the current pixel and the next
			if(input_image->bitmap[i][j].green >= input_image->bitmap[i+1][j].green)
			{
				output_image->bitmap[i][j].green = (input_image->bitmap[i][j].green - input_image->bitmap[i+1][j].green);
			}
			else
			{
				output_image->bitmap[i][j].green = (input_image->bitmap[i+1][j].green - input_image->bitmap[i][j].green);
			}
	
		}
	}
	
	
	//---Perform Green Y-axis differentiation---//
	for(i=0; i<input_image->info_header.width; i++)
	{
		for(j=0;j<input_image->info_header.height; j++)
		{
			//If the current pixel is the last pixel, set the output to be the zero there, and do not diffentiate it
			if(j==input_image->info_header.height-1)
			{
				output_image->bitmap[i][j].green = 0x00;
				continue;
			}
			
			//Get the positive difference of the current pixel and the next
			if(input_image->bitmap[i][j].green >= input_image->bitmap[i][j+1].green)
			{
				output_image->bitmap[i][j+1].green = output_image->bitmap[i][j+1].green + (input_image->bitmap[i][j].green - input_image->bitmap[i][j+1].green);
			}
			else
			{
				output_image->bitmap[i][j].green = output_image->bitmap[i][j+1].green + (input_image->bitmap[i][j+1].green - input_image->bitmap[i][j].green);
			}
	
		}
	}
	
	
	
	//---Perform red X-axis differentiation---//
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<input_image->info_header.width; i++)
		{
			//If the current pixel is the last pixel, set the output to be the zero there, and do not diffentiate it
			if(i==input_image->info_header.width-1)
			{
				output_image->bitmap[i][j].red = 0x00;
				continue;
			}
			
			//Get the positive difference of the current pixel and the next
			if(input_image->bitmap[i][j].red >= input_image->bitmap[i+1][j].red)
			{
				output_image->bitmap[i][j].red = (input_image->bitmap[i][j].red - input_image->bitmap[i+1][j].red);
			}
			else
			{
				output_image->bitmap[i][j].red = (input_image->bitmap[i+1][j].red - input_image->bitmap[i][j].red);
			}
	
		}
	}
	
	
	//---Perform red Y-axis differentiation---//
	for(i=0; i<input_image->info_header.width; i++)
	{
		for(j=0;j<input_image->info_header.height; j++)
		{
			//If the current pixel is the last pixel, set the output to be the zero there, and do not diffentiate it
			if(j==input_image->info_header.height-1)
			{
				output_image->bitmap[i][j].red = 0x00;
				continue;
			}
			
			//Get the positive difference of the current pixel and the next
			if(input_image->bitmap[i][j].red >= input_image->bitmap[i][j+1].red)
			{
				output_image->bitmap[i][j+1].red = output_image->bitmap[i][j+1].red + (input_image->bitmap[i][j].red - input_image->bitmap[i][j+1].red);
			}
			else
			{
				output_image->bitmap[i][j].red = output_image->bitmap[i][j+1].red + (input_image->bitmap[i][j+1].red - input_image->bitmap[i][j].red);
			}
	
		}
	}
	
	return;
	
}




void multiply_image(IMAGE* input_image, SINGLE_PIXEL* multiplier)
{
	int i,j,k;

	//---Perform Mutlipy---//
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<input_image->info_header.width; i++)
		{
		
			if(input_image->bitmap[i][j].blue * multiplier->blue < 0xFF)
				input_image->bitmap[i][j].blue = input_image->bitmap[i][j].blue * multiplier->blue;
			else input_image->bitmap[i][j].blue = 0xFF;
			
			if(input_image->bitmap[i][j].green * multiplier->green < 0xFF)
				input_image->bitmap[i][j].green = input_image->bitmap[i][j].green * multiplier->green;
			else input_image->bitmap[i][j].green = 0xFF;
			
			if(input_image->bitmap[i][j].red * multiplier->red < 0xFF)
				input_image->bitmap[i][j].red = input_image->bitmap[i][j].red * multiplier->red;
			else input_image->bitmap[i][j].red = 0xFF;
								
		}
	}
	
	return;
	
}


















//Performs a threshold calculation on an image given a threahold value
void threshold_image(IMAGE* input_image, SINGLE_PIXEL* threshold)
{
	int i,j;

	//---Perform Threshold---//
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0;i<input_image->info_header.width; i++)
		{
		
			//Blue Threshold
			if(input_image->bitmap[i][j].blue > threshold->blue)
			{
				input_image->bitmap[i][j].blue=0xFF;
			}
			else
			{
				input_image->bitmap[i][j].blue=0x00;
			}
			
			//Green Threshold
			if(input_image->bitmap[i][j].green > threshold->green)
			{
				input_image->bitmap[i][j].green=0xFF;
			}
			else
			{
				input_image->bitmap[i][j].green=0x00;
			}
			
			//Red Threshold
			if(input_image->bitmap[i][j].red > threshold->red)
			{
				input_image->bitmap[i][j].red=0xFF;
			}
			else
			{
				input_image->bitmap[i][j].red=0x00;
			}
					
		}
	}
	
	return;
}




//Combine two objects
void combine_objects(int obj1, int obj2, OBJECT* objects)
{
	//Local variables
	
	//General purpose variables
	int i, j;

	//printf("\nFound overlap on objects:%d\tand\t%d",obj1,obj2);

	//combine the higher numbered object into the lower numbered one
	if(obj1 < obj2)
	{
		//Merge larger object into the lower nmbered one
		if(objects[obj2].left < objects[obj1].left)
			objects[obj1].left = objects[obj2].left;
		
		if(objects[obj2].right > objects[obj1].right)
			objects[obj1].right = objects[obj2].right;
			
		if(objects[obj2].top < objects[obj1].top)
			objects[obj1].top = objects[obj2].top;
		
		if(objects[obj2].bottom > objects[obj1].bottom)
			objects[obj1].bottom = objects[obj2].bottom;
			
		//Invaidate the larger numbered object
		objects[obj2].active = NO;
	}
	else
	{
		//Merge larger object into the lower nmbered one
		if(objects[obj1].left < objects[obj2].left)
			objects[obj2].left = objects[obj1].left;
		
		if(objects[obj1].right > objects[obj2].right)
			objects[obj2].right = objects[obj1].right;
			
		if(objects[obj1].top < objects[obj2].top)
			objects[obj2].top = objects[obj1].top;
		
		if(objects[obj1].bottom > objects[obj2].bottom)
			objects[obj2].bottom = objects[obj1].bottom;
			
		//Invaidate the larger numbered object
		objects[obj1].active = NO;
	}
	
				
		
	return;
}


















//Changes a color input image into a black and white image
//mode: 0 for black and white, 1 for grey-scale
void bw(IMAGE* input_image, IMAGE* output_image, int mode)
{
	//Local variables
	int i, j;
	
	//Temp average color
	unsigned char temp;
	
	if(mode==0)
	{
		for(j=0; j<input_image->info_header.height; j++)
		{
			for(i=0;i<input_image->info_header.width; i++)
			{
			
				if(input_image->bitmap[i][j].blue > 0)
				{
					output_image->bitmap[i][j].blue = 0xFF;
					output_image->bitmap[i][j].green = 0xFF;
					output_image->bitmap[i][j].red = 0xFF;
				}
				
				if(input_image->bitmap[i][j].green > 0)
				{
					output_image->bitmap[i][j].blue = 0xFF;
					output_image->bitmap[i][j].green = 0xFF;
					output_image->bitmap[i][j].red = 0xFF;
				}
					
				if(input_image->bitmap[i][j].red > 0)
				{
					output_image->bitmap[i][j].blue = 0xFF;
					output_image->bitmap[i][j].green = 0xFF;
					output_image->bitmap[i][j].red = 0xFF;
				}
				
			}
		}
	}
	else
	{
		for(j=0; j<input_image->info_header.height; j++)
		{
			for(i=0;i<input_image->info_header.width; i++)
			{
			
				/*if(input_image->bitmap[i][j].red >= input_image->bitmap[i][j].green && input_image->bitmap[i][j].red >= input_image->bitmap[i][j].blue)
				{
					temp = input_image->bitmap[i][j].red;
				}
				else if(input_image->bitmap[i][j].green >= input_image->bitmap[i][j].red && input_image->bitmap[i][j].green >= input_image->bitmap[i][j].blue)
				{
					temp = input_image->bitmap[i][j].green;
				}
				else
				{
					temp = input_image->bitmap[i][j].blue;
				}*/
				
				temp = (input_image->bitmap[i][j].red + input_image->bitmap[i][j].green + input_image->bitmap[i][j].blue)/3;
				
				output_image->bitmap[i][j].red = temp;
				output_image->bitmap[i][j].green = temp;
				output_image->bitmap[i][j].blue = temp;				
			}
		}
	}
}



//Output the data for a histagram
unsigned char histogram(IMAGE* input_image)
{
	//Local variables
	int i,j,k,dev,x,y,max;
	
	//Threshold
	unsigned char threshold;
	
	//Standard Deviation
	double sta_dev;
	
	//Average value
	double avg;
	
	//File pointer
	FILE* fp;
	
	//Histagram IMAGE
	IMAGE* hist;
	
	//Average color
	int temp;
	
	//Array to hold the number of pixels with n brightness.
	unsigned int intensity[256];
	
	for(i=0; i<256; i++)
	{
		intensity[i]=0;
	}
	
	//Clear the standard deviation
	sta_dev=0;
	
	//Clear the Average
	avg = 0;
	
	//Clear the max
	max = 0;
	
	//Clear threshold
	threshold = 0;
	
	//Set x and y variables
	x = input_image->info_header.width;
	y = input_image->info_header.height;
	
	//Find the attributes of the image
	for(j=0; j<y; j++)
	{
		for(i=0;i<x; i++)
		{
			
			//Assign the temp value
			temp = (int)(input_image->bitmap[i][j].green);// + input_image->bitmap[i][j].green + input_image->bitmap[i][j].blue)/3;
			
			//Sum all the values
			avg+=temp;
						
			//Only incriment non-zero values
			if(temp!=0)	intensity[temp]+=1;
		}
	}
	
	//Devide by total number of pixels to get the average value
	avg = (avg/(x*y));
	
	//Calculate standard deviation
	for(j=0; j<y; j++)
	{
		for(i=0;i<x; i++)
		{
			temp = (int)(input_image->bitmap[i][j].green);
			
			if(temp!=0) sta_dev += ((temp - avg)*(temp - avg));
		}
	}
	
	//Finish calculating standard deviation
	sta_dev = sqrt(sta_dev);
	
	
	
	//Find the max number of pixels at any one intensity level
	for(i=0; i<255; i++)
	{
		if(intensity[i] > max) max = intensity[i];
	}
	
	
	
	//Calculate minimum threshold value
	threshold = (unsigned char)(max/600);	
	
	
	printf("\n\nStandard Deviation: %f", sta_dev);
	printf("\nMax: %d", max);
	printf("\nThreshold: %d", threshold);
	fflush(NULL);
		
	dev=1;
	
	//Open the file
	fp = fopen("histogram.txt", "w");
		
	for(i=0; i<256; i++)
	{
		k=0;
	
		for(j=i; j<i+dev; j++)
		{
			k+=intensity[j];
		}
		
		fprintf(fp, "%d,%u\n",i,k);
		
	}
	
	fclose(fp);
	
	
	//Return the appropriate hough threshold value
	return threshold;
			
}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


//Perform hough transform on image
IMAGE* hough(IMAGE* input_image, SINGLE_PIXEL* threshold)
{

	//Local variables
	int i,j,k,x,y;
	
	int b1, b2, x1, x2, y1, y2, length, x_intersection, y_intersection, temp, x_midpoint, y_midpoint, bounce_flag;
	
	float m1, m2, theta, alpha;
	
	//Lookup table for various images: row 0 is theta, row 1 is m1, row 2 is m2, and row 3 is alpha
	float** lookup;
	
	//hough transform image
	IMAGE* htrans;
	
	
	
	//Set x and y variables for easier code reading
	x = input_image->info_header.width;
	y = input_image->info_header.height;
	
	x_midpoint = (input_image->info_header.width)/2;
	y_midpoint = (input_image->info_header.height)/2;
	
	//Allocate memory for the image struct
	htrans = (IMAGE*)calloc(1,sizeof(IMAGE));
	
	
	
	//Allocate memory for the frist row of the lookup table
	lookup = (float**)calloc(HOUGH_ANGLE*SAMPLES_PER_UNIT, sizeof(float*));
		
	//Allocate memory for the other rows of the lookup table
	for(i=0; i< (HOUGH_ANGLE*SAMPLES_PER_UNIT); i++)
	{
		lookup[i] = (float*)calloc(4, sizeof(float));
	}
	
	
	
	//Allocate memory for x-asix of the bitmap
	htrans->bitmap = (SINGLE_PIXEL**)calloc((int)(HOUGH_ANGLE*SAMPLES_PER_UNIT), sizeof(SINGLE_PIXEL*));
	
	//Allocate memory for the y-axis of the bitmap
	for(i=0; i<(HOUGH_ANGLE*SAMPLES_PER_UNIT); i++)
	{
		htrans->bitmap[i] = (SINGLE_PIXEL*)calloc((int)sqrt(x*x+y*y),sizeof(SINGLE_PIXEL));
	}
	
	
	
	//Set image size
	htrans->info_header.width = (HOUGH_ANGLE*SAMPLES_PER_UNIT);
	htrans->info_header.height = (int)sqrt(x*x+y*y);
	
	
	
	printf("\n\nCalculating Hough Transform...");
	fflush(NULL);
	
	
	//Acutally Calculate the hough transform
	for(j=0; j<input_image->info_header.height; j++)
	{
		for(i=0; i<input_image->info_header.width; i++)
		{
		
			if(input_image->bitmap[i][j].blue >threshold->blue || input_image->bitmap[i][j].green > threshold->green || input_image->bitmap[i][j].red > threshold->red)
			{
				
				for(theta=0; theta<HOUGH_ANGLE; theta+=(1.0f/SAMPLES_PER_UNIT))
				{
				
					//Calculate the length of the tangent angle
					length = (int)(((i - x_midpoint)*cos(theta*PI/180) + (j - y_midpoint)*sin(theta*PI/180)));	
					
					//Scale max angle to match the width of the hough transform image
					alpha = (int)(theta*SAMPLES_PER_UNIT);
																																		
					//Save info to hough transfer image
					if(0xFF - htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].red >= INTENSITY_ADDED)
					{
						htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].red += INTENSITY_ADDED;
					}
					else if(0xFF - htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].green >= INTENSITY_ADDED)
					{
						htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].red = 0xFF;
						htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].green += INTENSITY_ADDED;
					}
					else if(0xFF - htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].blue >= INTENSITY_ADDED)
					{
						htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].red = 0xFF;
						htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].green = 0xFF;
						htrans->bitmap[(int)alpha][(htrans->info_header.height/2)+length].blue += INTENSITY_ADDED;
					}
				}
				
			}
		}
	}
	
	printf("Done");
	fflush(NULL);
	
	return htrans;
	
}






















//Box all objects in input array
void box_objects(OBJECT* objects, IMAGE* input_image, int selection)
{
	//Local variables
	int i;
	
	//Bounding Box Color
	SINGLE_PIXEL bndbox;

	//Check to see if all, or just the reduced set, of objects are to be boxed
	if(selection!=0)
	{
		//---Box all objects of interests---//
		for(i=1; i< MAX_NUMBER_OF_OBJECTS && objects[i].number>0; i++)
		{
			//Set bounding box color
			if((i-1)%3 == 0)
			{
				bndbox.red = 0xFF;
				bndbox.green = 0x00;
				bndbox.blue = 0x00;
			}
			else if((i-1)%3 == 1)
			{
				bndbox.red = 0x00;
				bndbox.green = 0xFF;
				bndbox.blue = 0x00;
			}
			else if((i-1)%3 == 2)
			{
				bndbox.red = 0x00;
				bndbox.green = 0x00;
				bndbox.blue = 0xFF;
			}
			else
			{
				bndbox.red = 0xFF;
				bndbox.green = 0x00;
				bndbox.blue = 0xFF;
			}			
		
			boxbound(objects[i].top, objects[i].bottom, objects[i].left, objects[i].right, input_image, bndbox);
		}
	}
	else
	{	
		
		//Set boudning box color
		bndbox.red = 0x00;
		bndbox.green = 0xFF;
		bndbox.blue = 0x00;
		
		//Iterate through records and box appropriate objects
		for(i=1; i<MAX_NUMBER_OF_OBJECTS && objects[i].number>0; i++)
		{
			if(objects[i].active==1)
			{
				boxbound(objects[i].top, objects[i].bottom, objects[i].left, objects[i].right, input_image, bndbox);
			}
			else 
			{
				num_objects--;
			}
		}
	}

	
	
	return;
}











void hough_lines(OBJECT* objects, IMAGE* input_image, int max_radius)
{
	//Local variables
	int i, j, k, n, x1, x2;
	float radius, alpha;
	
	//Iterate through records and draw appropriate lines
	for(k=1; k<MAX_NUMBER_OF_OBJECTS && objects[k].number>0; k++)
	{
		if(objects[k].active==1)
		{
			//Get average angle
			alpha = ((objects[k].left + objects[k].right)/2)/SAMPLES_PER_UNIT;

			//Get average radius
			radius = ((((objects[k].top + objects[k].bottom)/2)-(max_radius/2)));

			//Draw the line
			for(j=-(int)(input_image->info_header.height); j<(int)(input_image->info_header.height); j++)
			{
				i = (int)(radius - ((j)*sin(alpha*PI/180)))/(cos(alpha*PI/180)) + (input_image->info_header.width/2);
				
				//Set right bound
				x2 = (int)(radius - ((j+1)*sin(alpha*PI/180)))/(cos(alpha*PI/180)) + (input_image->info_header.width/2);
				
				if(i>0 && i<input_image->info_header.width && (j+input_image->info_header.height/2)>0 && (j+input_image->info_header.height/2)<input_image->info_header.height)				
				{
					input_image->bitmap[i][(j+input_image->info_header.height/2)].red = 0xFF;
					input_image->bitmap[i][(j+input_image->info_header.height/2)].green = 0x00;
					input_image->bitmap[i][(j+input_image->info_header.height/2)].blue = 0x00;
					
					//Fill in the pixels along the x-axis
					if(i<x2)
					{
						for(n=i; n<=x2; n++)
						{
							if(n>0 && n<input_image->info_header.width && (j+input_image->info_header.height/2)>0 && (j+input_image->info_header.height/2)<input_image->info_header.height)				
							{
								input_image->bitmap[n][(j+input_image->info_header.height/2)].red = 0xFF;
								input_image->bitmap[n][(j+input_image->info_header.height/2)].green = 0x00;
								input_image->bitmap[n][(j+input_image->info_header.height/2)].blue = 0x00;
							}
						}
					}
					else
					{
						for(n=i; n>=x2; n--)
						{
							if(n>0 && n<input_image->info_header.width && (j+input_image->info_header.height/2)>0 && (j+input_image->info_header.height/2)<input_image->info_header.height)				
							{
								input_image->bitmap[n][(j+input_image->info_header.height/2)].red = 0xFF;
								input_image->bitmap[n][(j+input_image->info_header.height/2)].green = 0x00;
								input_image->bitmap[n][(j+input_image->info_header.height/2)].blue = 0x00;
							}
						}
					}
				}
				
			}
			
		}

	}
	
	return;
}











//FFT function
void fft(IMAGE* input_image)
{
	/*//Local variables
	
	//Input image dimentions
	unsigned int x,y;
	
	//General indecies
	unsigned int i,j,k;
	
	//Size of sample block
	unsigned int size;
	
	//Sampling frequency
	float fs;
	float delta_f;
	
	//index
	unsigned int m;
	unsigned int k;
	
	//Sum
	float complex **sum;
	
	//Find input image dimentions
	x = (input_image->info_header.width);
	y = (input_image->info_header.height);
	
	
	//Allocate memory for sum variable
	sum = (float complex**)calloc(x,sizeof(float complex*));
	
	for(i=0; i<x; i++)
	{
		sum[i] = (float complex*)calloc(y, sizeof(float complex));
	}

	
	//Sampling time
	float ts;
	
	//Calculate the frequence step
	delta_f = fs/size;
	
	for(j=0; j<y; j++)
	{
		for(i=0; i<width; i++)
		{
			for(m=0; m<size-1; m++)
			{
				sum = ts*input_image->bitmap[0][m].red*exp((-I*2*PI)/size);
			}
		}
	}*/
	
	return;
	
}












