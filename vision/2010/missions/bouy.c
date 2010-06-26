
#include "seawolf.h"
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "seawolf3.h"

#include "util.h"
#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#include "mission.h"

/******* #DEFINES for BOUY **********/

// Definitions for the bouy colors
#define YELLOW_BOUY 1
#define RED_BOUY    2
#define GREEN_BOUY  3

//order of bouys from left to right
static int bouy_order[] = {
    [RED_BOUY]    = 1,
    [GREEN_BOUY]  = 2,
    [YELLOW_BOUY] = 3
};

// The order to hit the bouys in
#define BOUY_1 YELLOW_BOUY
#define BOUY_2 RED_BOUY

// States for the bouy state machine
#define BOUY_STATE_FIRST_APPROACH 0
#define BOUY_STATE_FIRST_ORIENTATION 1
#define BOUY_STATE_BUMP_FIRST_BOUY 2
#define BOUY_STATE_FIRST_BACKING_UP 3
#define BOUY_STATE_SECOND_ORIENTATION 4
#define BOUY_STATE_BUMP_SECOND_BOUY 5
#define BOUY_STATE_FINAL_ORIENTATION 6
#define BOUY_STATE_FINISH_FINAL_TURN_1 7
#define BOUY_STATE_SEARCHING_FOR_PATH 8
#define BOUY_STATE_COMPLETE 9

// How Long We Must See a Blob Durring Approach
#define APPROACH_THRESHOLD 2

// How large blobs must be
#define MIN_BLOB_SIZE 200

// What fraction of the found color has to be taken up by a blob for us to
// consider it a blob
#define BLOB_COLOR_FRACTION (3.0/4.0)

// Turn Rate When Searching For Bouys
#define TURN_RATE 5

// How Long To Back Up After 1st Bouy
#define BACK_UP_TIME_1 7

// How long in SECONDS after we first saw a blob in bouy_bump before we give up and say we hit it.
#define BOUY_BUMP_TIMER 7

// How many consecutive frames we must see a bouy before thinking we've hit it
#define MAX_TRACKING_COUNT 45

// How many frames since first seeing a large blob before we think we've hit a bouy
#define BIG_BLOB_WAIT 10

// Y value for where a blob is found is multiplied by this to get the relative
// depth heading
#define DEPTH_SCALE_FACTOR (1.0/200.0)

// How far to turn after bumping the second bouy in degrees
#define TURN_AMOUNT_AFTER_SECOND_BOUY_BUMP 70

// How many frames we need to see an orangle blob to think we've seen the path
#define SEEN_PATH_THRESHOLD 2 

// Bigger the number, the less we turn
#define YAW_SCALE_FACTOR 1

//how long each leg of the search should be
#define SEARCH_PATTERN_TIME 6
/************* STATE VARIABLES FOR BOUY *************/

// State Variables for Bouy Mission
double initial_angle = 0;
static int bouy_state = 0;           //Keeps track of primary bouy state machine
static int bouys_found = 0;          //turns to 1,2, or 3 when a bouy is found, # signifies color
static RGBPixel bouy_colors[] = {    //holds the three colors of the bouys

    // Ideal Colors
    [YELLOW_BOUY] = {0xff, 0xff, 0x00 },
    [RED_BOUY]    = {0xff, 0x00, 0x00 },
    [GREEN_BOUY]  = {0x00, 0xff, 0x00 },

    // Numbers from about as far away as it can see, taken from Jeff's pool on
    // a very good visibility day.
    //[YELLOW_BOUY] = {0x9C, 0xC8, 0xC7 },
    //[RED_BOUY]    = {0xA3, 0xA3, 0xBB },
    //[GREEN_BOUY]  = {0xD8, 0xCB, 0xCB },

    // Numbers very close, taken from Jeff's pool on a very good visibility
    // day.
    //[YELLOW_BOUY] = {0xD7, 0xDE, 0xB2 },
    //[RED_BOUY]    = {0xAE, 0x83, 0x94 },
    //[GREEN_BOUY]  = {0xAE, 0xE4, 0xCA },

    //[GREEN_BOUY]  = {0x96, 0xBB, 0xC4 },

};

// State Variables for BOUY - First Approach sub routine
static int approach_counter = 0;  //counts how many frames we've seen any blob

// State Variables for BOUY - First Orientation sub routine

// State variables for BOUY - Bump Bouy Sub Routine
static int lost_blob = 0;         //how long it's been since we lost the blob
static int tracking_counter = 0;  //total number of frames we've seen a blob
static int saw_big_blob = 0;      //starts incrementing once we see a big enough blob
static int hit_blob = 0;          //increments for every frame we think we've hit the blob
static int bump_initialized = 0;  //flag to keep track of initializing bump routine
static Timer* bouy_timer = NULL;      //time how long since we first saw the bouy

// State Variables for Bouy - First Backing Up
static Timer* backing_timer = NULL;      //times our backing up step for us

// State Variables for Dead Reakoning At End
double heading;
double target;

// State Variables for Search Pattern For Path
static int search_direction = 0; //which direction we need to turn next (1 or 2)
static int initial_leg_length = 0; //how long our first leg of the search pattern should be
static int search_pattern_turning = 0; //flags we are completing a turn
static int seen_orange_blob = 0; //lets us know if we have found the path
static Timer* search_timer = NULL; //times the legs of our search
static int first_search_leg = 1; //true when we are on our first search leg

RGBPixel find_blob_avg_color(IplImage* img, BLOB* blob);
RGBPixel find_blob_avg_color(IplImage* img, BLOB* blob) {
    unsigned int avg_r = 0;
    unsigned int avg_g = 0;
    unsigned int avg_b = 0;
    CvPoint* pixel = blob->pixels;
    for (int i=0; i<blob->area; i++) {
        avg_r += (unsigned int) img->imageData[img->width*pixel->y + img->height*pixel->x + 2];
        avg_g += (unsigned int) img->imageData[img->width*pixel->y + img->height*pixel->x + 1];
        avg_b += (unsigned int) img->imageData[img->width*pixel->y + img->height*pixel->x + 0];
        pixel++;
    }
    avg_r = avg_r / blob->area;
    avg_g = avg_g / blob->area;
    avg_b = avg_b / blob->area;
    RGBPixel average = {avg_r, avg_g, avg_b};
    return average;
}

void mission_bouy_init(IplImage * frame, struct mission_output* result)
{
    bouy_state = BOUY_STATE_FIRST_APPROACH;
    bouy_bump_init();
    result->depth_control = DEPTH_ABSOLUTE;
    result->depth = 1.5;

    if (search_timer != NULL) {
        Timer_destroy(search_timer);
    }
    search_timer = NULL;
    initial_angle = Var_get("SEA.Yaw");
}

struct mission_output mission_bouy_step (struct mission_output result)
{

    switch (bouy_state) {

        case BOUY_STATE_FIRST_APPROACH:
            //drive forward
            result.rho = 20;

            //scan the image for any of the three bouys
            bouys_found = bouy_first_approach(&result);

            // if we see a bouy, move on
            if(bouys_found){
                printf("we finished the approach \n");
                bouy_state++;
            } else {
                // Don't break if we're going to change states, or we would
                // waste a frame
                break;
            }

        case BOUY_STATE_FIRST_ORIENTATION:
            //turn towards our first bouy
            result.yaw_control = ROT_MODE_RATE;

            if(bouy_order[bouys_found] > bouy_order[BOUY_1]){
                //TURN LEFT
                printf("Going LEFT to desired bouy\n");
                result.rho = 0;
                result.yaw = -1*TURN_RATE;
            }
            else if(bouy_order[bouys_found] < bouy_order[BOUY_1]){
                //TURN RIGHT
                result.rho = 0;
                printf("Going RIGHT to desired bouy\n");
                result.yaw = TURN_RATE;
            }
            else{
                printf("Going STRAIGHT to desired bouy\n");
                //STAY STRAIGHT
            }
            bouy_state++;
            // Move onto next case without a break so that we don't waste a
            // frame

        case BOUY_STATE_BUMP_FIRST_BOUY:

            //initialize bouy bump
            if(bump_initialized == 0){
                bouy_bump_init();
            }

            //run bump routine until complete
            if( bouy_bump(&result, &bouy_colors[BOUY_1]) == 1){
                bouy_state++;
                bump_initialized = 0;
                printf("we finished bouy bump 1 \n");
            }
            break;

        case BOUY_STATE_FIRST_BACKING_UP:

            //back up
            result.rho = -20;
            printf("we are backing up \n");

            //back up for X seconds
            if( backing_timer == NULL){
                backing_timer = Timer_new();
            }else{
                //kill some time
                Util_usleep(0.1);
            }

            if(Timer_getTotal(backing_timer) > BACK_UP_TIME_1){
                //we have backed up long enough
                bouy_state++;
                result.rho = 0;
                printf("We are done backing up \n");
            }

            break;

        case BOUY_STATE_SECOND_ORIENTATION:
            //turn towards our second bouy
            result.yaw_control = ROT_MODE_RATE;

            if(bouy_order[BOUY_2] < bouy_order[BOUY_1]){
                //TURN_LEFT
                result.yaw = -1*TURN_RATE;
                printf("Turning Left, towards the second bouy \n");
            }
            else if(bouy_order[BOUY_2] > bouy_order[BOUY_1]){
                //TURN_RIGHT
                result.yaw = TURN_RATE;
                printf("Turning Right, towards the second bouy \n");
            }
            else{
                printf("Why are we hitting the same bouy twice? really? are we that vindictive? what did that bouy ever do to us?");
            }

            //move on
            bouy_state++;

            break;

        case BOUY_STATE_BUMP_SECOND_BOUY:

            //initialize bouy bump
            if(bump_initialized == 0){
                printf("initializing bump for bouy 2\n");
                bouy_bump_init();
            }

            //run bump routine until complete
            if( bouy_bump(&result, &bouy_colors[BOUY_2]) == 1){
                bouy_state++;
                bump_initialized = 0;
                printf("we finished bouy bump 2 \n");
            }
            break;

        case BOUY_STATE_FINAL_ORIENTATION:
            //determine which direction to turn to turn beyond the obstacle

            if(bouy_order[BOUY_2] == 1){
                //turn right
                result.yaw = TURN_AMOUNT_AFTER_SECOND_BOUY_BUMP;
                search_direction = 1;
                printf("turning right\n");
            }else if(bouy_order[BOUY_2] == 2){
                //arbitrarily turn right
                result.yaw = TURN_AMOUNT_AFTER_SECOND_BOUY_BUMP;
                search_direction = 1;
                printf("turning right\n");
            }else if(bouy_order[BOUY_2]== 3){
                //turn left
                result.yaw = -1*TURN_AMOUNT_AFTER_SECOND_BOUY_BUMP;
                search_direction = -1;
                printf("turning left\n");
            }else{
                printf("BOUY_2 DEFINED INCORRECTLY\n");
            }
            bouy_state++;

        case BOUY_STATE_FINISH_FINAL_TURN_1:

            //if our heading is close enough to
            heading = Var_get("SEA.Yaw");
            target = Var_get("Rot.Angular.Target");
            printf("completing final turn, heading = %f, target = %f \n",heading,target);
            if(fabs(heading-target) < 10){
                printf("finished final turn\n");
                bouy_state++;
            }
            break;

        //case BOUY_STATE_SMALL_DRIVE_1:
            //drive a short ways beyond the obstacle


            bouy_state++;
            break;

        //case BOUY_STATE_TURN_TOWARDS_BOUY:
            //determine which way to turn to orient ourselves

            bouy_state++;
            break;

        //case BOUY_STATE_TURNING_TOWARDS_BOUY:
            //turn towards the bouy being used for orientation

            bouy_state++;
            break;

        //case BOUY_STATE_TURN_FROM_BOUY:
            //set the turn to angle us away from the orientation bouy

            bouy_state++;
            break;

        //case BOUY_STATE_TURNING_FROM_BOUY:
            //turn away from the orientation bouy

            bouy_state++;
            break;

        case BOUY_STATE_SEARCHING_FOR_PATH:
            //perform a search patter to begin looking for the path

            result.yaw_control = ROT_MODE_ANGULAR; 

            if(search_pattern_turning == 0){
                printf("going forward in search\n");
                if( search_timer == NULL){
                    //start a timer
                    search_timer = Timer_new();
                } else if(Timer_getTotal(search_timer) > SEARCH_PATTERN_TIME || 
                          (Timer_getTotal(search_timer) > SEARCH_PATTERN_TIME/2 && bouy_order[BOUY_2] == 2 && first_search_leg ==1) ){
                    //we've been driving long enough
                    Timer_destroy(search_timer);
                    search_timer = NULL;
                    first_search_leg = 0;
                    search_pattern_turning = 1;
                } else {
                    //go forward 
                    result.rho = 10;
                }
            }else if (search_pattern_turning == 1){
                //initiate turn
                result.yaw = (int)(initial_angle + 70 * search_direction+180)%360-180; 
                search_direction *= -1;
                search_pattern_turning = 2;
            }else{
                printf("turning in search\n");
                //continue turning
                result.rho = 5;

                //if our heading is close enough, finish turn
                heading = Var_get("SEA.Yaw");
                target = Var_get("Rot.Angular.Target");

                if(fabs(heading-target) < 10){
                    search_pattern_turning = 0;
                }
            }


            if(/*we see orange XXX */0){
                if(++seen_orange_blob > SEEN_PATH_THRESHOLD){
                    bouy_state++;
                }
            }
            break;

        case BOUY_STATE_COMPLETE:
            result.mission_done = true;
            break;

        default:
            printf("bouy_state set to meaningless value");
            break;
    }

    return result;
}

/**
 * find_closest_blob
 * Takes in n colors and n blobs so that the nth blob corresponds to the nth
 * color.  This function finds which blob it closest to it's target color and
 * returns it.
 *
 * We did not get good results from using this.  It may have bugs in it, or it
 * may just be a bad idea.
 */
int find_closest_blob(int n, RGBPixel colors[], BLOB* blobs[], IplImage* image);
int find_closest_blob(int n, RGBPixel colors[], BLOB* blobs[], IplImage* image) {

    // Gather information about what color blobs we're seeing
    double min_distance = sqrt(255*255*255);
    int closest_blob = 0;
    for (int i=0; i<n; i++) {

        RGBPixel average = find_blob_avg_color(image, blobs[i]);
        double distance = Pixel_stddev(&colors[i], &average);
        if (distance < min_distance) {
            min_distance = distance;
            closest_blob = i;
        }

    }
    return closest_blob;
}

int find_bouy(IplImage* frame, BLOB** found_blob, int* blobs_found_arg, int target_color);
int find_bouy(IplImage* frame, BLOB** found_blob, int* blobs_found_arg, int target_color) {

    int found_bouy = 0;

    IplImage* ipl_out[3];
    ipl_out[0] = cvCreateImage(cvGetSize (frame), 8, 3);
    ipl_out[1] = cvCreateImage(cvGetSize (frame), 8, 3);
    ipl_out[2] = cvCreateImage(cvGetSize (frame), 8, 3);

    int num_pixels[3];
    num_pixels[0] = FindTargetColor(frame, ipl_out[0], &bouy_colors[YELLOW_BOUY], 1, 190, 1);
    num_pixels[1] = FindTargetColor(frame, ipl_out[1], &bouy_colors[RED_BOUY], 1, 190, 1.5);
    num_pixels[2] = FindTargetColor(frame, ipl_out[2], &bouy_colors[GREEN_BOUY], 1, 210, 1.5);

    // Debugs
    cvNamedWindow("Yellow", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("Red", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("Green", CV_WINDOW_AUTOSIZE);
    cvShowImage("Yellow", ipl_out[0]);
    cvShowImage("Red", ipl_out[1]);
    cvShowImage("Green", ipl_out[2]);

    //Look for blobs
    BLOB* blobs[3];
    int blobs_found[3];
    blobs_found[0] = blob(ipl_out[0], &blobs[0], 4, MIN_BLOB_SIZE);
    blobs_found[1] = blob(ipl_out[1], &blobs[1], 4, MIN_BLOB_SIZE);
    blobs_found[2] = blob(ipl_out[2], &blobs[2], 4, MIN_BLOB_SIZE);
    printf("Blobs found: y=%d r=%d g=%d\n", blobs_found[0], blobs_found[1], blobs_found[2]);

    int seen_blob[3];
    BLOB* blobs_seen[3];
    RGBPixel colors_seen[3];
    int indexes_seen[3];
    int num_colors_seen = 0;
    static int max_blob_size = 1000000000;
    for (int i=0; i<3; i++) {
        printf("blobs[%d]->area = %ld\n", i, blobs[i]->area);
        if ((blobs_found[i] == 1 || blobs_found[i] == 2) &&
            blobs[i]->area < max_blob_size &&
            ((float)blobs[i]->area) / ((float)num_pixels[i]) > BLOB_COLOR_FRACTION)
        {
            printf("i=%d\n", i);
            blobs_seen[num_colors_seen] = blobs[i];
            colors_seen[num_colors_seen] = bouy_colors[i+1];
            indexes_seen[num_colors_seen] = i+1;
            num_colors_seen++;
            seen_blob[i] = 1;
        } else {
            printf("Blob amount / Filter amount = %f\n", ((float)blobs[i]->area) / ((float)num_pixels[i]));
            seen_blob[i] = 0;
        }
    }

    // Make a decision baised on how many colors we've seen:
    //  0) We saw nothing
    //  1) The one color we saw is correct
    //  2) Choose the color that's closer to it's target
    //  3) We're getting bad data, assume we saw nothing
    printf("Number of bouys seen: %d\n", num_colors_seen);
    if (num_colors_seen == 1) {
        found_bouy = indexes_seen[0];
    } else if (num_colors_seen == 2) {
        /*
        found_bouy = indexes_seen[
            find_closest_blob(2, colors_seen, blobs_seen, frame)
        ];
        */
        if (blobs_seen[0]->area > blobs_seen[1]->area) {
            found_bouy = indexes_seen[0];
        } else {
            found_bouy = indexes_seen[1];
        }
    } else if (num_colors_seen == 0 || num_colors_seen == 3) {
        //we don't see anything
        found_bouy = 0;
    }

    //free resources
    for (int i=0; i<3; i++) {
        if (i == found_bouy-1) {
            *found_blob = blobs[i];
            *blobs_found_arg = blobs_found[i];
        } else {
            blob_free(blobs[i], blobs_found[i]);
        }
        cvReleaseImage(&ipl_out[i]);
    }

    return found_bouy;
}

/*******      First Approach      ***********/
// Scan Image, if we see a bouy, return it's color.  Otherwise
// return zero.
int bouy_first_approach(struct mission_output* result){

    //obtain frame
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    result->frame = frame;
    frame = normalize_image(frame);

    BLOB* found_blob = NULL;
    int blobs_found = 0;
    int found_bouy = find_bouy(frame, &found_blob, &blobs_found, 0);

    approach_counter++;
    if (found_bouy == YELLOW_BOUY) {
        result->depth_control = DEPTH_RELATIVE;
        result->depth = found_blob->mid.y * DEPTH_SCALE_FACTOR;
        printf("FOUND YELLOW\n");
    } else if (found_bouy == RED_BOUY) {
        result->depth_control = DEPTH_RELATIVE;
        result->depth = found_blob->mid.y * DEPTH_SCALE_FACTOR;
        printf("FOUND RED\n");
    } else if (found_bouy == GREEN_BOUY) {
        result->depth_control = DEPTH_RELATIVE;
        printf("FOUND GREEN\n");
        result->depth = found_blob->mid.y * DEPTH_SCALE_FACTOR;
    } else {
        approach_counter = 0;
    }

    //if we've seen a blob for longer than a threshold, finish
    printf("approch_counter=%d\n", approach_counter);
    if(approach_counter <= APPROACH_THRESHOLD){
        //we haven't seen the blob long enough, keep trying
        found_bouy = 0;
    }

    if (found_blob != NULL) {
        blob_free(found_blob, blobs_found);
    }

    return found_bouy;

}


/*******      Bouy Bump      ***********/

void bouy_bump_init(void){
    //initialize state variables for the bouy_bump routine
    tracking_counter = 0;
    saw_big_blob = 0;
    lost_blob = 0;
    hit_blob = 0;
    if (bouy_timer != NULL) {
        Timer_destroy(bouy_timer);
    }
    bouy_timer = NULL;
    bump_initialized = 1;
}

int bouy_bump(struct mission_output* result, RGBPixel* color){

    int bump_complete = 0;

    //obtain image data
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    frame = normalize_image(frame);
    result->frame = frame;
    int frame_width = frame->width;
    int frame_height = frame->height;

    BLOB* found_blob = NULL;
    int blobs_found = 0;
    int found_bouy = find_bouy(frame, &found_blob, &blobs_found, 0);

    // If we saw the wrong color, ignore it
    if (bouy_colors[found_bouy].r != color->r ||
        bouy_colors[found_bouy].g != color->g ||
        bouy_colors[found_bouy].b != color->b
    ) {
        blobs_found = 0;
    }

    // Determine course
    printf ("tracking_counter = %d\n", tracking_counter);
    CvPoint heading;
    if (blobs_found == 0 || blobs_found > 3) {

        // We don't think what we see is a blob
        if (tracking_counter > 6)
        {
            // We have seen the blob for long enough, we may have hit it
            if (++hit_blob > 2)
            {
                //we have probably hit the blob, so let's look for a marker
                printf("We've missed the blob for a while; assuming we hit it.\n");
                bump_complete = 1;
            }
        }
        // We havn't gotten to it yet, but are pretty sure we saw it once
        else if (tracking_counter > 5)
        {
            //don't udpate yaw heading, head for last place we saw the blob

            if (++lost_blob > 100)
            {
                //Something might be wrong.  Keep looking for the blob though
                printf ("WE LOST THE BLOB!!");
            }
        }
        else
        {
            //we arn't even sure we've seen it, so just stay our current course
            tracking_counter = 0;
        }

    }
    else if (++tracking_counter > 2)
    {
        //we do see a blob
        result->depth_control = DEPTH_RELATIVE;
        result->yaw_control = ROT_MODE_RELATIVE;

        //modify state variables
        hit_blob = 0;
        lost_blob = 0;

        // Update heading
        // We do this only for a few frames to get a good heading
        if (tracking_counter < 15) {
            printf("setting yaw to chase a blob\n");
            heading = found_blob[0].mid;
            result->yaw = heading.x;
            result->depth = heading.y;
            cvCircle(result->frame, cvPoint(result->yaw, result->depth), 5, cvScalar(0,0,0,255),1,8,0);
            //adjust to put the origin in the center of the frame
            result->yaw = result->yaw - frame_width / 2;
            result->depth = result->depth - frame_height / 2;
            result->depth *= DEPTH_SCALE_FACTOR; // Scaling factor
            //subjectively scale output !!!!!!!
            result->yaw = result->yaw / YAW_SCALE_FACTOR; // Scale Output

            //Convert Pixels to Degrees
            result->yaw = PixToDeg(result->yaw);

            // Start moving forward
            result->rho = 20;

            // Init timer
            if (bouy_timer == NULL) {
                bouy_timer = Timer_new();
            }

        }

        //if the blob gets big enough for us to be close, start a countdown
        if(found_blob[0].area > frame_width*frame_height / 4 && saw_big_blob == 0){
            saw_big_blob++;
        }

        if (tracking_counter > MAX_TRACKING_COUNT || saw_big_blob > BIG_BLOB_WAIT)
        {
            result->yaw = 0;
            result->depth = 0;
            result->rho = 0;
            bump_complete = 1;
            printf ("WE ARE AT THE BLOB ^_^ !!!!\n");
        }

    }

    //check big blob countdown
    if(saw_big_blob > 0){
        if(++saw_big_blob > 10){
            result->yaw = 0;
            result->depth = 0;
            result->rho = 0;
            bump_complete = 1;
        }
        printf("saw_big_blob = %d \n", saw_big_blob);
    }
//
//   if (bouy_timer != NULL &&
//        Timer_getTotal(bouy_timer) >= BOUY_BUMP_TIMER)
//    {
///            result->yaw = 0;
//            result->depth = 0;
//            result->rho = 0;
//            bump_complete = 1;
//            printf("It's been a while since we've first seen the blob...\n");
//            printf("  We probably either hit it, or failed, so I'm moving on.\n");
//    }

    //RELEASE THINGS
    if (found_blob != NULL) {
        blob_free (found_blob, blobs_found);
    }
    //cvReleaseImage (&frame);

    return bump_complete;
}
