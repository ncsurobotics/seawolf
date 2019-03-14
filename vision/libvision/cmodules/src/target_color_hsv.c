/**
 * \file
 * Target Color HSV
 */

//************************************************
//  target_color_hsv.c: 
//
//  Houses find_target_color_hsv() and related functions
//        - returns a blacked-out IplImage (black is
//          not the color you are looking for)
//

#include <stdio.h>
#include <cv.h>
#include <highgui.h>  
#include <math.h>

/** 
 * \ingroup colortools
 * \{
 */
 
 /** 
 * \brief Searches for pixels in an image that most closely match target color.
 *  
 * This function takes in an IplImage and a target color.  It searches the
 * image for the pixels which most closely match the target color.  All other
 * pixels are set to black.  Location of pixels to eachother is ignored. 
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

#define VISUAL_DEBUG 1

#define HUE_WEIGHT 2
#define SAT_WEIGHT 1
#define VAL_WEIGHT 1

struct HSVPixel_s {
    unsigned char h;
    unsigned char s;
    unsigned char v;
};

typedef struct HSVPixel_s HSVPixel; 

float Pixel_dist_hsv(HSVPixel* px_1, HSVPixel* px_2);

int min(int a, int b);
 
IplImage* find_target_color_hsv(IplImage* frame, int hue, int saturation, int value, int min_blobsize, int dev_threshold, double precision_threshold){ //should find the set of colors closest to the target color
    int i,j,s;
    int* radii; //holds the accumulation for all possible distances from target pixel
    int blobsize = 0; //current number of pixels found in color "blob" (not necceserily a single blob)
    int rlimit=0; // stddev; //the computed maximum allowable stddev
    int raverage; //the average stddev from target color
    int smallestr; //the smallest stddev found
    double imgAverage_h=0; //hold average colors for this image as doubles
    double imgAverage_s=0;
    double imgAverage_v=0;
    HSVPixel imgAverage;
    HSVPixel tempPixel;
   
    //Initialize Images  
    IplImage* out = cvCreateImage(cvGetSize(frame),8,1);
    IplImage* in = cvCreateImage(cvGetSize(frame),8,3);
    cvCvtColor(frame, in, CV_BGR2HSV);

    uchar* ptrIn = (uchar*) in->imageData;
    uchar* ptrOut = (uchar*) out->imageData;
   
    //Compile target color 
    HSVPixel color; 
    color.h = hue;
	color.s = saturation;
	color.v = value;

    int maxr = (int) sqrt(pow((short)256*HUE_WEIGHT,2)+
                        pow((short)256*SAT_WEIGHT,2)+
                        pow((short)256*VAL_WEIGHT,2));
    // It's easiest if maxr is always even
    if((double) maxr/2 != maxr/2) maxr++;

    radii = (int*)calloc(maxr,sizeof(int));

    // Initialize tables
    for (i=0;i<maxr;i++) {
        radii[i] = 0;
    }


    //Fill the accumulator table / histogram
    smallestr = maxr;
    int peakr = 0;
    for(i=in->width*in->height; i>=0;i--){  
        tempPixel.v = ptrIn[3*i+2];
        tempPixel.h = ptrIn[3*i+0];
        tempPixel.s = ptrIn[3*i+1];
        s = (int)Pixel_dist_hsv(&color, &tempPixel); 
        radii[s]++;
        if(radii[s] > peakr) peakr = radii[s]; 
        if(s < smallestr) smallestr = s;

        // Update the average color
        imgAverage_h = (imgAverage_h*(i)+tempPixel.h)/(i+1);
        imgAverage_s = (imgAverage_s*(i)+tempPixel.s)/(i+1);
        imgAverage_v = (imgAverage_v*(i)+tempPixel.v)/(i+1); 
    }

    #ifdef VISUAL_DEBUG
        CvSize histsize = {maxr,300};
        IplImage* rgram = cvCreateImage(histsize, 8, 1);
        uchar* histdata = rgram->imageData;

        for(i=0; i<maxr; i++){
            int j;
            for(j=0; j<300; j++){
                if(peakr !=0 && j<radii[i]*300/peakr)
                    histdata[j*(maxr) + i] = 150 ; 
                else
                    histdata[j*(maxr) + i] = 0; 
            }
        }
    #endif

    // Update the imgAverage pixel (converting all averages to integers)
    imgAverage.h = (int)imgAverage_h;
    imgAverage.s = (int)imgAverage_s;
    imgAverage.v = (int)imgAverage_v;

    raverage= Pixel_dist_hsv(&color,&imgAverage); 

    int tot_sum = 0;
    int prev_sum = 0;
    int check1 = 0;
    rlimit = 0;
    //use a differential approach to locate the best place to draw the line
    for( i=smallestr; i<maxr && i<dev_threshold; i+=3){
        int cur_sum = radii[i] + radii[i+1] + radii[i+2]; 
        tot_sum += cur_sum;
        if (cur_sum < prev_sum && tot_sum > min_blobsize ) {
            rlimit = i + (i - smallestr) * precision_threshold;
            break;
        }
        prev_sum = cur_sum; 
    }

    #ifdef VISUAL_DEBUG 
        //Draw a line representing the selected distance cut-off
        CvPoint pt1 = {rlimit,0};
        CvPoint pt2 = {rlimit,299};
        CvScalar cutoffline_color = {254,254,254};
        cvLine(rgram,pt1,pt2,cutoffline_color,1,8,0);

        cvNamedWindow("Rgram", CV_WINDOW_AUTOSIZE);
        cvShowImage("Rgram", rgram);
    #endif

    for(i=in->width*in->height-1;i>=0;i--){ //Update the Output Image
        tempPixel.v = ptrIn[3*i+2];
        tempPixel.h = ptrIn[3*i+0];
        tempPixel.s = ptrIn[3*i+1];
        if((int)Pixel_dist_hsv(&color,&tempPixel) < rlimit){
            // This pixel is "close" to the target color, mark it white
            ptrOut[i] = 0xff;
        } else {
            // This pixel is not "close" to the target color: mark it black
            ptrOut[i] = 0x00;
        } 
    }

    free(radii);
    cvReleaseImage(&in);
    #ifdef VISUAL_DEBUG
        cvReleaseImage(&rgram);
    #endif

    return out;
}

/**
 * \brief computes distance between two pixels in rgb space
 * \private
 */
float Pixel_dist_hsv(HSVPixel* px_1, HSVPixel* px_2) {
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
