/* edge_opencv.c
 * This is pretty much a binding function for opencv's edge detect, adding some
 * debug functionality.
 *
 * Debugs specific to this file:
 *   debug_edge
 *   debug_edge_args
 */

#include "vision_lib.h"

#include <stdio.h>
#include <cv.h>
#include <highgui.h>

IplImage* ret;
#ifdef debug_edge_args
    int low_threshold_slider = 50;
    int high_threshold_slider = 150;
#endif

void edge_opencv_init()
{
    #ifdef debug_edge
        cvNamedWindow("Edge", CV_WINDOW_AUTOSIZE);
    #endif
    #ifdef debug_edge_args
        cvCreateTrackbar("Low", "Edge", &low_threshold_slider, 400, NULL);
        cvCreateTrackbar("High", "Edge", &high_threshold_slider, 400, NULL);
    #endif
}

IplImage* edge_opencv(IplImage* frame, int low_threshold, int high_threshold, int aperture)
{
    #ifdef debug_edge_args
        low_threshold = low_threshold_slider;
        high_threshold = high_threshold_slider;
    #endif

    ret = cvCreateImage(cvGetSize(frame), 8, 1);
    #ifdef debug_image_typecheck
        if (frame->nChannels != 1)
        {
          printf("edgeDetect() must take in a single channel image.\nYou probably want to use:\ncvCvtColor(original, modified, CV_BGR2GRAY);\n");
          exit(-1);
        }
    #endif
    cvCanny(frame, ret, low_threshold, high_threshold, aperture);
    #ifdef debug_edge
        cvShowImage("Edge", ret);
    #endif

    for(int i = ret->height * ret->width - 1; i >= ret->height*(ret->width - 10); i--) {
    ret->imageData[i] = 0; //turn bottom of the screen black, b/c sobel was messing up
    }

    return ret;
}

void edge_opencv_free()
{

}
