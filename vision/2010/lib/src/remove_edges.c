#include "vision_lib.h"

#include <cv.h>
#include <highgui.h>
//removes highlighted areas from the edge-dectected image 

IplImage* remove_edges(IplImage* img, IplImage* edge, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax) {

  int y,x,i,j; 

  IplImage* modified = cvCreateImage(cvGetSize(edge),8,1);
  cvCopy(edge,modified,0);

  for(y=2; y<img->height-2; y++ ) {
    uchar* ptr = (uchar*) (img->imageData + y * img->widthStep);
    uchar* ptrN = (uchar*) (modified->imageData + y * modified->widthStep);

    for(x=2; x<img->width-2; x++ ) {
      
      //if pixel in range, remove from edge
      if (((ptr[3*x+2]>=rmin && ptr[3*x+2]<=rmax) &&
            (ptr[3*x+1]>=bmin && ptr[3*x+1]<=bmax) &&
            (ptr[3*x+0]>=gmin && ptr[3*x+0]<=gmax))) { 
    for(i=-2;i<=2;i++)
      for(j=-2;j<=2;j++)
            ptrN[x+i+j*modified->widthStep] = 0;
      }
    }
  }
  //now get rid of all pixels that arn't part of a verticle line **testing**
  for(y=1; y<img->height-1; y++ ) {
    uchar* ptr = (uchar*) (edge->imageData + y * edge->widthStep);
    uchar* ptrN = (uchar*) (modified->imageData + y * modified->widthStep);

    for(x=0; x<img->width; x++ ) {
      if(!ptr[x+edge->widthStep] || !ptr[x-edge->widthStep])
    ptrN[x] = 0;
    }
  }  

  //now get rid of all vertically isolated pixels
  for(y=1; y<img->height-1; y++ ) {
    uchar* ptrN = (uchar*) (modified->imageData + y * modified->widthStep);

    for(x=0; x<img->width; x++ ) {
      if(!ptrN[x+modified->widthStep] && !ptrN[x-modified->widthStep])
    ptrN[x] = 0;
    }
  }  

  return modified; 
}
