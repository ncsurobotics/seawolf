#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <cv.h>
#include <highgui.h>
#include <time.h>

#include "vision.h"

// Debugs specific to this file:
//#define debug_show_source
//#define custom_ffmpeg // Not implemented
#define delay 10 // Delay between frames in ms. 0 for keystroke wait.  -1 for speedtests
                 // You probably want about 10ms delay if you have any opencv
                 // windows, this the wait call is where gtk work is done.
#define num_frames -1 // -1 for to wait for escape key

int main(int argc, char** argv)
{
    
    //// Init variables ////
    int key;
    int frames_calculated;
    IplImage* frame;
    IplImage* edge;
    IplImage* grey;
    IplImage* colorfiltered;
    CvPoint* heading;
    CvSeq* lines;
    CvCapture* capture = 0;

    #ifdef debug_controls
        cvNamedWindow("Controls", CV_WINDOW_AUTOSIZE);
    #endif

    //// Init Capture ////
    if( argc == 1 || (argc == 2 && strlen(argv[1]) == 1 && isdigit(argv[1][0])))
    {
        printf("Looking for Camera...");
        capture = cvCaptureFromCAM( argc == 2 ? argv[1][0] - '0' : 0 );
    }
    else if( argc == 2 )
    {
        printf("Reading AVI...");
        capture = cvCaptureFromFile( argv[1] );
        if (!capture) {
            printf("%s\n",cvErrorStr(cvGetErrStatus()));
            printf("OpenCV AVI read failed, trying custom...");
            //Code Here
        }
    } else {
        printf("USAGE: ./test_transforms [avi file | camera number]\n");
        printf("Defaults to camera 0\n");
        return -1;
    }

    if (capture)
    {
        printf("Success!\n");
    } else {
        printf("FAILED\n");
        return -1;
    }

    //// Init Transforms ////
    hough_opencv_init();
    colorfilter_init();
    blob_init();
    edge_opencv_init();

    //// Init Windows ////
    #ifdef debug_show_source
        cvNamedWindow("Source", CV_WINDOW_AUTOSIZE);
    #endif
    #ifdef debug_display_controls //TODO
        cvNamedWindow("Controls", CV_WINDOW_AUTOSIZE);
    #endif

    clock_t start_time = clock();   

    for (frames_calculated=0;frames_calculated!=num_frames;frames_calculated++)
    {

        //// Get Frame ////
        #ifdef custom_ffmpeg
            // Custom FFMPEG Implementation
            printf("Custom FFMPEG is unimplemented.  \n");
            return -1;
        #else
            //printf("Capturing...");
            //fflush(NULL);
            frame = cvQueryFrame(capture);
            //printf("Done\n");
            //fflush(NULL);
        #endif

        //// Do Transforms ////
        grey = cvCreateImage(cvGetSize(frame), 8, 1);
        colorfiltered = colorfilter(frame, 75, 255, 0, 50, 0, 175);
        cvCvtColor((CvArr*) colorfiltered, (CvArr*) grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 50, 150, 3);
        lines = hough_opencv(edge, frame, 100, 2, 8.0, 10, 60, 60);
        heading = blob(colorfiltered, 1, 250);

        #ifdef debug_show_source
            cvShowImage("Source",frame);
        #endif

        //// Handle Keys ////
        #if delay != -1
            key = cvWaitKey(delay);
            if ( (char) key == 27) // Esc to exit
            {
                break;
            }
            switch( (char) key)
            {
                // Keyboard Commands
            }
        #endif

        //// Release Variables ////
        //cvReleaseImage(&frame);
        free(heading);
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvReleaseImage(&colorfiltered);
        cvRelease((void**) &lines);

        //// Call Transform Free's ////
        edge_opencv_free();
        colorfilter_free();
        blob_free();
        hough_opencv_free();

    }

    // Time Statistics Calculations
    float time_elapsed = ((double)clock() - start_time) / CLOCKS_PER_SEC;
    float frames_per_second = frames_calculated*CLOCKS_PER_SEC/((double)clock() - start_time);
    float seconds_per_frame = 1/frames_per_second;
    printf("Frames Calculated: %d\n", frames_calculated);
    printf("Time elapsed: %f\n", time_elapsed);
    printf("Frame Rate: %f frames/second\n", frames_per_second);
    printf("            %f seconds/frame\n", seconds_per_frame);

    //// Release Variables ////
    #ifdef debug_show_source
        cvDestroyWindow("Source");
    #endif
    cvReleaseCapture(&capture);

}
