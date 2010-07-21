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
#include "util.h"


/******* #DEFINES for Window **********/

// Definitions for the window colors NOT THE ORDER, SEE BELOW
#define YELLOW_WINDOW 1
#define RED_WINDOW    2
#define GREEN_WINDOW  3
#define BLUE_WINDOW   4

// The Window we need to hit
#define TARGET_WINDOW RED_WINDOW

// Window Order from top left to bottom right:
// 1 2
// 3 4
static int window_order[] = {
    [RED_WINDOW]    = 3,
    [BLUE_WINDOW]   = 2,
    [GREEN_WINDOW]  = 1,
    [YELLOW_WINDOW] = 4
}; 

static RGBPixel window_colors[] = {
    [RED_WINDOW] = {0xff, 0x00, 0x00},
    [BLUE_WINDOW] = {0x00, 0x00, 0xff},
    [GREEN_WINDOW] = {0x00, 0xff, 0x00},
    [YELLOW_WINDOW] = {0xff, 0xff, 0x00},
};

//DEPTH OF THE WINDOW ROWS
#define TOP_ROW_DEPTH 1
#define BOTTOM_ROW_DEPTH 2

// Y value for where a blob is found is multiplied by this to get the relative
// depth heading
#define DEPTH_SCALE_FACTOR (1.0/200.0)

// Bigger the number, the less we turn
#define YAW_SCALE_FACTOR 5

// How Long We Must See a Blob Durring Approach
#define APPROACH_THRESHOLD 1

// How Long we must see a blob durring Lock on Target to think it's not noise
#define TRACKING_THRESHOLD 2

// How large blobs must be
#define MIN_BLOB_SIZE 200

// What fraction of the found color has to be taken up by a blob for us to
// consider it a blob
#define BLOB_COLOR_FRACTION (3.0/4.0)

//what height to start the robot at
#define INITIAL_DEPTH 2

//how fast to turn when alligning with a window
#define TURN_RATE 5

// How Far to Turn When Looking for a Window
#define TURNING_THRESHOLD 70

// How Fast to approach a window when locking onto it
#define TRACKING_SPEED 10

// How much of the frame a window must fill (horizontally) to be considered close enough to fire
#define WINDOW_SCREEN_FRACTION 0.8

// How long we must spend centering on target before moving forward
#define TRACKING_PAUSE 5

// How Long we must lose a window for before backing up to find it
#define LOST_THRESHOLD 2

//State variables for Window
#define WINDOW_STATE_FIRST_APPROACH 0
#define WINDOW_STATE_FIRST_ORIENTATION 1
#define WINDOW_STATE_LOCK_ON_TARGET 2
#define FIRE_ZE_MISSILES            3
#define WINDOW_STATE_COMPLETE       4

static int window_state = 0; //tracks the state of the window mission
static Timer* search_timer = NULL; //timer used when searching for path after windows
static double initial_angle = 0; //tracks what angle we were at approaching the Windows mission

//state variables for first approach
static int approach_counter = 0;  //counts how many frames we've seen any blob
static int window_found = 0; //tracks which window we've seen
static int tracking_pause = 0;

//state variable for orientation
static double starting_angle;

//state variables for window_lock_on_target
static int lock_counter = 0;
static int tracking_counter = 0;
static int window_initialized = 0;
static int lost_blob = 0;

void mission_window_init(struct mission_output* result)
{

    window_state = WINDOW_STATE_FIRST_APPROACH;
    approach_counter = 0;
    tracking_pause = 0;
    result->depth_control = DEPTH_ABSOLUTE;
    result->depth = INITIAL_DEPTH;

    if (search_timer != NULL) {
        Timer_destroy(search_timer);
    }
    search_timer = NULL;
    initial_angle = Var_get("SEA.Yaw");
}

struct mission_output mission_window_step(struct mission_output result)
{

    switch (window_state) {

        case WINDOW_STATE_FIRST_APPROACH:
            //drive forward
            result.rho = 10;

            //scan the image for any of the three bouys
            window_found = window_first_approach(&result);

            // if we see a bouy, move on
            if(window_found){
                printf("we finished the approach \n");
                window_state++;
            } else {
                // Don't break if we're going to change states, or we would
                // waste a frame
                break;
            }

        case WINDOW_STATE_FIRST_ORIENTATION:

            //stop the robot
            result.rho = 0;
            
            //set our depth to the first bouy we need to see
            if(window_order[TARGET_WINDOW] < 3){
                result.depth = TOP_ROW_DEPTH;
            }else{
                result.depth = BOTTOM_ROW_DEPTH;
            }

            //turn towards our first bouy
            result.yaw_control = ROT_MODE_RATE;

            //record what angle we started this turn
            starting_angle = Var_get("SEA.Yaw");

            //if we are on an odd window, and need to go to even, turn right
            //if on even, need to go to odd, turn left
            //otherwise, don't turn, just change depth
            if(window_order[window_found]%2 == 0 && window_order[TARGET_WINDOW]%2 ==1){
                //TURN LEFT
                printf("Going LEFT to desired window\n");
                result.yaw = -1*TURN_RATE;
            }
            else if(window_order[window_found]%2 == 1 && window_order[TARGET_WINDOW]%2 ==0){
                //TURN RIGHT
                printf("Going RIGHT to desired window\n");
                result.yaw = TURN_RATE;
            }
            else if(window_found == TARGET_WINDOW){
                printf("Facing Target Window\n");
                //STAY STRAIGHT
            } else {
                printf("Sees the window above or below target\n");
            }
            window_state++;
            // Move onto next case without a break so that we don't waste a
            // frame

        case WINDOW_STATE_LOCK_ON_TARGET:
            //initialize targeting function
            printf("Locking on target\n");
            if(window_initialized == 0){
                window_lock_on_target_init();
            }

            //run bump routine until complete
            if( window_lock_on_target(&result, &window_colors[TARGET_WINDOW]) == 1){
                window_state++;
                window_initialized = 0;
                printf("we finished locking on target ^^\n");
            }else{
                //grab angle data to check how far we have turned
                double current_angle = Var_get("SEA.Yaw");
                if(!(fabs(current_angle-starting_angle) < TURNING_THRESHOLD ||
                    fabs(current_angle-starting_angle) > 360-TURNING_THRESHOLD))
                {
                    //We have turned too far
                    result.yaw *= -1;
                    starting_angle = current_angle;
                }
            }
            break;

        case FIRE_ZE_MISSILES: 
            //do it. do it now. 
            printf("Firing Ze Missiles!\n");
            Notify_send("RUN", "Torpedo");
            Util_usleep(1);
        
        case WINDOW_STATE_COMPLETE:
            //I guess we are done
            break;

        default:
            printf("window_state SET TO UNDEFINED VALUE\n");
            break;
              
    }
    return result;
}

int find_window(IplImage* frame, BLOB** found_blob, int* blobs_found_arg, int target_color) {

    int found_target = 0;

    IplImage* ipl_out[4];
    ipl_out[0] = cvCreateImage(cvGetSize (frame), 8, 3);
    ipl_out[1] = cvCreateImage(cvGetSize (frame), 8, 3);
    ipl_out[2] = cvCreateImage(cvGetSize (frame), 8, 3);
    ipl_out[3] = cvCreateImage(cvGetSize (frame), 8, 3);

    int num_pixels[4];                                                 //color thresholds
    num_pixels[0] = FindTargetColor(frame, ipl_out[0], &window_colors[YELLOW_WINDOW], 1, 280, 2.0); 
    num_pixels[1] = FindTargetColor(frame, ipl_out[1], &window_colors[RED_WINDOW], 1, 400, 2.0);
    num_pixels[2] = FindTargetColor(frame, ipl_out[2], &window_colors[GREEN_WINDOW], 1, 1, 1);
    num_pixels[3] = FindTargetColor(frame, ipl_out[3], &window_colors[BLUE_WINDOW], 1, 1, 1);

    // Debugs
    #ifdef VISION_GRAPHICAL
        cvNamedWindow("Yellow", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Red", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Green", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Blue", CV_WINDOW_AUTOSIZE); 
        cvShowImage("Yellow", ipl_out[0]);
        cvShowImage("Red", ipl_out[1]);
        cvShowImage("Green", ipl_out[2]);
        cvShowImage("Blue", ipl_out[3]);
    #endif

    //Look for blobs
    BLOB* blobs[4];
    int blobs_found[4];
    blobs_found[0] = blob(ipl_out[0], &blobs[0], 4, MIN_BLOB_SIZE);
    blobs_found[1] = blob(ipl_out[1], &blobs[1], 4, MIN_BLOB_SIZE);
    blobs_found[2] = blob(ipl_out[2], &blobs[2], 4, MIN_BLOB_SIZE);
    blobs_found[3] = blob(ipl_out[3], &blobs[3], 4, MIN_BLOB_SIZE);

    printf("Blobs found: y=%d r=%d g=%d b=%d\n", blobs_found[0], blobs_found[1], blobs_found[2], blobs_found[3]);

    int seen_blob[4];
    BLOB* blobs_seen[4];
    RGBPixel colors_seen[4];
    int indexes_seen[4];
    int num_colors_seen = 0;
    static int max_blob_size = 1000000000;
    for (int i=0; i<4; i++) {
        //printf("blobs[%d]->area = %ld\n", i, blobs[i]->area);
        if ((blobs_found[i] == 1 || blobs_found[i] == 2) &&
            blobs[i]->area < max_blob_size &&
            ((float)blobs[i]->area) / ((float)num_pixels[i]) > BLOB_COLOR_FRACTION)
        {
            //printf("i=%d\n", i);
            blobs_seen[num_colors_seen] = blobs[i];
            colors_seen[num_colors_seen] = window_colors[i+1];
            indexes_seen[num_colors_seen] = i+1;
            num_colors_seen++;
            seen_blob[i] = 1;
        } else {
            //printf("Blob amount / Filter amount = %f\n", ((float)blobs[i]->area) / ((float)num_pixels[i]));
            seen_blob[i] = 0;
        }
    }

    // Make a decision baised on how many colors we've seen:
    //  0) We saw nothing
    //  1) The one color we saw is correct
    //  2) Choose the color that's closer to it's target
    //  3) We're getting bad data, assume we saw nothing
    //printf("Number of bouys seen: %d\n", num_colors_seen);
    if (num_colors_seen == 1) {
        found_target = indexes_seen[0];
    } else if (num_colors_seen == 2) {
        /*
        found_bouy = indexes_seen[
            find_closest_blob(2, colors_seen, blobs_seen, frame)
        ];
        */
        if (blobs_seen[0]->area > blobs_seen[1]->area) {
            found_target = indexes_seen[0];
        } else {
            found_target = indexes_seen[1];
        }
    } else if (num_colors_seen == 0 || num_colors_seen == 3) {
        //we don't see anything
        found_target = 0;
    }

    //free resources
    for (int i=0; i<4; i++) {
        if (i == found_target-1) {
            *found_blob = blobs[i];
            *blobs_found_arg = blobs_found[i];
        } else {
            blob_free(blobs[i], blobs_found[i]);
        }
        cvReleaseImage(&ipl_out[i]);
    }

    return found_target;
}

/*******      First Approach      ***********/
// Scan Image, if we see a target, return it's color.  Otherwise
// return zero.
int window_first_approach(struct mission_output* result){

    //obtain frame
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    result->frame = frame;
    //frame = normalize_image(frame);

    BLOB* found_blob = NULL;
    int blobs_found = 0;
    int found_target= find_window(frame, &found_blob, &blobs_found, 0);

    approach_counter++;
    if (found_target == YELLOW_WINDOW) {
        printf("FOUND YELLOW\n");
    } else if (found_target == RED_WINDOW) {
        printf("FOUND RED\n");
    } else if (found_target == GREEN_WINDOW) {
        printf("FOUND GREEN\n");
    } else if (found_target == BLUE_WINDOW) {
        printf("FOUND BLUE\n");
        approach_counter = 0;
    } else {
        approach_counter = 0;
    }

    //if we've seen a blob for longer than a threshold, finish
    printf("approch_counter=%d\n", approach_counter);
    if(approach_counter <= APPROACH_THRESHOLD){
        //we haven't seen the blob long enough, keep trying
        found_target = 0;
    }

    if (found_blob != NULL) {
        blob_free(found_blob, blobs_found);
    }

    return found_target;

}

/******* Window lock on target ********/
void window_lock_on_target_init(void) {
    lock_counter = 0;
    tracking_counter = 0;
    window_initialized = 1;
    lost_blob = 0;
}

int window_lock_on_target(struct mission_output* result, RGBPixel* color) {
    IplImage* frame = multicam_get_frame(FORWARD_CAM);
    result->frame = frame;
    int frame_width = frame->width;
    int frame_height = frame->height;
    int target_locked = 0;

    BLOB* found_blob = NULL;
    int blobs_found = 0;
    int found_target= find_window(frame, &found_blob, &blobs_found, 0);

    // If we saw the wrong color, ignore it
    if (window_colors[found_target].r != color->r ||
        window_colors[found_target].g != color->g ||
        window_colors[found_target].b != color->b
    ) {
        blobs_found = 0;
    }

    if (blobs_found == 0 && tracking_counter < TRACKING_THRESHOLD) {
        // Keep turning, we didn't see anything
        tracking_counter = 0;

    } else if (blobs_found == 0 && lost_blob++ > LOST_THRESHOLD) {
        printf("Lost blob, backing up\n");
        //back up, try and find it again
        result->rho = -1*TRACKING_SPEED;
        tracking_pause = 0;
    } else if (blobs_found == 0) {
        printf("Lost blob\n");
    } else if (++tracking_counter > TRACKING_THRESHOLD) {
        lost_blob = 0;
        //result->depth_control = DEPTH_RELATIVE;
        // Set thruster values to track
        printf("setting yaw to chase a blob\n");
        CvPoint heading = found_blob[0].mid;
        result->yaw = heading.x;
        //result->depth = heading.y;
        cvCircle(result->frame, cvPoint(result->yaw, result->depth), 5, cvScalar(0,0,0,255),1,8,0);
        //adjust to put the origin in the center of the frame
        result->yaw = result->yaw - frame_width / 2;
        //result->depth = result->depth - frame_height / 2;
        //result->depth *= DEPTH_SCALE_FACTOR; // Scaling factor
        //subjectively scale output !!!!!!!
        result->yaw = result->yaw / YAW_SCALE_FACTOR; // Scale Output

        //Convert Pixels to Degrees
        result->yaw = PixToDeg(result->yaw);

        //Check the size of the blob, and move forward (slowly) if neccessary
        if((float)(found_blob[0].right - found_blob[0].left)/frame_width > WINDOW_SCREEN_FRACTION){
            if(tracking_pause++ > TRACKING_PAUSE){
                //we are close enough, stop the robot.
                result->rho = 0;
                printf("IN CORRECT POSITION");
            }
        }else{
            //we should move forward slowly
            result->rho = TRACKING_SPEED;
            printf("approaching window \n");
        }

        // See if we've centered

        // If we've centered for long enough... huzzah!!!

    } else {
        // We saw something but not long enough to be sure
    }

    //RELEASE THINGS
    if (found_blob != NULL) {
        blob_free (found_blob, blobs_found);
    }

    return target_locked;

}
