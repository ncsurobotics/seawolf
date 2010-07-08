#include <seawolf.h>

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

#define HEDGE_STATE_DO_HEDGE 0
#define HEDGE_STATE_LOOKING_FOR_ORANGE 1
#define HEDGE_STATE_TURNING_1 2
#define HEDGE_STATE_FORWARD 3
#define HEDGE_STATE_TURNING_2 4

static int hedge_state;

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
static double desired_depth; // desired depth
static RGBPixel PathColor = {0xff, 0x88, 0x00};

// Find path state variables
static int seen_orange_blob;
static Timer* forward_timer;

// How many degrees we turn to the inside when seeing only one pole
#define ONE_POLE_CORRECTION_DEGREES 10

// How large blobs must be
#define MIN_BLOB_SIZE 200

//How well we have to see a blob to think it's the path
#define PATH_FRACTION_THRESHOLD .75

// How many frames we need to see an orangle blob to think we've seen the path
#define SEEN_PATH_THRESHOLD 3

// How close we have to be to consider ourselves turned in the right direction
#define ANGLE_THRESHOLD 5

// Amount we turn to the right after first seeing the path
#define TURN_AMOUNT 90

// Amount of time (seconds) we go forward after turning TURN_AMOUNT degrees
#define FORWARD_TIME 5

void mission_hedge_init(IplImage* frame)
{
    hedge_state = 0;

    // Record reference angle
    Var_set("ReferenceAngle", Var_get("SEA.Yaw"));

    // Do hedge variables
    close_to_gate = 0;
    gate_width = 0;
    frames_since_seen_gate = 0;
    seen_gate = 0;
    left_pole = 0;
    right_pole = frame->width;
    seen_both_poles = 0;
    desired_depth = 1.5;
    //Var_set("ReferenceAngle", Var_get("SEA.Yaw"));

    // Finding path variables
    seen_orange_blob = 0;
    if (forward_timer != NULL) {
        Timer_destroy(forward_timer);
        forward_timer = NULL;
    }
}

struct mission_output mission_hedge_step(struct mission_output result)
{
    IplImage* grey;
    IplImage* edge;
    IplImage* ipl_out = NULL;
    RGBPixel color = {0xff, 0x00, 0x00};
    CvSeq* lines;
    IplImage* frame;
    int num_pixels;
    float heading;

    switch (hedge_state) {

        case HEDGE_STATE_DO_HEDGE:

            // Set the depth
            result.depth_control = DEPTH_ABSOLUTE;
            result.depth = desired_depth;
            
            // Set Yaw control 
            result.yaw_control = ROT_MODE_RELATIVE;

            // Find lines, white or black
            frame = multicam_get_frame(FORWARD_CAM);
            result.frame = frame;
            if (WHITE_GATE_FLAG) { // LOOK FOR WHITE LINES
                grey = cvCreateImage(cvSize(frame->width,frame->height), 8, 1);
                cvCvtColor(frame, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 25,40, 3); // This should be much more lenient than normal
                edge = remove_edges(frame, edge, 1,0,0,0,0,0); 
                lines = hough(edge, frame, 27, 2, 90,20, 10, 150, 150);

            } else { // LOOK FOR BLACK LINES
                color.r=0xFF;
                color.g=0xA6;
                color.b=0x00;
                grey = cvCreateImage(cvGetSize(frame), 8, 1);
                ipl_out = cvCreateImage(cvGetSize(frame),8,3);
                num_pixels = FindTargetColor(frame, ipl_out, &color, 80, 256,2);
                cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 20, 30, 3);
                //edge = remove_edges(frame, edge, 0,0,0,0,0,0); 
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
                printf("I see two lines \n");
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

                printf("before pixToDeg yaw = %f \n",result.yaw);
                // Convert pixels to degrees
                result.yaw = PixToDeg(result.yaw);

                printf("after pixToDeg yaw = %f \n",result.yaw);

            } else if (rho_gate[1] != -999 && seen_both_poles < 2) {
                printf("I see one line and havne't yet seen both poles for 2 frames\n");
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
                    result.yaw =  ONE_POLE_CORRECTION_DEGREES;

                    // Convert pixels to degrees
                    result.yaw = PixToDeg(result.yaw);
                } else {
                    // We see the right pole
                    printf("I see the right pole!");
                    int difference =  pt_gate[1] - right_pole;
                    left_pole = left_pole + difference;
                    right_pole = pt_gate[1];
                    result.yaw = -1 * ONE_POLE_CORRECTION_DEGREES;
                
                    // Convert pixels to degrees
                    result.yaw = PixToDeg(result.yaw);
                }
            } else if (rho_gate[1] != -999 && seen_both_poles >1) {
                printf("I see one line and am ignoring it\n");
            
                //We only see one line, but should know where the gate is, so don't do anything
                
            } else { // We don't see anything
            
                // Check to see if we could have passed through the gate
                if (++frames_since_seen_gate > 20 && seen_gate > 10) {
                    result.mission_done = true;
                }
            }

            // Determine rho
            if(close_to_gate > 3)
                result.rho= 20; // Low rho
            else
                result.rho = 21; // High rho

            // Debugs:
            #ifdef VISION_SHOW_HEADING
                hough_draw_lines(result.frame, lines);
                cvCircle(result.frame, cvPoint(result.yaw, frame->height/2), 5, cvScalar(0,0,0,255),1,8,0);
            #endif

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

            break;

        case HEDGE_STATE_LOOKING_FOR_ORANGE:
            // Go forward until we see orange

            frame = multicam_get_frame(DOWN_CAM);
            result.frame = frame;

            IplImage* ipl_out = cvCreateImage(cvGetSize (frame), 8, 3);
            int num_pixels = FindTargetColor(frame, ipl_out, &PathColor , 1, 310, 1.5);
            BLOB* path_blob;
            int blobs_found = blob(ipl_out, &path_blob, 4, MIN_BLOB_SIZE);

            if((blobs_found == 1 || blobs_found == 2) &&
                (float)path_blob->area / num_pixels > PATH_FRACTION_THRESHOLD ){
                if(++seen_orange_blob > SEEN_PATH_THRESHOLD){
                    hedge_state++;
                }
            } else {
                seen_orange_blob = 0;
            }

            break;

        case HEDGE_STATE_TURNING_1:
            // Turn ~90 degrees to the right
            result.yaw_control = ROT_MODE_ANGULAR;
            result.yaw = Var_get("ReferenceAngle") + TURN_AMOUNT;
            result.yaw = (((int)result.yaw+180) % 360) - 180; // Mod -180 to 180

            // Have we turned far enough?
            heading = Var_get("SEA.Yaw");
            if (fabs(result.yaw - heading) < ANGLE_THRESHOLD ||
                fabs(result.yaw - heading) > 360-ANGLE_THRESHOLD)
            {
                hedge_state++;
            } else {
                break;
            }

        case HEDGE_STATE_FORWARD:
            // Go forward a set amount
            if (forward_timer == NULL) {
                forward_timer = Timer_new();
            } else {
                if (Timer_getTotal(forward_timer) > FORWARD_TIME) {
                    Timer_destroy(forward_timer);
                    forward_timer = NULL;
                    hedge_state++;
                } else {
                    break;
                }
            }
            break;

        case HEDGE_STATE_TURNING_2:
            // Turn 180 degrees, then go forward and switch to path mission
            result.yaw_control = ROT_MODE_ANGULAR;
            result.yaw = Var_get("ReferenceAngle") + TURN_AMOUNT - 180;
            result.yaw = (((int)result.yaw+180) % 360) - 180; // Mod -180 to 180

            // Have we turned far enough?
            heading = Var_get("SEA.Yaw");
            if (fabs(result.yaw - heading) < ANGLE_THRESHOLD ||
                fabs(result.yaw - heading) > 360-ANGLE_THRESHOLD)
            {
                result.mission_done = true;
            }
            break;

        default:
            printf("Warning: hedge_state set to invalid value!\n");

    } // End state machine
    
    return result;
}
