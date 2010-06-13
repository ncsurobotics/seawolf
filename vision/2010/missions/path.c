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

#define PATH_STATE_SEARCHING_FORWARD 0
#define PATH_STATE_SEARCHING_STOPPING 1
#define PATH_STATE_SEARCHING_TURNING 2
#define PATH_STATE_RECORDING 3
#define PATH_STATE_ALIGNING 4

/********* Tuning Values **********/

// Speed we go while searching
#define SEARCHING_SPEED 20

// Time it takes us to stop (in seconds)
#define STOP_TIME 1.0

// How many frames we must see a blob before we think we see the path.
#define SEEN_BLOB_THRESHOLD 3

// How far from the center in the respective direction a blob has to be in
// order to be considered to that side.
#define FORWARD_THRESHOLD 100
#define BACKWARD_THRESHOLD 50
#define LEFT_THRESHOLD 50
#define RIGHT_THRESHOLD 50

// Threshold for our angle when turning toward the blob
#define BLOB_ANGLE_THRESHOLD 10

// The number of frames we must stay facing the correct direction before moving
// on while searching for the path
#define BLOB_TURNING_ALLIGNMENT_FRAMES 3

/**********************************/

// In order to think we see a blob, the blob has to contain a large enough
// percentage of the total orange pixels we see.  This number is that
// percentage.
#define BLOB_PIXEL_PERCENTAGE 0.75

// State Variables
static int path_state = 0;
static int frames_in_a_row_i_have_seen_a_line = 0;
static int frames_in_a_row_i_have_seen_a_blob = 0;
static double blob_angle;
static int blob_correct_angle;
Timer* stop_timer = NULL;

//state variables for ALLIGN_PATH
/* OLD
static int on_path=0,xdist,ydist,direction=0;
static double max_measured_rho;
static int path_alligned = 0;
static CvPoint last_heading = {-999,-999};
static int seen_blob = 0;
static int lost_path = 0;
static double last_theta = -999; // Used to keep track of the correct end of the marker
*/

void mission_align_path_init(IplImage* frame, struct mission_output* results)
{
    path_state = 0;
    frames_in_a_row_i_have_seen_a_line = 0;
    frames_in_a_row_i_have_seen_a_blob = 0;
    if (stop_timer != NULL) {
        Timer_destroy(stop_timer);
    }
    stop_timer = NULL;
    blob_correct_angle = 0;

    results->rho = SEARCHING_SPEED;

    /* OLD
    //state variables for ALLIGN_PATH
    int on_path=0,xdist,ydist,direction=0;
    double max_measured_rho;
    int path_alligned = 0;
    CvPoint last_heading = {-999,-999};
    int seen_blob = 0;
    int lost_path = 0;
    double last_theta = -999; // Used to keep track of the correct end of the marker
    */
}

double get_absolute_angle(double theta);
double get_absolute_angle(double theta) {
    double heading = Var_get("SEA.Yaw") + 180; // From 0 to 360
    return ((int)(theta+heading)) % 360 - 180;
}

struct mission_output mission_align_path_step(struct mission_output result)
{
    result.depth_control = DEPTH_RELATIVE;

    IplImage* grey;
    IplImage* edge;
    IplImage* ipl_out = NULL;
    RGBPixel color = {0xff, 0x88, 0x00};
    CvSeq* lines;

    // Grab Frame
    IplImage* frame = multicam_get_frame(DOWN_CAM);
    ipl_out = cvCreateImage(cvGetSize(frame),8,3);
    result.frame = frame;

    // Color Filter
    int num_pixels = FindTargetColor(frame, ipl_out, &color, 400, 250,3);

    // Blob Detection
    BLOB *blobs;
    int blobs_found = blob(ipl_out, &blobs, 4, 100);

    // Determine if we've seen a blob
    bool see_blob = true;
    if (blobs_found < 1) see_blob = false;
    if (blobs_found > 2) see_blob = false;
    if (blobs[0].area < 0.25*num_pixels) see_blob = false;

    // Keep track of how many frames in a row we've seen a blob
    if (see_blob) {
        frames_in_a_row_i_have_seen_a_blob++;
    } else {
        frames_in_a_row_i_have_seen_a_blob = 0;
    }

    int lines_found;
    if (see_blob) {

        // Hough Transform
        grey = cvCreateImage(cvGetSize(frame), 8, 1);
        cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 50, 200, 3);
        lines = hough(edge, frame, 25, 1, 90, 90, 10, 60, 60);
        float* line = (float*)cvGetSeqElem(lines,0);
        if (line[0] != -999) {
            lines_found = 1;
        }

        #ifdef VISION_SHOW_HEADING
            hough_draw_lines(result.frame, lines);
        #endif

    } else {
        lines_found = 0;
    }

    // Keep track of how many frames in a row we've seen a line
    if (lines_found) {
        frames_in_a_row_i_have_seen_a_line++;
    } else {
        frames_in_a_row_i_have_seen_a_line = 0;
    }

    switch (path_state) {

        case PATH_STATE_SEARCHING_FORWARD:
            result.yaw = 0;
            result.yaw_control = ROT_MODE_RELATIVE;

            // Determine if we see the path
            if (lines_found || frames_in_a_row_i_have_seen_a_blob > SEEN_BLOB_THRESHOLD) {

                // Center of blob so that 0 is the middle of the screen
                int x = blobs[0].mid.x - frame->width/2;
                int y = frame->height/2 - blobs[0].mid.y ;

                // Is the path to the left right or straight?
                if (x < -1*LEFT_THRESHOLD || // Left
                    x > RIGHT_THRESHOLD) // Right
                {
                    double theta;
                    if (y != 0) {
                        theta = atan(x / y) * 180/PI;
                    } else if (x < 0) {
                        theta = -90;
                    } else if (x > 0) {
                        theta = 90;
                    } else {
                        printf("THIS SHOULD NEVER EVER EVER EVER HAPPEN..... EVER!!!!!!1111\n");
                    }
                    printf("Turning toward path at angle %f\n", theta);
                    result.yaw = theta;
                    blob_angle = get_absolute_angle(theta);
                    path_state = PATH_STATE_SEARCHING_STOPPING;

                } else if (y > FORWARD_THRESHOLD) { // Forward
                    result.rho = SEARCHING_SPEED;
                } else if (y < BACKWARD_THRESHOLD) { // Backward
                    result.rho = -1*SEARCHING_SPEED;
                } else if (lines_found) { // Center
                    printf("The path is in the center!!!!\n");
                    result.rho = 0;
                    result.yaw = 0;
                    path_state = PATH_STATE_RECORDING;
                } else { // Blob is centered, but we see no lines, something is wrong
                    printf("I'm confused.  There's a blob in the center, but I see no lines!\n");
                }
            }

        break;

        case PATH_STATE_SEARCHING_STOPPING:

            result.yaw = 0;
            result.rho = 0;

            // Init timer
            if (stop_timer == NULL) {
                stop_timer = Timer_new();
            }

            if (Timer_getTotal(stop_timer) > STOP_TIME) {
                Timer_destroy(stop_timer);
                stop_timer = NULL;
                path_state = PATH_STATE_SEARCHING_TURNING;
            }

        break;

        case PATH_STATE_SEARCHING_TURNING:
            // Turn to the angle I recorded in PATH_STATE_SEARCHING

            result.rho = 0;
            result.yaw = blob_angle;

            if (fabs(blob_angle - Var_get("SEA.Yaw")) < BLOB_ANGLE_THRESHOLD) {
                blob_correct_angle++;
            } else {
                blob_correct_angle = 0;
            }

            // Determine if we've finished
            if (blob_correct_angle > BLOB_TURNING_ALLIGNMENT_FRAMES) {
                blob_correct_angle = 0;
                path_state = PATH_STATE_SEARCHING_FORWARD;
            }

        break;

        case PATH_STATE_RECORDING:
            //TODO
        break;

        case PATH_STATE_ALIGNING:
            //TODO
        break;

        default:
            printf("Warning!  Invalid value for path_state: %d.", path_state);
        break;
    }
    return result;

/* OLD
    IplImage* grey;
    IplImage* edge;
    IplImage* ipl_out = NULL;
    RGBPixel color = {0xff, 0x88, 0x00};
    CvSeq* lines;
    IplImage* frame = multicam_get_frame(DOWN_CAM);
    ipl_out = cvCreateImage(cvGetSize(frame),8,3);
    result.frame = frame;
    
    //set variable modes
    result.depth_control = DEPTH_RELATIVE;
    result.yaw_control = ROT_MODE_RELATIVE;

    // Temporary variables
    double theta=result.yaw;
    int phi=result.depth;
    int rho=result.rho;

    // Run a color filter on the frame to select the path's color
    int num_pixels = FindTargetColor(frame, ipl_out, &color, 400, 250,3);

    // Run hough transform to look for line
    normalize_image(frame);
    grey = cvCreateImage(cvGetSize(frame), 8, 1);
    cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
    edge = edge_opencv(grey, 50, 200, 3);
    lines = hough(edge, frame, 25, 1, 90, 90, 10, 60, 60);
    float* line = (float*)cvGetSeqElem(lines,0);

    #ifdef VISION_SHOW_HEADING
        hough_draw_lines(result.frame, lines);
    #endif

    // If we've seen a blob, keep track of the angle
    if(last_theta != -999 && line[0] != -999){
    
        // ******** HOW HOUGH RETURNS ANGLES: *********** // 
        //  line[1] is returned in radians, measured clockwise 
        //  off the vertical (range from zero to pi)
        // ********************************************** //
        theta = line[1]> PI/2 ? line[1] - PI : line[1]; //Grab angle from hough line 
                                                        // 0 to pi/2 clockwise
                                                        // 0 to -pi/2 ccw from vertical
        // Don't allow theta to jump 180 degrees when the line passes pi/2
        if(theta < 0){
            theta = fabs(theta-last_theta) < fabs((theta + PI) - last_theta) ? theta : theta + PI;
        }else{
            theta = fabs(theta-last_theta) < fabs((theta - PI) - last_theta) ? theta : theta - PI;
        }
        // Store this theta value
        last_theta = theta;
        
        printf("******** theta = %f \n", theta);
    }

    // Look for multiple blobs (3) if we see more than two, assume we arn't
    // getting a solid color filter reading
    BLOB *blobs;
    int blobs_found = blob(ipl_out, &blobs, 4, 100);
    CvPoint heading = blobs[0].mid;

    if(on_path < 6){
        printf("we are centering ourselves\n");
        if (blobs_found == 0 ||
            blobs_found>3 ||
            blobs[0].area < (num_pixels*4/5>1000?num_pixels*4/5:1000) ||
            line[0] == -999)
        {
            // We don't see a blob
            seen_blob = 0;
            if(last_heading.x == -999 && last_heading.y == -999){
                // We have no clue where the marker is
                rho = 10;
                theta = 0;
                phi = 0;
            } else if (last_heading.y < frame->height/2) {
                rho = 10;
                theta = 0;
                phi = 0;
            } else {
                rho = -10;
                theta = 0;
                phi = 0;
            }
        } else if ( ++seen_blob>3) {
            // We see a blob, lets try and track it
            phi = 0;
            xdist = heading.x - frame->width/2;
            ydist = frame->height/2 - heading.y ;
            theta = tan(abs(ydist)/xdist);
            max_measured_rho = sqrt((frame->width/2)*(frame->width/2)+(frame->height/2)*(frame->height/2));
            rho = sqrt(xdist*xdist + ydist*ydist); // Compute estimated distance to target
            if(ydist < 0){
                // If we need to go backwards, change the sign of rho and theta
                theta = -1*theta;
                rho = -1*rho;
            }
            // Scale the rho and theta value
            rho = (rho*MAX_RHO/max_measured_rho);

            // Decide if this counts as on top of the marker
            if(abs(rho) < MAX_RHO/6) {
                on_path++;
            } else {
                on_path = 0;
            }
            // Don't go charging off until we are pointed at the target
            if(abs(theta) > .1) rho = 0;

            // Try to aproximate actual distance we need to cover (so scale rho
            // AGAIN)
            rho /=4; // Scaled down additionaly, b/c we will never be more than a few feet off

        }else{
            // We see what might become a blob, so let's initialize last_theta
            // here
            // Only initialize this value once.
            if(last_theta == -999){
                printf("initializing theta\n");
                last_theta = line[1]> PI/2 ? line[1] - PI : line[1]; //Grab angle from hough line 
            }
        }

    }else{
        // We are now supposing ourselves to be on the marker, and need to
        // orient correctly

        printf("on maker: **** theta = %f \n",theta);

        if(blobs_found == 0 || blobs_found>3) { // If we don't see the marker
            // Just wait for it to come back I suppose
            theta = 0;
            lost_path++;

        }else if(line[0] != -999) {
            lost_path=0;

            if(fabs(theta)< .1) {
                path_alligned++;
            } else {
                path_alligned=0; // Only consecutive counts
            }
            if(path_alligned>10) {
                // We have just completed a task and can start the next one,
                // beginning with bringing craft to correct altitude
                // SET NEW MISSION DEPTH, THEN MOVE FORWARD OFF PATH MARKER
                theta = 0;
                printf("we are alligned\n");
                // Reset our state variables so they don't conflict when we run
                // allign path again
                int on_path=0,xdist,ydist,direction=0;
                double max_measured_rho;
                int path_alligned = 0;
                CvPoint last_heading = {-999,-999};
                int seen_blob = 0;
                int lost_path = 0;
                float last_theta = -999; // Used to keep track of the correct end of the marker
                result.mission_done = true;
            }
            // Now set the rho (we do still want to try to stay centered, and y
            // is the easy direction
            rho = ((frame->height/2-heading.y)*MAX_RHO/(frame->height/2))/4;
            // Make sure the path isn't horribly off the screen in the x
            // direction. if it is, fall back to centering ourselves
            if(abs(heading.x-frame->width/2)>(frame->width/2)*3/4) {
                printf("GOD DAMNIT I'M LOOSING THE BLOODY MARKER, NOW I HAVE TO GO GET  BACK ON TOP OF IT\n");
                on_path=0;
            }
        } else {
            // We see a blob but not a line, so it's prob. not our blob
            theta = 0;
            lost_path++;
        }
        if (lost_path>4) {
            // We deffinetly lost the path so let's go find it again
            lost_path=0;
            on_path=0;
        }
        phi = 0; // We don't want to go up or down

    }

    // Screen results based on blob size
    if (frame->width*frame->height / 5 >num_pixels && ++seen_blob>4) {
        last_heading = heading;
    }

    // Update direction
    result.yaw = theta;
    result.depth = phi;
    result.rho = rho;

    // Release Resources
    blob_free (blobs, blobs_found);
    cvReleaseImage(&grey);
    cvReleaseImage(&edge);
    cvReleaseImage(&ipl_out);
    //cvRelease((void**) &lines);
    cvReleaseMemStorage(&(lines->storage));

    return result;
    */
}
