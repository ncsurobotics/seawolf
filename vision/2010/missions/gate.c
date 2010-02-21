#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#include "mission.h"


// State variables for GATE (static limits scope to file)
static int WHITE_GATE_FLAG =0; // Set to zero to look for black gate
static int close_to_gate =0; // Number of consecutive frames we've seen something we think is a gate
static int gate_width =0; // The width of the last gate we saw 
static int frames_since_seen_gate = 0; // Frames since we've seen the gate
static int seen_gate = 0;
static int left_pole = 0;
static int right_pole = 0;
static int seen_both_poles = 0; // Increments every time we see both poles

void mission_gate_init(IplImage* frame)
{
    close_to_gate = 0;
    gate_width = 0;
    frames_since_seen_gate = 0;
    seen_gate = 0;
    left_pole = 0;
    right_pole = frame->width;
    seen_both_poles = 0;
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
    //TODO: Depth
    //SeaSQL_setTrackerDoDepth(2.0);
    result.depth = 4.0;
    // Find lines, white or black
    if (WHITE_GATE_FLAG) { // LOOK FOR WHITE LINES
        grey = cvCreateImage(cvSize(frame->width,frame->height), 8, 1);
        cvCvtColor(frame, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 60,100, 3); // This should be much more lenient than normal
        edge = remove_edges(frame, edge, 0,0,0,0,0,0); // For now this isn't neccessary, leavin in for debugging
        lines = hough(edge, frame, 27, 2, 90,20, 10, 150, 150);

    } else { // LOOK FOR BLACK LINES
        color.r=0xFF;
        color.g=0xA6;
        color.b=0x00;
        grey = cvCreateImage(cvGetSize(frame), 8, 1);
        ipl_out = cvCreateImage(cvGetSize(frame),8,3);
        num_pixels = FindTargetColor(frame, ipl_out, &color, 80, 256);
        cvCvtColor(ipl_out, grey, CV_BGR2GRAY); 
        edge = edge_opencv(grey, 40, 60, 3);
        edge = remove_edges(frame, edge, 0,0,0,0,0,0); // For now this isn't neccessary, leavin in for debugging
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

        //result.theta = ((pt_gate[0]+pt_gate[1])/2-frame->width/2)/2+frame->width/2; // Head towards the middle of the gate
        result.theta = (pt_gate[0]+pt_gate[1])/2; // - frame->width/2;

    } else if (rho_gate[1] != -999) { // We only see one line
        seen_gate++;
        frames_since_seen_gate = 0;

        // If the line we see is closest to the left pole, turn right, else turn left
        if ( abs((int)pt_gate[1]-left_pole) < abs((int)pt_gate[1]-right_pole) ) {
            // We see the left pole
            printf("I see the left pole!");
            int difference =  pt_gate[1] - left_pole;
            right_pole = right_pole + difference;
            left_pole = pt_gate[1];
            result.theta = frame->width/2 + 15;
        } else {
            // We see the right pole
            printf("I see the right pole!");
            int difference =  pt_gate[1] - right_pole;
            left_pole = left_pole + difference;
            right_pole = pt_gate[1];
            result.theta = frame->width/2 - 15;
        }

    } else { // We don't see anything
        if (++frames_since_seen_gate > 20 && seen_gate > 10) {
            result.mission_done = true;
        }

        result.theta = frame->width/2;
    }

    // Determine rho
    if(close_to_gate > 3)
        result.rho= 15; // Low rho
    else
        result.rho = 15; // High rho

    // Debugs:
    hough_draw_lines(result.frame, lines);
    cvCircle(result.frame, cvPoint(result.theta, frame->height/2), 5, cvScalar(0,0,0,255),1,8,0);

    // Scale output 
    result.theta -= frame->width/2;
    result.theta = (result.theta*MAX_THETA / (frame->width/2))/6;
    result.phi = 0;

    if (WHITE_GATE_FLAG) { // Free white gate resources
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvRelease((void**) &lines);
    } else { // Free black gate resources
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvReleaseImage(&ipl_out);
        cvReleaseMemStorage(&(lines->storage));
    }

    return result;
}
