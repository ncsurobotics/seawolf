/* edge.c
 * This is pretty much a binding function for opencv's edge detect, adding some
 * debug functionality.
 *
 */

#include "vision_lib.h"

#include <stdio.h>
#include <cv.h>
#include <highgui.h>

IplImage* edge_opencv(IplImage* frame, int low_threshold, int high_threshold, int aperture)
{

    IplImage* ret = cvCreateImage(cvGetSize(frame), 8, 1);
    #ifdef VISION_LIB_IMAGE_TYPECHECK
        if (frame->nChannels != 1)
        {
          printf("edgeDetect() must take in a single channel image.\nYou probably want to use:\ncvCvtColor(original, modified, CV_BGR2GRAY);\n");
          exit(-1);
        }
    #endif
    cvCanny(frame, ret, low_threshold, high_threshold, aperture);

    for (int i = ret->height * ret->width - 1; i >= ret->height*(ret->width - 10); i--) {
        ret->imageData[i] = 0; // Turn bottom of the screen black, b/c sobel was messing up
    }

    return ret;
}
