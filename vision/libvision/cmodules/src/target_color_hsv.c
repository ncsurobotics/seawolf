/**
 * \file
 * Target Color HSV
 */

//************************************************
//  target_color_hsv.c: 
//
//  Houses find_target_color() and related functions
//        - returns a blacked-out IplImage (black is
//          not the color you are looking for)
//

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

/* DEFINITIONS */ 

#define HUE_WEIGHT 1
#define SAT_WEIGHT 1
#define VAL_WEIGHT 1

struct HSVPixel_s {
    unsigned char h;
    unsigned char s;
    unsigned char v;
};

typedef struct HSVPixel_s HSVPixel; 

float Pixel_stddev_hsv(HSVPixel* px_1, HSVPixel* px_2);

int min(int a, int b);
 
IplImage* find_target_color_hsv(IplImage* frame, int hue, int saturation, int value, int min_blobsize, int dev_threshold, double precision_threshold){ //should find the set of colors closest to the target color
    int i,j,s;
    int* sigmas; //holds the accumulation for all possible standard deviations in the image
    int blobsize = 0; //current number of pixels found in color "blob" (not necceserily a single blob)
    int stddev; //the computed maximum allowable stddev
    int averagestddev; //the average stddev from target color
    int smallest_stddev = -1; //the smallest stddev found
    double imgAverage_h=0; //hold average colors for this image as doubles
    double imgAverage_s=0;
    double imgAverage_v=0;
    HSVPixel imgAverage;
    HSVPixel tempPixel;
   
    //Initialize Images  
    IplImage* out = cvCreateImage(cvGetSize(frame),8,3);
    IplImage* in = cvCreateImage(cvGetSize(frame),8,3);
    cvCvtColor(frame, in, CV_BGR2HSV);

    uchar* ptrIn = (uchar*) in->imageData;
    uchar* ptrOut = (uchar*) out->imageData;
   
    //Compile target color 
    HSVPixel color; 
        color.h = hue;
	color.s = saturation;
	color.v = value;

    sigmas = (int*)calloc(444,sizeof(int)); // Allocate memory for sigma table (max sigma is sqrt(256^2 + 256^2 + 256^2) ) 

    // Initialize tables
    for (i=0;i<444;i++) {
        sigmas[i] = 0;
    }


    for(i=in->width*in->height; i>=0;i--){ // Fill the acumulator tables 
        tempPixel.v = ptrIn[3*i+2];
        tempPixel.h = ptrIn[3*i+0];
        tempPixel.s = ptrIn[3*i+1];
        s = (int)Pixel_stddev_hsv(&color, &tempPixel); //this function used to keep color data associated with each sigma, so this s got used a lot
        sigmas[s]++;
        // Update the average color
        imgAverage_v = (imgAverage_h*(i)+tempPixel.h)/(i+1);
        imgAverage_h = (imgAverage_s*(i)+tempPixel.s)/(i+1);
        imgAverage_s = (imgAverage_v*(i)+tempPixel.v)/(i+1); 
    }
    // Update the imgAverage pixel (converting all averages to integers)
    imgAverage.h = (int)imgAverage_h;
    imgAverage.s = (int)imgAverage_s;
    imgAverage.v = (int)imgAverage_v;

    averagestddev= Pixel_stddev_hsv(&color,&imgAverage); 

    for(i=0; (blobsize < min_blobsize || i < smallest_stddev + (averagestddev-smallest_stddev)/precision_threshold)  && i<dev_threshold;i++){ //analyze data to determine sigma
        if(sigmas[i] != 0 && smallest_stddev < 0 ) {
            smallest_stddev = i;
        }
        blobsize += sigmas[i]; 
    }
    stddev = i; // Save the max. std dev

    for(i=in->width*in->height-1;i>=0;i--){ //Update the Output Image
        tempPixel.h = ptrIn[3*i+2];
        tempPixel.s = ptrIn[3*i+0];
        tempPixel.v = ptrIn[3*i+1];
        if((int)Pixel_stddev_hsv(&color,&tempPixel) < stddev){
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
    cvReleaseImage(&in);
    //printf("confidence = %d blobsize = %d\n",averagestddev-smallest_stddev,blobsize);
    //fflush(NULL);
    return out;
}

/**
 * \brief computes distance between two pixels in rgb space
 * \private
 */
float Pixel_stddev_hsv(HSVPixel* px_1, HSVPixel* px_2) {
    int hue = min(abs(px_1->h - px_2->h), abs(px_1->h + px_2->h - 179) );
    int sat = px_1->s - px_2->s;
    int val = px_1->v - px_2->v;
    return sqrt(pow((short)hue * HUE_WEIGHT, 2) +
                pow((short)sat * SAT_WEIGHT, 2) +
                pow((short)val * VAL_WEIGHT, 2));
}

int min(int a, int b) {
    int min;
    if (a < b ) 
	min = a;
    else
        min = b;
    return min;
}
/** } */
