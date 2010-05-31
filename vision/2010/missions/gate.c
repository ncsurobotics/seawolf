#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include <seawolf3.h>

#include "util.h"
#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#include "mission.h"


// State variables for GATE (static limits scope to file)
static int close_to_gate =0; // Number of consecutive frames we've seen something we think is a gate
static int gate_width =0; // The width of the last gate we saw
static int frames_since_seen_gate = 0; // Frames since we've seen the gate
static int seen_gate = 0;
static int left_pole = 0;
static int right_pole = 0;
static int seen_both_poles = 0; // Increments every time we see both poles

// Manual State Variables
static int WHITE_GATE_FLAG = 1; // Set to zero to look for black gate
static double desired_depth = 2.0; // desired depth

void mission_gate_init(IplImage* frame, double depth)
{
    close_to_gate = 0;
    gate_width = 0;
    frames_since_seen_gate = 0;
    seen_gate = 0;
    left_pole = 0;
    right_pole = frame->width;
    seen_both_poles = 0;
    desired_depth = depth;
}

struct mission_output mission_gate_step(struct mission_output result)
{
    IplImage* grey;
    IplImage* edge;
    IplImage* ipl_out = NULL;
    RGBPixel color = {0xff, 0x00, 0x00};
    CvSeq* lines;
    IplImage* frame = multicam_get_frame(FORWARD_CAM);
    result.frame = frame;
    int num_pixels;

    // Set the depth
    result.depth_control = DEPTH_ABSOLUTE;
    result.depth = desired_depth;
    
    // Set Yaw control 
    result.yaw_control = ROT_MODE_RELATIVE;

    // Find lines, white or black
    if (WHITE_GATE_FLAG) { // LOOK FOR WHITE LINES
        grey = cvCreateImage(cvSize(frame->width,frame->height), 8, 1);
        cvCvtColor(frame, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 60,100, 3); // This should be much more lenient than normal
        edge = remove_edges(frame, edge, 0,0,0,0,0,0); 
        lines = hough(edge, frame, 27, 2, 90,20, 10, 150, 150);

    } else { // LOOK FOR BLACK LINES
        color.r=0xFF;
        color.g=0xA6;
        color.b=0x00;
        grey = cvCreateImage(cvGetSize(frame), 8, 1);
        ipl_out = cvCreateImage(cvGetSize(frame),8,3);
        num_pixels = FindTargetColor(frame, ipl_out, &color, 80, 256,2);
        cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 40, 60, 3);
        edge = remove_edges(frame, edge, 0,0,0,0,0,0); 
        lines = hough(edge, frame, 20, 2, 90,20, 10, 150, 150);

        #ifdef DEBUG_BLACK_GATE
            cvNamedWindow("Black_Gate", CV_WINDOW_AUTOSIZE);
            cvShowImage("Black_Gate", ipl_out);
        #endif

    }

    // Now analyze lines
    int pt_gate[2];
    float rho_gate[2];
    float theta_gate[2];
    for (int i=0; i<2; i++) {
        float* line = (float*) cvGetSeqElem(lines,i);
        rho_gate[i] = line[0];
        theta_gate[i] = line[1];
        pt_gate[i] = cos(theta_gate[i])*rho_gate[i];
    }

    // Figure out where the gate is
    if (rho_gate[0] != -999) { // We see two lines
        seen_gate++;
        seen_both_poles++;
        frames_since_seen_gate = 0;
        gate_width = abs(pt_gate[0]-pt_gate[1]);
        if(abs(frame->width - gate_width) < frame->width / 4)
            close_to_gate++;   // We are close to the gate
        else if(abs(frame->width-gate_width) > frame->width/5)
            close_to_gate = 0; // We arn't close to the gate

        // Assign values to the left and right poles
        left_pole = pt_gate[0]<pt_gate[1]?pt_gate[0]:pt_gate[1];
        right_pole = pt_gate[0]>pt_gate[1]?pt_gate[0]:pt_gate[1];

        //Set the yaw heading to the center of the two poles
        result.yaw = (pt_gate[0]+pt_gate[1])/2; 
        result.yaw -= frame->width/2;

    } else if (rho_gate[1] != -999 && seen_both_poles < 2) { 
        // We only see one line, and don't know where the gate is
        
        seen_gate++;
        frames_since_seen_gate = 0;

        // If the line we see is closest to the left pole, turn right, else turn left
        if ( abs((int)pt_gate[1]-left_pole) < abs((int)pt_gate[1]-right_pole) ) {
            // We see the left pole
            printf("I see the left pole!");
            int difference =  pt_gate[1] - left_pole;
            right_pole = right_pole + difference;
            left_pole = pt_gate[1];
            result.yaw = frame->width/2 + 30;
            result.yaw -= frame->width/2;

        } else {
            // We see the right pole
            printf("I see the right pole!");
            int difference =  pt_gate[1] - right_pole;
            left_pole = left_pole + difference;
            right_pole = pt_gate[1];
            result.yaw = frame->width/2 - 30;
            result.yaw -= frame->width/2;
        }
    } else if (rho_gate[1] != -999 && seen_both_poles >1) {
    
        //We only see one line, but should know where the gate is, so don't do anything
        
    } else { // We don't see anything
    
        // Check to see if we could have passed through the gate
        if (++frames_since_seen_gate > 20 && seen_gate > 10) {
            result.mission_done = true;
        }
    }

    // Determine rho
    if(close_to_gate > 3)
        result.rho= 10; // Low rho
    else
        result.rho = 11; // High rho

    // Debugs:
    #ifdef VISION_SHOW_HEADING
        hough_draw_lines(result.frame, lines);
        cvCircle(result.frame, cvPoint(result.yaw, frame->height/2), 5, cvScalar(0,0,0,255),1,8,0);
    #endif

    // Shift output to zero center of the frame
    result.depth = 0;
    
    // Convert pixels to degrees
    result.yaw = PixToDeg(result.yaw);

    if (WHITE_GATE_FLAG) { // Free white gate resources
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvRelease((void**) &lines);
    } else { // Free black gate resources
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvReleaseImage(&ipl_out);
        //cvRelease((void**) &lines);
        cvReleaseMemStorage(&(lines->storage));
    }

    return result;
}
