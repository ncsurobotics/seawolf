#include "vision_lib.h"

#include <cv.h>
#include <highgui.h>

// This transform defines the following debug options:
//  #define debug_color
//  #define debug_color_thresholds

int rmin_slider = 40,rmax_slider = 255; // 75 255
int bmin_slider = 41, bmax_slider = 102; // 0 50
int gmin_slider = 0, gmax_slider = 204; // 0 175

void colorfilter_init()
{ 
  #ifdef debug_color
    cvNamedWindow("Color Filter", CV_WINDOW_AUTOSIZE);
  #endif
  #ifdef debug_color_thresholds
    cvCreateTrackbar("rmin", "Color Filter", &rmin_slider, 255, NULL);
    cvCreateTrackbar("rmax", "Color Filter", &rmax_slider, 255, NULL);
    cvCreateTrackbar("bmin", "Color Filter", &bmin_slider, 255, NULL);
    cvCreateTrackbar("bmax", "Color Filter", &bmax_slider, 255, NULL);
    cvCreateTrackbar("gmin", "Color Filter", &gmin_slider, 255, NULL);
    cvCreateTrackbar("gmax", "Color Filter", &gmax_slider, 255, NULL);
  #endif
}

IplImage* colorfilter(IplImage* img, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax) {
  #ifdef debug_color_thresholds
    rmin = rmin_slider;
    rmax = rmax_slider;
    bmin = bmin_slider;
    bmax = bmax_slider;
    gmin = gmin_slider;
    gmax = gmax_slider;
  #endif

  int y,x; 

  IplImage* color = cvCreateImage(cvGetSize(img),8,3);

  for(y=0; y<img->height; y++ ) {
    uchar* ptr = (uchar*) (img->imageData + y * img->widthStep);
    uchar* ptrN = (uchar*) (color->imageData + y * img->widthStep);

    for(x=0; x<img->width; x++ ) {
      
      //if not in range, black it out 
      if (!((ptr[3*x+2]>=rmin && ptr[3*x+2]<=rmax) &&
            (ptr[3*x+1]>=bmin && ptr[3*x+1]<=bmax) &&
            (ptr[3*x+0]>=gmin && ptr[3*x+0]<=gmax))) {
          ptrN[3*x+0] = ptrN[3*x+1] = ptrN[3*x+2] = 0;
      } else { // Copy value, don't adjust it
        ptrN[3*x+0] = ptr[3*x+0];
        ptrN[3*x+1] = ptr[3*x+1];
        ptrN[3*x+2] = ptr[3*x+2];
      } 
    }
  }
  #ifdef debug_color
    cvShowImage("Color Filter", color);
  #endif

  return color; 
}

void colorfilter_free() {}
