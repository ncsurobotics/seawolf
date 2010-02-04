#include "vision_lib.h"

#include <cv.h>
#include <highgui.h>
//removes highlighted areas from the edge-dectected image 

int rmin2_slider = 26,rmax2_slider = 255; // 75 255
int bmin2_slider = 117, bmax2_slider = 255; // 0 50
int gmin2_slider = 103, gmax2_slider = 255; // 0 175

void remove_edges_init()
{ 
  #ifdef debug_remove_edges
    cvNamedWindow("Remove Edges", CV_WINDOW_AUTOSIZE);
  #endif
  #ifdef debug_remove_edges_thresholds
    cvCreateTrackbar("rmin", "Remove Edges", &rmin2_slider, 255, NULL);
    cvCreateTrackbar("rmax", "Remove Edges", &rmax2_slider, 255, NULL);
    cvCreateTrackbar("bmin", "Remove Edges", &bmin2_slider, 255, NULL);
    cvCreateTrackbar("bmax", "Remove Edges", &bmax2_slider, 255, NULL);
    cvCreateTrackbar("gmin", "Remove Edges", &gmin2_slider, 255, NULL);
    cvCreateTrackbar("gmax", "Remove Edges", &gmax2_slider, 255, NULL);
  #endif
}

IplImage* remove_edges(IplImage* img, IplImage* edge, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax) {

  #ifdef debug_remove_edges_thresholds
    rmin = rmin2_slider;
    rmax = rmax2_slider;
    bmin = bmin2_slider;
    bmax = bmax2_slider;
    gmin = gmin2_slider;
    gmax = gmax2_slider;
  #endif

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
  #ifdef debug_remove_edges   
    cvShowImage("Remove Edges", modified);
  #endif

  return modified; 
}

void remove_edges_free() {}
