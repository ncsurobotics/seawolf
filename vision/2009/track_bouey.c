#include "seawolf.h"
#include <cv.h>
#include <stdio.h>
#include <stdlib.h>
#include <highgui.h>

#include "vision.h"

#define debug_show_source

int main(int argc, char** argv) {

    // Init seawolf library
    Seawolf_loadConfig("../../conf/seawolf.conf");
    Seawolf_init("Bouey Tracking");

    // Init variables
    IplImage* frame;
    IplImage* colorfiltered;
    CvPoint* heading;
    CvCapture* capture = 0;
    int key;

    // Transform Inits
    colorfilter_init();
    blob_init();

    #ifdef debug_show_source
        cvNamedWindow("Heading", CV_WINDOW_AUTOSIZE);
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
        capture = cvCaptureFromAVI( argv[1] );
        if (!capture) {
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

    int framenum;
    for (framenum=0; 1; framenum++)
    {
        
        // Get Frame
        frame = cvQueryFrame(capture);
        char framenumchar[10];
        sprintf(framenumchar, "%d", framenum);
        //itoa(framenum, framenumchar, 10);
        strcat(framenumchar,".jpg");
        cvSaveImage(framenumchar, frame);

        // Heading Calculation
        colorfiltered = colorfilter(frame, 40, 255, 0, 120, 0, 175);
        heading = blob(colorfiltered, 2, 250);
        printf("Heading: %d %d\n",heading->x, heading->y);
        fflush(NULL);

        // Update Heading
        SeaSQL_setSetPointVision_Phi(0.0);
        SeaSQL_setSetPointVision_Theta(1.0);
        SeaSQL_setSetPointVision_Rho(1.0);
        Notify_send("UPDATED", "SetPointVision");

        // Transform Frees
        colorfilter_free();
        blob_free();

        #ifdef debug_show_source
            cvCircle(frame, cvPoint(heading->x,heading->y), 5, cvScalar(0,255,0, 0), 1, 8, 0);
            cvShowImage("Heading",frame);
        #endif

        // Free variables
        free(heading);
        cvReleaseImage(&colorfiltered);

        key = cvWaitKey(10);
        if ((char) key == 27) {break;};

    }

    Seawolf_close();
    return 0;
}
