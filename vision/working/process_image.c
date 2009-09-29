	/*process_image.c
 *
 *Author: R. Brooks Stephenson
 *Date: 1.30.2009
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "bitmap.h"

#define DEVIATION 0x20
#define YES 1
#define NO 0


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
	
	
	//Bounding Box Color
	SINGLE_PIXEL bndbox;
	
	//Filter threshold
	SINGLE_PIXEL* color_filter;
	
	//Array of objects	
	OBJECT* objects = (OBJECT*)malloc(sizeof(OBJECT)*NUMBER_OF_OBJECTS);
	
	//Clear objects array
	for(i=0; i<NUMBER_OF_OBJECTS; i++)
	{
		objects[i].number=0;
	}
	
	
	//Setup color filter
	color_filter->red = 0x73;
	color_filter->green = 0xCB;
	color_filter->blue = 0xA1;
	
	
	
	//edge_detect(input_image, output_image);
	filter(input_image, color_filter);
			
	//First stage output - edge detection
	write_bitmap("1_edge_detect.bmp", input_image);
	
	output_image = input_image;
	
	multiply_image(output_image, multiplier);
	
			
	//Second stage output - multiplier
	write_bitmap("2_multiply.bmp", output_image);
	
	threshold_image(output_image, threshold);
	
	//Third stage output - threshold
	write_bitmap("3_threshold.bmp", output_image);
	
	
	//---Check for objects---//
	find_objects(output_image->info_header.width, output_image->info_header.height, output_image, objects, threshold, deviation);
	

	//---Box all objects of interests---//
	for(i=1; i< NUMBER_OF_OBJECTS && objects[i].number>0; i++)
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
	
		boxbound(objects[i].top, objects[i].bottom, objects[i].left, objects[i].right, output_image, bndbox);
	}
	
	//Third stage output - edge detection
	write_bitmap("4_dirty_box.bmp", output_image);
	
	
	
	
	//---Size Threshold---//
	for(i=1; i< NUMBER_OF_OBJECTS && objects[i].number!=0 ;i++)
	{
		if((objects[i].right - objects[i].left) < size || (objects[i].bottom - objects[i].top) < size)
		{
			objects[i].active=0;
		}
	}
	
	//---Box all objects of interests after size threshold---//
	
	//Set boudning box color
	bndbox.red = 0xFF;
	bndbox.green = 0x00;
	bndbox.blue = 0x00;
	
	//Iterate through records and box appropriate objects
	for(i=1; i<NUMBER_OF_OBJECTS && objects[i].number>0; i++)
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
	
	//Free resources
	free(objects);
	
	//Return the number of objects found
	return num_objects;
}




//---Check pixel to see if it's part of an object---//
void find_objects(int x, int y, IMAGE* input_image, OBJECT* objects, SINGLE_PIXEL* threshold, SINGLE_PIXEL* deviation)
{
	//Local Vairbales
	
	//Array to keep track of objects that have been found.  Size of this is designated by x, y arguments.
	unsigned int** obj;
	
	//General Purpose Variables
	int i,j,k1,k2;
	
	//No duplicates tag
	short no_dup;
	
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
			if(input_image->bitmap[i][j].blue >threshold->blue || input_image->bitmap[i][j].green > threshold->green || input_image->bitmap[i][j].red > threshold->red )
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
	printf("\nRunning cleanup:");
	
	//Set the no_dup flag to the while loop will run at least once
	no_dup = 1;
	
	while(no_dup>0)
	{
	
		printf(".");
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
	
	
	
	printf("\nNumber of objects found by find_objects(): %d",num_objects);
	
	//Release resources
	free(obj);
	
	return;
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

	int i,j;

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
			if(i==input_image->info_header.width-1)
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
			if(i==input_image->info_header.width-1)
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
			if(i==input_image->info_header.width-1)
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




void filter(IMAGE* input_image, SINGLE_PIXEL* threshold)
{
	int x,y,i,j;
	
	char deviation;
	
	//get image size
	x = input_image->info_header.width;
	y = input_image->info_header.height;
	
	deviation = 0x5;
	
	for(j=0; j<y; j++)
	{
		for(i=0; i<x; i++)
		{
			if(input_image->bitmap[i][j].red < (threshold->red+deviation) && input_image->bitmap[i][j].red > (threshold->red-deviation) &&
				input_image->bitmap[i][j].green < (threshold->green+deviation) && input_image->bitmap[i][j].green > (threshold->green-deviation) &&
				input_image->bitmap[i][j].blue < (threshold->blue+deviation) && input_image->bitmap[i][j].blue > (threshold->blue-deviation))
			{
				;
			}
			else
			{
				input_image->bitmap[i][j].red = 0;
				input_image->bitmap[i][j].green = 0;
				input_image->bitmap[i][j].blue = 0;
			}
		}
	}
	
	
	
	return;
}

























