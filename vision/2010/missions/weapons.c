#include "seawolf.h"
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "seawolf3.h"

#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#include "mission.h"


void mission_weapons_init(void){

}

GRID grid;


struct mission_output mission_weapons_step(struct mission_output result){
    IplImage* grey;
    IplImage* edge;
    CvSeq* lines;
    
    //grab a frame
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    frame = normalize_image(frame);
    
    //run a hough transform
    grey = cvCreateImage(cvSize(frame->width,frame->height), 8, 1);
    cvCvtColor(frame, grey, CV_BGR2GRAY);
    edge = edge_opencv(grey, 25,40, 3); // This should be much more lenient than normal
    lines = hough(edge, frame, 27, 10, 90,20, 10, 150, 150);
    
    //sort the hough lines into a grid
    find_regions(lines,&grid, frame);
    
    //free resources
    cvReleaseImage(&grey);
    cvReleaseImage(&edge);
    cvRelease((void**) &lines);
    
    printf("We Just Completed the Weapons Run!!");
    return result;   
}
