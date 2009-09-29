
#include "seawolf.h"
#include "img.h"

#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    //CvCapture* capture = cvCaptureFromCAM(0);
    CvCapture* capture = cvCaptureFromFile("gate.avi");
    IplImage* ipl_frame;
    IplImage* ipl_out = NULL;
    Image* rgb_tmp = NULL;
    Image* indexed_tmp = NULL;
    RGBPixel color = {0xff, 0x40, 0x00};

    cvNamedWindow("src", 0);
    cvNamedWindow("out1", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("out2", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("out3", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("out4", CV_WINDOW_AUTOSIZE);

    cvMoveWindow("out1", 200, 50);
    cvMoveWindow("out2", 400, 50);
    cvMoveWindow("out3", 600, 50);
    cvMoveWindow("out4", 800, 50);
    
    int wait = 0,
        blur = 1,
        colorCount = 16,
        colorThreshold = 16,
        colorFilterCount = 1;
        
    cvCreateTrackbar("Wait", "src", &wait, 100, NULL);
    cvCreateTrackbar("Blur Rounds", "src", &blur, 16, NULL);
    cvCreateTrackbar("Color Count", "src", &colorCount, 256, NULL);
    cvCreateTrackbar("Color Blend", "src", &colorThreshold, 256, NULL);
    cvCreateTrackbar("Color Filter Threshold", "src", &colorFilterCount, 256, NULL);

    /* Initialize temporary images */
    ipl_frame = cvQueryFrame(capture);
    ipl_out = cvCreateImage(cvGetSize(ipl_frame), IPL_DEPTH_8U, 3);
    rgb_tmp = Image_new(RGB, ipl_frame->width, ipl_frame->height);
    indexed_tmp = Image_new(INDEXED, ipl_frame->width, ipl_frame->height);

    while(cvWaitKey(wait) != 'q') {
        ipl_frame = cvQueryFrame(capture);
        cvShowImage("src", ipl_frame);
      
        IplImageToImage(ipl_frame, rgb_tmp);

        Image_normalize(rgb_tmp, rgb_tmp);

        ImageToIplImage(rgb_tmp, ipl_out);
        cvShowImage("out1", ipl_out);

        Image_blur(rgb_tmp, rgb_tmp, 2);
        Image_reduceSpectrum(rgb_tmp, indexed_tmp, colorCount, colorThreshold);

        Image_indexedToRGB(indexed_tmp, rgb_tmp);
        ImageToIplImage(rgb_tmp, ipl_out);
        cvShowImage("out2", ipl_out);

        Image_colorFilter(indexed_tmp, indexed_tmp, &color, colorFilterCount);
        Image_toMonochrome(indexed_tmp, indexed_tmp);

        Image_indexedToRGB(indexed_tmp, rgb_tmp);
        ImageToIplImage(rgb_tmp, ipl_out);
        cvShowImage("out3", ipl_out);

        Image_identifyBlobs(indexed_tmp, indexed_tmp);

        Image_indexedToRGB(indexed_tmp, rgb_tmp);
        ImageToIplImage(rgb_tmp, ipl_out);
        cvShowImage("out4", ipl_out);
    }

    Image_destroy(rgb_tmp);
    Image_destroy(indexed_tmp);
    cvReleaseCapture(&capture);
    cvDestroyAllWindows();
    return 0;
}
