#include "seawolf.h"
#include <stdio.h>
#include <stdlib.h>
#include "vision.h>"
#include <cv.h>
#include <highgui.h>
#include <math.h>




//state variables for GATE
int WHITE_GATE_FLAG =1; //set to zero to look for black gate
int close_to_gate =0; //number of consecutive frames we've seen something we think is a gate
int gate_width =0; //the width of the last gate we saw 
int frames_since_seen_gate = 0; // Frames since we've seen the gate
int seen_gate = 0;
int left_pole = 0;
int right_pole = frame_width;
int seen_both_poles = 0; //increments every time we see both poles

void mission_gate_init()
{
    close_to_gate = 0;
    gate_width = 0;
    frames_since_seen_gate = 0;
    seen_gate = 0;
    left_pole = 0;
    right_pole = frame_width;
    seen_both_poles = 0;
}

void mission_gate_step()
{
    frame = multicam_get_frame(FORWARD_CAM);
    // Set the depth
    SeaSQL_setTrackerDoDepth(0.0);
    SeaSQL_setDepthHeading(4.0);
    if(WHITE_GATE_FLAG){ //LOOK FOR WHITE LINES
        grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);
        cvCvtColor(frame, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 60,100, 3); //this should be much more lenient than normal
        edge = remove_edges(frame, edge, 0,0,0,0,0,0); //for now this isn't neccessary, leavin in for debugging
        lines = hough_opencv(edge, frame, 27, 2, 90,20, 10, 150, 150);
    }else{//LOOK FOR BLACK LINES
        color.r=0x00;
        color.g=0x00;
        color.b=0x00;
        grey = cvCreateImage(cvGetSize(frame), 8, 1);
        IplImageToImage(frame, rgb_tmp);
        num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80, 256);
        Image_indexedToRGB(indexed_tmp, rgb_tmp); 
        ImageToIplImage(rgb_tmp, ipl_out);
        #ifdef debug_tuna
            cvShowImage("out2", ipl_out);
        #endif
        cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 40, 60, 3);
        lines = hough_opencv(edge, frame, 24, 2, 90,20, 10, 150, 150);
    }

    //now analyze lines
    int pt_gate[2];
    float rho_gate[2];
    float theta_gate[2];
    for(i=0;i<2;i++){
        float* line = (float*)cvGetSeqElem(lines,i);
        rho_gate[i] = line[0];
        theta_gate[i] = line[1];
        pt_gate[i] = cos(theta_gate[i])*rho_gate[i];
    }

    //figure out where the gate is
    if(rho_gate[0] != -999){ //we see two lines
        seen_gate++;
        seen_both_poles++;
        frames_since_seen_gate = 0;
        gate_width = abs(pt_gate[0]-pt_gate[1]);
        if(abs(frame_width - gate_width) < frame_width / 4)
            close_to_gate++;   //we are close to the gate
        else if(abs(frame_width-gate_width) > frame_width/5)
            close_to_gate = 0; //we arn't close to the gate 

        //assign values to the left and right poles
        left_pole = pt_gate[0]<pt_gate[1]?pt_gate[0]:pt_gate[1];
        right_pole = pt_gate[0]>pt_gate[1]?pt_gate[0]:pt_gate[1];

        theta = ((pt_gate[0]+pt_gate[1])/2-frame_width/2)/2+frame_width/2; //head towards the middle of the gate
    }else if(rho_gate[1] != -999){//we only see one line
        seen_gate++;
        frames_since_seen_gate = 0;

        //if the line we see is closest to the left pole, turn right, else turn left
        if(abs((int)pt_gate[1]-left_pole) < abs((int)pt_gate[1]-right_pole)){
            //we see the left pole
            printf("I see the left pole!");
            int difference =  pt_gate[1] - left_pole;
            right_pole = right_pole + difference;
            left_pole = pt_gate[1];
            theta = frame_width/2 + 15;
        }else{
            //we see the right pole
            printf("I see the right pole!");
            int difference =  pt_gate[1] - right_pole;
            left_pole = left_pole + difference;
            right_pole = pt_gate[1];
            theta = frame_width/2 - 15;
        }

    }else{ //we don't see anything
        if(++frames_since_seen_gate > 20 && seen_gate > 10){
            mission = ALLIGN_PATH;
        }

    theta = frame_width/2;
    }

    //determine rho
    if(close_to_gate > 3)
        rho= 15; //low rho
    else
        rho = 15; //high rho

    //scale output 
    theta -= frame_width/2;
    theta = (theta*MAX_THETA / (frame_width/2))/6;
    phi = 0;

    //free resources
    cvReleaseImage(&grey);
    cvReleaseImage(&edge);
    cvRelease((void**) &lines);

    if(WHITE_GATE_FLAG){//free white gate resources
        colorfilter_free();
        edge_opencv_free();
        hough_opencv_free();
        remove_edges_free();
    }else{//free black gate resources
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvRelease((void**) &lines);
        colorfilter_free();
        edge_opencv_free();
        hough_opencv_free();
    }
}
