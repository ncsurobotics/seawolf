/**
 * \file
 * Target Color
 */

//************************************************
//  target_color.c: 
//
//  Houses FindTargetColor() and related functions
//        - returns a blacked-out IplImage (black is
//          not the color you are looking for)
//

#include "vision_lib.h"
#include <stdio.h>
#include <cv.h>
#include <highgui.h>  

/** 
 * \ingroup colortools
 * \{
 */
 
 /** 
 * \brief Searches for pixels in an image that most closely match target color.
 *  
 * This function takes in an IplImage and a target color.  It searches the
 * image for the pixels which most closely match the target color.  All other
 * pixels are set to black.  Location of pixels to eachother is ignored.  The
 * number of pixels found (not blacked out) is returned.  The filtered image is
 * passed as an argument.  
 *
 * Be Wary - the trickiest facet of this function is determining when the
 * target color is not in fact present in the image.  For example, if the
 * target is green, and the algorithm is passed an image of a grey table, it
 * will select the greenest part of the grey image, even if it does not appear
 * to be green at all.  The argument to adjust for this problem is
 * dev_threshold. 
 *
 * \param in The origional image to be filtered 
 * \param out The IplImage the filtered output will be assigned to.
 * \param color and RGBPixel of the target color
 * \param min_blobsize an integer of the smallest number of pixels the function
 *        is allowed to return (intended to keep from returning noise) NOTE:
 *        the term "blob" in the title does not have anything to do with it's
 *        use in the rest of the library.
 * \param dev_threshold Determines how far removed the accepted pixels may be
 *        from the target color in RGB space.
 * \param precision_threshold Influences how close to eachother in color the
 *        accepted pixels must be, but not neccesarily how close they are to
 *        the target color
 */
 
int FindTargetColor(IplImage* in, IplImage* out, RGBPixel* color, int min_blobsize, int dev_threshold, double precision_threshold){ //should find the set of colors closest to the target color
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

    sigmas = (int*)calloc(444,sizeof(int)); // Allocate memory for sigma table (max sigma is sqrt(256^2 + 256^2 + 256^2) ) 

    // Initialize tables
    for (i=0;i<444;i++) {
        sigmas[i] = 0;
    }


    for(i=in->width*in->height; i>=0;i--){ // Fill the acumulator tables 
        tempPixel.r = ptrIn[3*i+2];
        tempPixel.b = ptrIn[3*i+0];
        tempPixel.g = ptrIn[3*i+1];
        s = (int)Pixel_stddev(color, &tempPixel); //this function used to keep color data associated with each sigma, so this s got used a lot
        sigmas[s]++;
        // Update the average color
        imgAverage_r = (imgAverage_r*(i)+tempPixel.r)/(i+1);
        imgAverage_g = (imgAverage_g*(i)+tempPixel.g)/(i+1);
        imgAverage_b = (imgAverage_b*(i)+tempPixel.b)/(i+1); 
    }
    // Update the imgAverage pixel (converting all averages to integers)
    imgAverage.r = (int)imgAverage_r;
    imgAverage.g = (int)imgAverage_g;
    imgAverage.b = (int)imgAverage_b;

    averagestddev= Pixel_stddev(color,&imgAverage); 

    for(i=0; (blobsize < min_blobsize || i < smallest_stddev + (averagestddev-smallest_stddev)/precision_threshold)  && i<dev_threshold;i++){ //analyze data to determine sigma
        if(sigmas[i] != 0 && smallest_stddev < 0 ) {
            smallest_stddev = i;
        }
        blobsize += sigmas[i]; 
    }
    stddev = i; // Save the max. std dev

    for(i=in->width*in->height-1;i>=0;i--){ //Update the Output Image
        tempPixel.r = ptrIn[3*i+2];
        tempPixel.b = ptrIn[3*i+0];
        tempPixel.g = ptrIn[3*i+1];
        if((int)Pixel_stddev(color,&tempPixel) < stddev){
            // This pixel is "close" to the target color, mark it white
            ptrOut[3*i+2] = 0xff;   
            ptrOut[3*i+1] = 0xff;
            ptrOut[3*i+0] = 0xff;
        } else {
            // This pixel is not "close" to the target color: mark it black
            ptrOut[3*i+2] = 0x00;   
            ptrOut[3*i+1] = 0x00;
            ptrOut[3*i+0] = 0x00;
        } 
    }

    free(sigmas);

    //printf("confidence = %d blobsize = %d\n",averagestddev-smallest_stddev,blobsize);
    //fflush(NULL);
    return blobsize; //averagestddev-smallest_stddev;
}

/**
 * \brief computes distance between two pixels in rgb space
 * \private
 */
float Pixel_stddev(RGBPixel* px_1, RGBPixel* px_2) {
    return sqrt(pow((short)px_1->r - px_2->r, 2) +
                pow((short)px_1->g - px_2->g, 2) +
                pow((short)px_1->b - px_2->b, 2));
}
/** } */
