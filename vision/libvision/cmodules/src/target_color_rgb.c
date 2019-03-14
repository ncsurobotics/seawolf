/**
 * \file
 * Target Color RGB 
 */

//************************************************
//  target_color_rgb.c: 
//
//  Houses find_target_color_rgb() and related functions
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

//#define VISUAL_DEBUG 1

#define RED_WEIGHT 2
#define GREEN_WEIGHT 1
#define BLUE_WEIGHT 1
#define REL_SEPARATION_THRESHOLD .2 //how low the histogram must drop relative to current peak
#define ABS_SEPARATION_THRESHOLD 100 //how absolutely low the histogram must drop in order to consider a blob 'isolated' 
#define STDDEV_THRESHOLD 40 //required stddev of histogram to accept a blob

struct RGBPixel_s {
    unsigned char r;
    unsigned char g;
    unsigned char b;
};

typedef struct RGBPixel_s RGBPixel; 

float Pixel_dist_rgb(RGBPixel* px_1, RGBPixel* px_2);

int min(int a, int b);
 
IplImage* find_target_color_rgb(IplImage* frame, int red, int green, int blue, int min_blobsize, int dev_threshold, double precision_threshold){ //should find the set of colors closest to the target color
    int i,j,s;
    int* radii; //holds the accumulation for all possible distances from target pixel
    int blobsize = 0; //current number of pixels found in color "blob" (not necceserily a single blob)
    int rlimit=0; // stddev; //the computed maximum allowable stddev
    int raverage; //the average stddev from target color
    int smallestr; //the smallest stddev found
    double imgAverage_r=0; //hold average colors for this image as doubles
    double imgAverage_g=0;
    double imgAverage_b=0;
    double variance = 0; //the variance of the histogram
    int sample_size = 0; //the sample used to compute variance
    RGBPixel imgAverage;
    RGBPixel tempPixel;
   
    //Initialize Images
    IplImage* out = cvCreateImage(cvGetSize(frame),8,1);
    IplImage* in = cvCloneImage(frame);

    uchar* ptrIn = (uchar*) in->imageData;
    uchar* ptrOut = (uchar*) out->imageData;
   
    //Compile target color
    RGBPixel color;
    color.r = red;
	color.g = green;
	color.b = blue;

    int maxr = (int) sqrt(pow((short)256*RED_WEIGHT,2)+
                        pow((short)256*GREEN_WEIGHT,2)+
                        pow((short)256*BLUE_WEIGHT,2));
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
        tempPixel.r = ptrIn[3*i+2];
        tempPixel.g = ptrIn[3*i+1];
        tempPixel.b = ptrIn[3*i+0];
        s = (int)Pixel_dist_rgb(&color, &tempPixel); 
        radii[s]++;
        if(radii[s] > peakr) peakr = radii[s]; 
        if(s < smallestr) smallestr = s;

        // Update the average color
        imgAverage_r = (imgAverage_r*(i)+tempPixel.r)/(i+1);
        imgAverage_g = (imgAverage_g*(i)+tempPixel.g)/(i+1);
        imgAverage_b = (imgAverage_b*(i)+tempPixel.b)/(i+1); 
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
    imgAverage.r = (int)imgAverage_r;
    imgAverage.g = (int)imgAverage_g;
    imgAverage.b = (int)imgAverage_b;

    raverage= Pixel_dist_rgb(&color,&imgAverage); 

    int tot_sum = 0;
    int prev_sum = 0;
    int check_dif = 0;
    int check_thresh = 0;
    int rlimit_thresh = 0;
    int rlimit_dif = 0;
    int max_peak = 0;
    int target_sum = 0;

    //first see if a large group is isolated from the rest of the histogram
    //if that failed, use a differential approach to locate the first peak
    for( i=smallestr; i<maxr; i+=3){
        //compute variance / standard deviation
        variance += (radii[i])*(i-raverage)*(i-raverage);
        sample_size += radii[i];

        if (i<dev_threshold && i<raverage){
            //keep up a few basic values
            int cur_sum = radii[i] + radii[i+1] + radii[i+2]; 
            if(cur_sum > max_peak) max_peak = cur_sum;
            tot_sum += cur_sum;

            //test differential threshold(looks for first peak)
            if (cur_sum < prev_sum && tot_sum > min_blobsize && !target_sum ) {
                target_sum = tot_sum + tot_sum * precision_threshold;
            }
            if (target_sum && tot_sum >= target_sum && !check_dif) { 
                rlimit_dif = i;
                check_dif = 1;
            }
            prev_sum = cur_sum; 

            //test valley threshold(looks for first valley)
            int in_valley = 0;
            if( cur_sum < REL_SEPARATION_THRESHOLD*max_peak || cur_sum < ABS_SEPARATION_THRESHOLD){
                in_valley = 1;
            }
            if ( tot_sum > min_blobsize && in_valley && !check_thresh ){
                rlimit_thresh = i;
                check_thresh = 1;
            }

            if( check_dif && check_thresh )
                break;
        }
    }

    //compute standard deviation
    variance /= sample_size;
    int stddev = pow(variance,(double)0.5);

    //verify that stddev is large enough that 
    //  we could be seeing a correctly colored blob
    if(stddev < STDDEV_THRESHOLD){
        rlimit_thresh = 0;
        rlimit_dif = 0;
    }

    if(rlimit_thresh){
        //printf("Using Thresh\n");
        rlimit = rlimit_thresh;
    } else if(rlimit_dif){
        //printf("Using Dif\n");
        rlimit = rlimit_dif;
    } else {
        //printf("Color Not Found\n");
        rlimit = 0;
    }

    #ifdef VISUAL_DEBUG 
        //printf("rlimit = %d, smallestr = %d \n",rlimit, smallestr);
        //Draw a line representing the selected distance cut-off
        CvPoint pt1 = {rlimit,0};
        CvPoint pt2 = {rlimit,299};
        CvScalar cutoffline_color = {254,254,254};
        cvLine(rgram,pt1,pt2,cutoffline_color,1,8,0);
#if 0
        CvPoint pt1 = {raverage - stddev,0};
        CvPoint pt2 = {raverage - stddev,299};
        CvScalar stddevline_color = {254,254,254};
        cvLine(rgram,pt1,pt2,stddevline_color,1,8,0);

        CvPoint pt3 = {raverage,0};
        CvPoint pt4 = {raverage,299};
        CvScalar raverageline_color = {100,100,100};
        cvLine(rgram,pt3,pt4,raverageline_color,1,8,0);

#endif 
        cvNamedWindow("Rgram", CV_WINDOW_AUTOSIZE);
        cvShowImage("Rgram", rgram);
    #endif

    for(i=in->width*in->height-1;i>=0;i--){ //Update the Output Image
        tempPixel.r = ptrIn[3*i+2];
        tempPixel.g = ptrIn[3*i+1];
        tempPixel.b = ptrIn[3*i+0];
        if((int)Pixel_dist_rgb(&color,&tempPixel) < rlimit){
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
float Pixel_dist_rgb(RGBPixel* px_1, RGBPixel* px_2) {
    int red = px_1->r - px_2->r;
    int green = px_1->g - px_2->g;
    int blue = px_1->b - px_2->b;
    return sqrt(pow((short)red * RED_WEIGHT, 2) +
                pow((short)green * GREEN_WEIGHT, 2) +
                pow((short)blue * BLUE_WEIGHT, 2));
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
