#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include <math.h>


#define HOLE_SIZE .75 //small the number, smaller the hole

// Prototypes

void detect_letters(IplImage* binary);

// Definitions

struct Point_s {
    int x;
    int y;
};

typedef struct Point_s Point;  

void detect_letters(IplImage* binary){
    
    Point* points; //an array of the found pixel points 
    int* xsums;   //an array of the sums of pixels at each x coordinate
    int* ysums;   //an array of the sums of pixels at each y coordinate
    int* angdensity; //an array to hold pixel density at various angles
    int pixelcount = 0; //the total number of found pixels
    uchar* data = binary->imageData;

    //allocate memory for arrays 
    points = (Point*)calloc(binary->width * binary->height, sizeof(Point)); 
    xsums = (int*)calloc(binary->width, sizeof(int));
    ysums = (int*)calloc(binary->height, sizeof(int));
    angdensity = (int*)calloc(360, sizeof(int));

    //create a debug image
    IplImage* debug;
    debug = cvCloneImage(binary);
 
    //initialize arrays 
    int i;
    for( i = binary->width * binary->height - 1; i>=0; i--){
        if( i < binary->width)
            xsums[i] = 0;
        if( i < binary->height)  
            ysums[i] = 0;
        points[i].x = 0;
        points[i].y = 0;
    }
    for ( i=0; i<360; i++ ){
        angdensity[i] = 0; 
    }

    //walk through the image, populating a list of found pixels 
    int x,y;
    for(x = binary->width - 1; x>=0; x--){
        for(y = binary->height -1; y>=0; y--){

            //make sure this is a found pixel
            int pos = 3 * ( binary->width * y + x );
            if( data[pos] != 0xff || data[pos+1] != 0xff || data[pos+2] != 0xff)
            continue;

            //add this pixel to the list of found pixels
            points[pixelcount].x = x;
            points[pixelcount].y = y;

            //update the pixel sums 
            pixelcount++;
            xsums[x]++;
            ysums[y]++;
        }
    }

    //collect distribution data 
    int upxquart = -1;
    int lowxquart = -1;
    int upyquart = -1;
    int lowyquart = -1;
    int xmid = -1;
    int ymid = -1;

    int tempsum = 0;
    for ( x = binary->width - 1; x>=0; x--){
        tempsum += xsums[x];
        if (upxquart == -1 && tempsum >= pixelcount * 1/4)
            upxquart = x;
        if (xmid == -1 && tempsum >= pixelcount / 2)
            xmid = x;
        if (lowxquart == -1 && tempsum >= pixelcount * 3 / 4){
            lowxquart = x;
            break;
        }
    }

    tempsum = 0;
    for ( y = binary->height - 1; y>=0; y--){
        tempsum += ysums[y];
        if (upyquart == -1 && tempsum >= pixelcount * 1/4)
            upyquart = y;
        if (ymid == -1 && tempsum >= pixelcount / 2)
            ymid = y;
        if (lowyquart == -1 && tempsum >= pixelcount * 3/ 4){
            lowyquart = y;
            break;
        }
    }

    //use quartile data to compute an average radius
    int r1 = upxquart - xmid;
    int r2 = xmid - lowxquart;
    int r3 = upyquart - ymid;
    int r4 = ymid - lowyquart;
    int avg_radius = (r1 + r2 + r3 + r4)/4;

    //Test to make sure the radii are all about equal
    printf("---------------------------------------------------\n");
    printf("Radii = %d, %d, %d, %d, %d \n",r1,r2,r3,r4,avg_radius);
    printf("xmid = %d, ymid = %d \n",xmid,ymid);
    printf("---------------------------------------------------\n");

    //do statistical analysis on pixels
    int smallrcount = 0;
    int maxangdensity = 0;
    for ( i = pixelcount - 1; i >= 0; i--){
        x = points[i].x - xmid;
        y = points[i].y - ymid;

        //check that not too many pixels are in the center of the blob
        int r = (int)sqrt((double)(x*x + y*y));

        if(r < avg_radius * HOLE_SIZE ) {
            
            //mark that we found a new small radius point
            smallrcount++;

            //show on the debug the location of this point
            
            debug->imageData[points[i].y*debug->width*3 + points[i].x*3 + 0] = 0;
            //debug->imageData[points[i].y*debug->width*3 + points[i].x*3 + 1] = 254;
            debug->imageData[points[i].y*debug->width*3 + points[i].x*3 + 2] = 0;
        }

        //gather the angular distribution of the image
        if( x !=0 && y != 0 ){
            int theta = (int)(atan((double) y / x ) * 360 / 3.14) + 180;
            angdensity[theta]++;  
            if(angdensity[theta] > maxangdensity){
                maxangdensity++;
            }
        }      
    } 
    printf("pixel count = %d, small r count = %d, maxangdensity = %d\n",pixelcount, smallrcount, maxangdensity);

    /* DEBUG CODE */
        //make a histogram for the angular density
        CvSize histsize = {360,180};
        IplImage* thetagram = cvCreateImage(histsize, 8, 1); 
        uchar* histdata = thetagram->imageData; 

        for(i=0; i<360; i++){
            int j;
            for(j=0;j<180; j++){
                if(maxangdensity != 0 && j<angdensity[i] * 180 / maxangdensity)
                    histdata[j*360 + i] = 150;
                else
                    histdata[j*360 + i] = 0;
            }
        }

        cvNamedWindow("Thetagram", CV_WINDOW_AUTOSIZE);
        cvShowImage("Thetagram", thetagram);
        cvNamedWindow("Debug", CV_WINDOW_AUTOSIZE);
        cvShowImage("Debug", debug);
    /* END DEBUG */
  
    //free memory
    cvReleaseImage(&thetagram);
    cvReleaseImage(&debug);
    free(points);
    free(xsums);
    free(ysums);
    free(angdensity);
}


