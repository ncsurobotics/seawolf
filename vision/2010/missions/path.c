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

static char* path_state_names[] = {
    [PATH_STATE_SEARCHING_FORWARD] = "SEARCHING FORWARD",
    [PATH_STATE_SEARCHING_STOPPING] = "SEARCHING STOPPING",
    [PATH_STATE_SEARCHING_TURNING] = "SEARCHING TURNING",
    [PATH_STATE_RECORDING] = "RECORDING",
    [PATH_STATE_ALIGNING] = "ALIGNING"
};

/********* Tuning Values **********/

// Speed we go while searching
#define SEARCHING_SPEED 10

// Time it takes us to stop (in seconds)
#define STOP_TIME 0.0

// How many frames we must see a blob before we think we see the path.
#define SEEN_BLOB_THRESHOLD 3

// In order to think we see a blob, the blob has to contain a large enough
// percentage of the total orange pixels we see.  This number is that
// percentage.
#define BLOB_PIXEL_PERCENTAGE 0.75

// How far from the center in the respective direction a blob has to be in
// order to be considered to that side.
#define FORWARD_THRESHOLD 100
#define BACKWARD_THRESHOLD 25
#define LEFT_THRESHOLD 100
#define RIGHT_THRESHOLD 100

// How many frames in a row a blob is centered before we move on
#define FRAMES_BLOB_CENTERED 5

// Threshold for our angle when turning toward the blob
#define BLOB_ANGLE_THRESHOLD 10

// The number of frames we must stay facing the correct direction before moving
// on while searching for the path
#define BLOB_TURNING_ALLIGNMENT_FRAMES 2

// When I'm getting a reading for where the marker is pointed, I'll average
// over this many samples to figure out where to go.
#define NUM_ANGLES_TO_AVERAGE 4

// While averaging the angles, the range must be less than this or it's assumed
// that we're getting bad values
#define ANGLE_DEVIATION_THRESHOLD 10

// Threshold for our angle while aligning with the marker
#define ALIGN_ANGLE_THRESHOLD 10

// The number of frames we must stay facing the correct direction before moving
// on while alligning with path
#define PATH_TURNING_ALLIGNMENT_FRAMES 10

/**********************************/

// State Variables
static int path_state = 0;
static int frames_in_a_row_i_have_seen_a_line = 0;
static int frames_in_a_row_i_have_seen_a_blob = 0;
static double blob_angle;
static int blob_correct_angle;
Timer* stop_timer = NULL;
static double recorded_angles[NUM_ANGLES_TO_AVERAGE];
static int num_angles_recorded = 0;
static int align_correct_angle;
static int path_centered;
static bool recording;
static int initial_angle;

double get_absolute_angle(double theta);

void mission_align_path_init(IplImage* frame, struct mission_output* results)
{
    path_state = 0;
    frames_in_a_row_i_have_seen_a_line = 0;
    frames_in_a_row_i_have_seen_a_blob = 0;
    path_centered = 0;
    if (stop_timer != NULL) {
        Timer_destroy(stop_timer);
    }
    stop_timer = NULL;
    blob_correct_angle = 0;
    num_angles_recorded = 0;
    align_correct_angle = 0;
    recording = false;

    //record which way we are currently facing
    initial_angle = Var_get("ReferenceAngle");
    printf("Initial angle: %d\n", initial_angle);

    results->rho = SEARCHING_SPEED;
    results->yaw = 0;
    results->depth_control = DEPTH_ABSOLUTE;
    results->depth = 1.0;

}

double get_absolute_angle(double theta) {
    double heading = Var_get("SEA.Yaw") + 180; // From 0 to 360
    printf("THETA, HEADING: %f, %f\n", theta, heading);
    return abs( ((int)(theta+heading)) % 360) - 180; // From -180 to 180
}

struct mission_output mission_align_path_step(struct mission_output result)
{
    result.depth_control = DEPTH_RELATIVE;

    IplImage* grey;
    IplImage* edge;
    IplImage* ipl_out = NULL;
    RGBPixel color = {0xff, 0x88, 0x00};
    CvSeq* lines;
    float* line;
    double current_yaw;
    
    // Grab Frame
    IplImage* frame = multicam_get_frame(DOWN_CAM);
    ipl_out = cvCreateImage(cvGetSize(frame),8,3);
    result.frame = frame;

    // Color Filter
    int num_pixels = FindTargetColor(frame, ipl_out, &color, 400, 350, 2.25);

    // Blob Detection
    BLOB *blobs;
    int blobs_found = blob(ipl_out, &blobs, 4, 300);

    // Determine if we've seen a blob
    bool see_blob = true;
    if (blobs_found < 1) see_blob = false;
    if (blobs_found > 2) see_blob = false;
    if (blobs[0].area < BLOB_PIXEL_PERCENTAGE*num_pixels) see_blob = false;

    // Keep track of how many frames in a row we've seen a blob
    if (see_blob) {
        frames_in_a_row_i_have_seen_a_blob++;
    } else {
        frames_in_a_row_i_have_seen_a_blob = 0;
    }

    printf("path_state: %s\n", path_state_names[path_state]);

    int lines_found;
    if (see_blob) {

        // Hough Transform
        grey = cvCreateImage(cvGetSize(frame), 8, 1);
        cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 50, 200, 3);
        lines = hough(edge, frame, 25, 1, 90, 90, 10, 60, 60);
        line = (float*)cvGetSeqElem(lines,0);
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
            result.yaw_control = ROT_MODE_RELATIVE;

            // Determine if we see the path
            if (lines_found || frames_in_a_row_i_have_seen_a_blob > SEEN_BLOB_THRESHOLD) {

                // Center of blob so that 0 is the middle of the screen
                int x = blobs[0].mid.x - frame->width/2;
                int y = frame->height/2 - blobs[0].mid.y ;
                printf("Blob found at: %d, %d\n", x, y);

                // Is the path to the left right or straight?
                if (x < -1*LEFT_THRESHOLD || // Left
                    x > RIGHT_THRESHOLD) // Right
                {
                    double theta;
                    if (y != 0) {
                        theta = atan( ((double)x) / ((double)y) ) * 180.0/PI;
                        if (y < 0) {
                            theta += 180;
                        }
                    } else if (x < 0) {
                        theta = -90;
                    } else if (x > 0) {
                        theta = 90;
                    } else {
                        printf("THIS SHOULD NEVER EVER EVER EVER HAPPEN..... EVER!!!!!!1111\n");
                    }
                    printf("Turning toward path at angle %f\n", theta);
                    blob_angle = get_absolute_angle(theta);
                    result.yaw = theta;
                    path_centered = 0;
                    result.rho = 0;

                } else if (y > FORWARD_THRESHOLD) { // Forward
                    result.rho = SEARCHING_SPEED;
                    result.yaw = 0;
                    path_centered = 0;
                } else if (y < -1*BACKWARD_THRESHOLD) { // Backward
                    result.rho = -1*SEARCHING_SPEED;
                    result.yaw = 0;
                    path_centered = 0;
                } else if (lines_found) { // Center
                    printf("The path is in the center!!!!\n");
                    path_centered++;
                    result.rho = 0;
                    result.yaw = 0;
                } else { // Blob is centered, but we see no lines, something is wrong
                    printf("I'm confused.  There's a blob in the center, but I see no lines!\n");
                }
            }

            if (result.yaw != 0) {
                current_yaw = Var_get("SEA.Yaw");
                printf("Turning to Blob angle: %f / %f\n", current_yaw, blob_angle);
                if (fabs(blob_angle - current_yaw) < BLOB_ANGLE_THRESHOLD) {
                    blob_correct_angle++;
                } else {
                    blob_correct_angle = 0;
                }
            }

            // If we've been heading in the right direction for long enough, go
            // forward
            if (blob_correct_angle > BLOB_TURNING_ALLIGNMENT_FRAMES) {
                blob_correct_angle = 0;
                result.rho = SEARCHING_SPEED;
            }

            // Determine if we've finished
            if (path_centered >= FRAMES_BLOB_CENTERED) {
                printf("I've been centered for long enough.  Recording...\n");
                //path_state = PATH_STATE_RECORDING;
                recording = true;
            }

            if (recording && lines_found != 0) {

                // Record a value
                double theta = line[1] * 180.0/PI;
                printf("line[1], theta: %f, %f\n", line[1], theta);
                recorded_angles[num_angles_recorded%NUM_ANGLES_TO_AVERAGE] = get_absolute_angle(theta);
                num_angles_recorded++;

                printf("RECORDED ANGLES:");
                for (int i=0; i<NUM_ANGLES_TO_AVERAGE; i++) {
                    printf(" %f", recorded_angles[i]);
                }
                printf("\n");

                if (num_angles_recorded >= NUM_ANGLES_TO_AVERAGE) {
                    // Search for highest and lowest to get range
                    double min = recorded_angles[0];
                    double max = recorded_angles[0];
                    double sum = 0;
                    for (int i=0; i<NUM_ANGLES_TO_AVERAGE; i++) {
                        double recorded_angle = recorded_angles[i];
                        if (recorded_angle < min) {
                            min = recorded_angles[i];
                        }
                        if (recorded_angle > max) {
                            max = recorded_angles[i];
                        }
                        sum += recorded_angle;
                    }

                    // The second term accounts for wraparound
                    if (fabs(min-max) < ANGLE_DEVIATION_THRESHOLD ||
                        fabs(min-max) > 360-ANGLE_DEVIATION_THRESHOLD) {

                        // Compute average in cartesian space
                        double avg_x = 0;
                        double avg_y = 0;
                        printf("Computing average X and Y:\n");
                        for (int i=0; i<NUM_ANGLES_TO_AVERAGE; i++) {
                            printf("  Recorded angle: %f\n", recorded_angles[i]);
                            printf("    Adding %f to avg_x\n", cos(-1*PI/180 * recorded_angles[i]));
                            printf("    Adding %f to avg_y\n", sin(-1*PI/180 * recorded_angles[i]));
                            avg_x += cos(-1*PI/180 * recorded_angles[i]);
                            avg_y += sin(-1*PI/180 * recorded_angles[i]);
                        }
                        printf("Total: avg_x=%f avg_y=%f\n", avg_x, avg_y);
                        avg_x /= NUM_ANGLES_TO_AVERAGE;
                        avg_y /= NUM_ANGLES_TO_AVERAGE;
                        printf("AFter Dividing: avg_x=%f avg_y=%f\n", avg_x, avg_y);
                        result.yaw = -1*atan(avg_y / avg_x);
                        printf("-1*atan(avg_y / avg_x) = %f\n", result.yaw);
                        if(avg_x < 0) {
                            result.yaw += PI * (avg_y < 0 ? 1 : -1);
                            printf("ADding %f to yaw\n", PI * (avg_y < 0 ? 1 : -1));
                        }
                        result.yaw *= 180/PI;
                        printf("Final yaw in degrees: %f\n", result.yaw);

                        printf("Initial_angle: %d\n", initial_angle);
                        //now set yaw to the end of the marker closest to 
                        // our origional heading
                        // backwards_angle is the angle 180 degrees away from our current yaw
                        int backwards_angle = result.yaw + 180;
                        backwards_angle = (backwards_angle + 180) % 360 - 180; // Modulous between -180 to 180
                        if(abs(result.yaw - initial_angle) > 90 && abs(result.yaw - initial_angle) < 270){
                            // The angle 180 degrees off from result.yaw is closer to inital_angle
                            result.yaw = backwards_angle;
                        }


                        result.yaw_control = ROT_MODE_ANGULAR;
                        path_state = PATH_STATE_ALIGNING;

                    }
                }
            }

            #ifdef VISION_SHOW_HEADING
                CvPoint lower_right = cvPoint(frame->width/2 + RIGHT_THRESHOLD, frame->height/2 - BACKWARD_THRESHOLD);
                CvPoint upper_left = cvPoint(frame->width/2 - LEFT_THRESHOLD, frame->height/2 + FORWARD_THRESHOLD);
                CvScalar rect_color = cvScalar(255, 255, 0, 0);
                cvRectangle(result.frame, lower_right, upper_left, rect_color, 0, 8, 0);
            #endif

        break;

        /*
        case PATH_STATE_SEARCHING_STOPPING:

            if (STOP_TIME != 0.0) {
                printf("Stopping...\n");
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
            } else {
                path_state = PATH_STATE_SEARCHING_TURNING;
            }
        // If STOP_TIME is zero, we'll just fall through

        case PATH_STATE_SEARCHING_TURNING:
            // Turn to the angle I recorded in PATH_STATE_SEARCHING

            result.rho = 0;
            result.yaw_control = ROT_MODE_ANGULAR;
            result.yaw = blob_angle;

            current_yaw = Var_get("SEA.Yaw");
            printf("Turning to Blob angle: %f / %f\n", current_yaw, blob_angle);
            if (fabs(blob_angle - current_yaw) < BLOB_ANGLE_THRESHOLD) {
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
        */

        /*
        case PATH_STATE_RECORDING:
            
            //make sure we see a line before recording
            if(lines_found == 0) break;

            // Record a value
            double theta = line[1] * 180.0/PI;
            printf("line[1], theta: %f, %f\n", line[1], theta);
            recorded_angles[num_angles_recorded%NUM_ANGLES_TO_AVERAGE] = get_absolute_angle(theta);
            num_angles_recorded++;

            printf("RECORDED ANGLES:");
            for (int i=0; i<NUM_ANGLES_TO_AVERAGE; i++) {
                printf(" %f", recorded_angles[i]);
            }
            printf("\n");

            if (num_angles_recorded >= NUM_ANGLES_TO_AVERAGE) {
                // Search for highest and lowest to get range
                double min = recorded_angles[0];
                double max = recorded_angles[0];
                double sum = 0;
                for (int i=0; i<NUM_ANGLES_TO_AVERAGE; i++) {
                    double recorded_angle = recorded_angles[i];
                    if (recorded_angle < min) {
                        min = recorded_angles[i];
                    }
                    if (recorded_angle > max) {
                        max = recorded_angles[i];
                    }
                    sum += recorded_angle;
                }

                // The second term accounts for wraparound
                if (fabs(min-max) < ANGLE_DEVIATION_THRESHOLD ||
                    fabs(min-max) > 360-ANGLE_DEVIATION_THRESHOLD) {

                    // Average angle and move to next state
                    result.yaw = sum / NUM_ANGLES_TO_AVERAGE;
                    result.yaw_control = ROT_MODE_ANGULAR;
                    path_state = PATH_STATE_ALIGNING;

                }
            }

        break;
        */

        case PATH_STATE_ALIGNING:

            current_yaw = Var_get("SEA.Yaw");
            printf("Alligning with path angle: %f / %f\n", current_yaw, result.yaw);
            if (fabs(result.yaw - current_yaw) < ALIGN_ANGLE_THRESHOLD) {
                align_correct_angle++;
            } else {
                align_correct_angle = 0;
            }

            // Determine if we've finished
            if (align_correct_angle > PATH_TURNING_ALLIGNMENT_FRAMES) {

                // Mission is finished!!!
                result.mission_done = true;
                result.rho = 20;

            }
        break;

        default:
            printf("Warning!  Invalid value for path_state: %d.", path_state);
        break;
    }
    
    //Free Our Resources
    blob_free (blobs, blobs_found);
    cvReleaseImage (&ipl_out);
    if (see_blob) {
        // Free Hough resources
        cvReleaseImage(&grey);
        cvReleaseImage(&edge);
        cvRelease((void**) &lines);
    }    
    
    
    return result;
}
