//************************************************
//	target_color.c: 
//
//	Houses FindTargetColor() and related functions
//	      - returns a blacked-out IplImage (black is
//			not the color you are looking for)
//

#include "vision_lib.h"
#include <stdio.h>
#include <cv.h>
#include <highgui.h>  

int FindTargetColor(IplImage* in, IplImage* out, RGBPixel* color, int min_blobsize, int dev_threshold){ //should find the set of colors closest to the target color
    int i,j,s;
    int* sigmas; //holds the accumulation for all possible standard deviations in the image
    int blobsize = 0; //current number of pixels found in color "blob" (not necceserily a single blob)
    int stddev; //the computed maximum allowable stddev
    int averagestddev; //the average stddev from target color
    int smallest_stddev = -1; //the smallest stddev found
    double imgAverage_r=0; //hold average colors for this image as doubles
    double imgAverage_g=0;
    double imgAverage_b=0;
    uchar* ptrIn = (uchar*) in->imageData;
    uchar* ptrOut = (uchar*) out->imageData;
    RGBPixel imgAverage;
    RGBPixel tempPixel;

    sigmas = (int*)calloc(444,sizeof(int)); //allocate memory for sigma table (max sigma is sqrt(256^2 + 256^2 + 256^2) ) 

    //initialize tables
    for(i=0;i<444;i++)
	sigmas[i] = 0;
  
   
    for(i=in->width*in->height; i>=0;i--){ //fill the acumulator tables 
	tempPixel.r = ptrIn[3*i+2];
	tempPixel.b = ptrIn[3*i+1];
	tempPixel.g = ptrIn[3*i+0];
        s = (int)Pixel_stddev(color, &tempPixel); //this function used to keep color data associated with each sigma, so this s got used a lot
        sigmas[s]++;
            //update the average color
        imgAverage_r = (imgAverage_r*(i)+tempPixel.r)/(i+1);
        imgAverage_g = (imgAverage_g*(i)+tempPixel.g)/(i+1);
        imgAverage_b = (imgAverage_b*(i)+tempPixel.b)/(i+1); 
    }
    //update the imgAverage pixel (converting all averages to integers)
    imgAverage.r = (int)imgAverage_r;
    imgAverage.g = (int)imgAverage_g;
    imgAverage.b = (int)imgAverage_b;

    averagestddev= Pixel_stddev(color,&imgAverage); 

    for(i=0; (blobsize < min_blobsize || i < smallest_stddev + (averagestddev-smallest_stddev)/2)  && i<dev_threshold;i++){ //analyze data to determine sigma
        if(sigmas[i] != 0 && smallest_stddev < 0 )
	    smallest_stddev = i;
	blobsize += sigmas[i]; 
    }
    stddev = i; //save the max. std dev

    for(i=in->width*in->height-1;i>=0;i--){ //Update the Output Image
	tempPixel.r = ptrIn[3*i+2];
	tempPixel.b = ptrIn[3*i+1];
	tempPixel.g = ptrIn[3*i+0];
	if((int)Pixel_stddev(color,&tempPixel) < stddev){
            //this pixel is "close" to the target color, mark it white
            ptrOut[3*i+2] = 0xff;	
            ptrOut[3*i+1] = 0xff;
            ptrOut[3*i+0] = 0xff;
	}else{
            //this pixel is not "close" to the target color: mark it black
            ptrOut[3*i+2] = 0x00;	
            ptrOut[3*i+1] = 0x00;
            ptrOut[3*i+0] = 0x00;
	} 
    }
   
    free(sigmas);

    //printf("confidence = %d blobsize = %d\n",averagestddev-smallest_stddev,blobsize);
    //fflush(NULL);
    return blobsize;//averagestddev-smallest_stddev;
}

float Pixel_stddev(RGBPixel* px_1, RGBPixel* px_2) {
    return sqrt(pow((short)px_1->r - px_2->r, 2) +
                pow((short)px_1->g - px_2->g, 2) +
                pow((short)px_1->b - px_2->b, 2));
}

