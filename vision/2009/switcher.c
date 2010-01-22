#include "seawolf.h"
#include "vision.h"
#include "cv.h"
#include "highgui.h"

int main(int argc, char** argv)
{
    // Init the cameras
    if (argc == 4) {
        multicam_set_camera(0,argv[1]);
        multicam_set_camera(1,argv[2]);
        multicam_set_camera(2,argv[3]);
    } else if (argc == 3) {
        multicam_set_camera(0,argv[1]);
        multicam_set_camera(1,argv[2]);
        multicam_set_camera(2,argv[1]);
    } else if (argc == 2) {
        multicam_set_camera(0,argv[1]);
        multicam_set_camera(1,argv[1]);
        multicam_set_camera(2,argv[1]);
    } else {
        multicam_set_camera(0,"0");
        multicam_set_camera(1,"1");
        multicam_set_camera(2,"2");
    }
    IplImage* frame;
    int current_cam = 0;
    cvNamedWindow("Camera", 1);

    while (1)
    {
        //printf("Got frame...\n");
        frame = multicam_get_frame(current_cam);
        cvShowImage("Camera", frame);
        int key = cvWaitKey(500);
        if ((char)key==27) break;
        switch ( (char) key )
        {
        case '1':
            current_cam = 0;
            break;
        case '2':
            current_cam = 1;
            break;
        case '3':
            current_cam = 2;
            break;
        }
    }
    
}
