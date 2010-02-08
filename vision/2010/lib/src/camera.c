/* camera.c
 * Handles camera
 */

#include <time.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

#include "vision_lib.h"
#include <highgui.h>

int frame_number=0;

// Some state variables for multi camera support
static char* cameras[3];
int current_cam_num = -1;
CvCapture* current_capture;

#ifdef VISION_LIB_IMAGE_RECORD
    static int record_dir_num = -1;
#endif

CvCapture* init_camera_from_args(int argc, char** argv) {
    CvCapture* capture;
    // Init Camera
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
        printf("Could not find Camera or AVI\n");
        exit(-1);
    }

    if (!capture)
    {
        printf("Could not find Camera or AVI\n");
        exit(-1);
    }

    return capture;
}

CvCapture* init_camera_from_string(char* str) {
    CvCapture* capture;
    if (strlen(str)==1 && isdigit(str[0]))
    {
        int number = atoi(str);
        printf("Camera Input #: %d\n", number);
        capture = cvCaptureFromCAM(number);
    } else {
        printf("Trying file\n");
        fflush(NULL);
        capture = cvCaptureFromFile(str);
    }
    if (!capture)
    {
        printf("Camera not found!\n");
        fflush(NULL);
        exit(1);
    }
    printf("Camera/file found\n");
    fflush(NULL);

//DO NOT UNCOMMENT THESE!
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 320);
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 240);

    return capture;
}

void multicam_set_camera(int camnumber, char* camstr)
{
    cameras[camnumber] = camstr;
}

IplImage* multicam_get_frame(int camnumber)
{
    #ifdef VISION_LIB_IMAGE_RECORD
        if (record_dir_num == -1)
        {
        char command[20];
            while (1)
            {
                record_dir_num++;
                system("mkdir capture");
                // Go through directories until one doesn't exist
                sprintf(command, "mkdir capture/%d", record_dir_num);
                int mkdir_ret = system(command);
                printf("mkdir_ret = %d\n", mkdir_ret);
                if (mkdir_ret != 256)
                {
                    // Directory created successfully
                    break;
                }
            }
            printf("Directory is: %d\n",record_dir_num);
        }
    #endif
    // See if we have to switch cameras
    if (camnumber != current_cam_num)
    {
        if (current_capture != NULL) {
            // Release current cam if there is one
            cvReleaseCapture(&current_capture);
        }
        current_capture = init_camera_from_string(cameras[camnumber]); 
    }
    current_cam_num = camnumber;
    IplImage* frame = get_frame(current_capture);
    // We have the camera open, output a frame
    return frame;
}

void multicam_reset_camera()
{
    current_cam_num = -1;
}

IplImage* get_frame(CvCapture* capture)
{

    IplImage* frame = cvQueryFrame(capture);

    #ifdef VISION_LIB_IMAGE_RECORD
        // Record frame
        char pathname[50];
        sprintf(pathname, "capture/%d/%05d.jpg", record_dir_num, frame_number);
        cvSaveImage(pathname, frame);
    #endif


    frame_number++;
    return frame;
}
