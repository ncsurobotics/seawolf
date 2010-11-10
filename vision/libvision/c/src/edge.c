/**
 * \file
 * This is pretty much a binding function for opencv's edge detect, adding some
 * debug functionality.
 *
 */

#include "vision_lib.h"

#include <stdio.h>
#include <cv.h>
#include <highgui.h>

/**
 * \ingroup edgetools
 * \{
 */

/**
 * \brief a binding function for opencv's edge detect.
 * Acts on a grey-scale IplImage, returns a black image, with edge pixels highlighted white.  This
 * results in an image with white
 * outlines 1 pixel in width set on a black background.  
 *
 * Typically used to generate the input for a hough transform.  May also be cleaned up for certain 
 * tasks with the function remove_edges() 
 *
 * example use
 * \code
 * grey = cvCreateImage(cvSize(frame->width,frame->height), 8, 1);
 * cvCvtColor(frame, grey, CV_BGR2GRAY);
 * edge = edge_opencv(grey, 60,100, 3);
 * \endcode
 *      
 * \param frame the input image to be analyzed
 * \param low_threshold the neccessary differential across a pixel adjacent next to a confirmed edge for 
 * that pixel to be considered an edge
 * \param high_threshold the neccessary differential across a lone pixel for that pixel to be considered
 * an edge. 
 * \param aperture usually set to 3
 */
 
IplImage* edge_opencv(IplImage* frame, int low_threshold, int high_threshold, int aperture)
{

    IplImage* ret = cvCreateImage(cvGetSize(frame), 8, 1);
    if (frame->nChannels != 1)
    {
      printf("edgeDetect() must take in a single channel image.\nYou probably want to use:\ncvCvtColor(original, modified, CV_BGR2GRAY);\n");
      exit(-1);
    }
    cvCanny(frame, ret, low_threshold, high_threshold, aperture);

    for (int i = ret->height * ret->width - 1; i >= ret->height*(ret->width - 10); i--) {
        ret->imageData[i] = 0; // Turn bottom of the screen black, b/c sobel was messing up
    }

    return ret;
}
/** } */
