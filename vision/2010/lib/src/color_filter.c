#include "vision_lib.h"

#include <cv.h>
#include <highgui.h>

IplImage* colorfilter(IplImage* img, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax) {

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

  return color; 
}
