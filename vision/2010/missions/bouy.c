
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

// Bouy colors from left to right
#define YELLOW_BOUY 1
#define RED_BOUY    2
#define GREEN_BOUY  3

// The order to hit the bouys in
#define BOUY_1 RED_BOUY
#define BOUY_2 YELLOW_BOUY

// States for the bouy state machine
#define BOUY_STATE_FIRST_APPROACH 0
#define BOUY_STATE_FIRST_ORIENTATION 1
#define BOUY_STATE_BUMP_FIRST_BOUY 2
#define BOUY_STATE_FIRST_BACKING_UP 3
#define BOUY_STATE_SECOND_ORIENTATION 4
#define BOUY_STATE_BUMP_SECOND_BOUY 5
#define BOUY_STATE_SECOND_BACKING_UP 6
#define BOUY_STATE_FINAL_ORIENTATION 7
#define BOUY_STATE_COMPLETE 8


// Turn Rate When Searching For Bouys
#define TURN_RATE 5

// How Long To Back Up After 1st Bouy
#define BACK_UP_TIME_1 5

/************* STATE VARIABLES FOR BOUY *************/

// State Variables for Bouy Mission
static int bouy_state = 0;           //Keeps track of primary bouy state machine
static int bouys_found = 0;          //turns to 1,2, or 3 when a bouy is found, # signifies color
static RGBPixel bouy_colors[] = {    //holds the three colors of the bouys
    [YELLOW_BOUY] = {0xff, 0xff, 0x00 },
    [RED_BOUY]    = {0xff, 0x00, 0x00 },
    [GREEN_BOUY]  = {0x00, 0xff, 0x00 },   
};

// State Variables for BOUY - First Approach sub routine

// State Variables for BOUY - First Orientation sub routine

// State variables for BOUY - Bump Bouy Sub Routine
static int lost_blob = 0;         //how long it's been since we lost the blob
static int tracking_counter = 0;  //total number of frames we've seen a blob
static int saw_big_blob = 0;      //starts incrementing once we see a big enough blob
static int hit_blob = 0;          //increments for every frame we think we've hit the blob
static int bump_initialized = 0;  //flag to keep track of initializing bump routine

// State Variables for Bouy - First Backing Up
static Timer* backing_timer = NULL;      //times our backing up step for us


void mission_bouy_init (IplImage * frame)
{
    bouy_state = BOUY_STATE_FIRST_APPROACH;
}

struct mission_output mission_bouy_step (struct mission_output result)
{
    switch (bouy_state) {
        
        case BOUY_STATE_FIRST_APPROACH:
            //drive forward 
            result.rho = 10;
                
            //scan the image for any of the three bouys
            bouys_found = bouy_first_approach();
            
            // if we see a bouy, move on
            if(bouys_found){
                printf("we finished the approach \n");
                bouy_state++;
            }
            break;
            
        case BOUY_STATE_FIRST_ORIENTATION:
            //turn towards our first bouy
            
            if(bouys_found < BOUY_1){
                //TURN LEFT
                result.yaw = -1*TURN_RATE;
            } 
            else if(bouys_found > BOUY_1){
                //TURN RIGHT
                result.yaw = TURN_RATE;
            }
            else{
                //STAY STRAIGHT 
            }
            bouy_state++;
            break;
            
        case BOUY_STATE_BUMP_FIRST_BOUY:
        
            //initialize bouy bump
            if(bump_initialized == 0){
                bouy_bump_init;
            }
            
            //run bump routine until complete
            if( bouy_bump(&result, &bouy_colors[BOUY_1]) == 1){
                bouy_state++;
                bump_initialized = 0;
                printf("we finished bouy bump 1 \n");
            }            
            break;
            
        case BOUY_STATE_FIRST_BACKING_UP:
            
            //back up for X seconds
            if( backing_timer == NULL){
                backing_timer = Timer_new();
            }            
             
            if(Timer_getTotal(backing_timer) > BACK_UP_TIME_1){
                //we have backed up long enough
                bouy_state++;
                printf("We are done backing up \n");
            }            
            break;
            
        case BOUY_STATE_SECOND_ORIENTATION:
            //turn towards our second bouy
            if(BOUY_2 < BOUY_1){
                //TURN_LEFT
                result.yaw = -1*TURN_RATE;
                printf("Turning Left, towards the second bouy");
            }
            else if(BOUY_2 > BOUY_1){
                //TURN_RIGHT
                result.yaw = TURN_RATE;
                printf("Turning Right, towards the second bouy");
            }
            else{
                printf("Why are we hitting the same bouy twice? really? are we that vindictive? what did that bouy ever do to us?");
            }
            break;
            
        case BOUY_STATE_BUMP_SECOND_BOUY:
        
            //initialize bouy bump
            if(bump_initialized == 0){
                bouy_bump_init;
            }
            
            //run bump routine until complete
            if( bouy_bump(&result, &bouy_colors[BOUY_2]) == 1){
                bouy_state++;
                bump_initialized = 0;
                printf("we finished bouy bump 1 \n");
            }         
            break;
            
        default:
            printf("bouy_state set to meaningless value");
            break;
    }
    
    //Convert Pixels to Degrees
    result.yaw = PixToDeg(result.yaw);

    return result;
}


/*******      First Approach      ***********/
// Scan Image, if we see a bouy, return it's color.  Otherwise
// return zero.

int bouy_first_approach(void){
    int found_bouy = 0;
    
    //obtain frame
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    
    //scan image for any of the bouy colors
    IplImage* ipl_out_1;
    ipl_out_1 = cvCreateImage(cvGetSize (frame), 8, 3);
    IplImage* ipl_out_2;
    ipl_out_2 = cvCreateImage(cvGetSize (frame), 8, 3);
    IplImage* ipl_out_3;
    ipl_out_3 = cvCreateImage(cvGetSize (frame), 8, 3);
    
    int num_pixels_1 = FindTargetColor(frame, ipl_out_1, &bouy_colors[YELLOW_BOUY], 1, 350, 1);
    int num_pixels_2 = FindTargetColor(frame, ipl_out_2, &bouy_colors[RED_BOUY], 1, 350, 1);
    int num_pixels_3 = FindTargetColor(frame, ipl_out_3, &bouy_colors[GREEN_BOUY], 1, 350, 1);
    
    //Look for blobs
    BLOB *blobs1;
    int blobs_found1 = blob(ipl_out_1, &blobs1, 4, 100);
    BLOB *blobs2;
    int blobs_found2 = blob(ipl_out_2, &blobs2, 4, 100);
    BLOB *blobs3;
    int blobs_found3 = blob(ipl_out_3, &blobs3, 4, 100);
    
    //if any of these look like a bouy, return the color and we're done
    if((blobs_found1 == 1 || blobs_found1 == 2) && blobs1[0].area > 80){
        //we see a yellow blob
        found_bouy = YELLOW_BOUY;
        printf("We see a yellow blob\n");
    }
    else if((blobs_found2 == 1 || blobs_found2 == 2) && blobs2[0].area > 80){
        //we see a red blob
        found_bouy = RED_BOUY;
        printf("We see a red blob\n");
    }
    else if((blobs_found3 == 1 || blobs_found3 == 2) && blobs3[0].area > 80){
        //we see a green blob
        found_bouy = GREEN_BOUY;
        printf("We see a green blob\n");
    }
    else{
        //we don't see anything
        found_bouy = 0;
    }
    
    //free resources
    blob_free (blobs1, blobs_found1);
    blob_free (blobs2, blobs_found2);
    blob_free (blobs3, blobs_found3);
    cvReleaseImage (&ipl_out_1);
    cvReleaseImage (&ipl_out_2);
    cvReleaseImage (&ipl_out_3);
    
    
    return found_bouy;
}


/*******      Bouy Bump      ***********/

void bouy_bump_init(void){
    //initialize state variables for the bouy_bump routine
    tracking_counter = 0;
    saw_big_blob = 0;
    lost_blob = 0;
    hit_blob = 0;
    bump_initialized = 1;
}

int bouy_bump(struct mission_output* result, RGBPixel* color){

    int bump_complete = 0;

    //obtain image data
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    result->frame = frame;
    int frame_width = frame->width;
    int frame_height = frame->height;
    result->depth_control = DEPTH_RELATIVE;
    result->yaw_control = ROT_MODE_RELATIVE;

    // Set some headings
    result->rho = 20;
    
    // Scan image for color
    IplImage* ipl_out;
    ipl_out = cvCreateImage(cvGetSize (frame), 8, 3);
    int num_pixels = FindTargetColor(frame, ipl_out, color, 1, 350, 1);

    // Find blobs
    BLOB *blobs;
    int blobs_found = blob(ipl_out, &blobs, 4, 100);

    // Determine course
    CvPoint heading;
    if (blobs_found == 0 || blobs_found > 3 ||
         blobs[0].area < (num_pixels * 3 / 4 > 100 ? num_pixels * 3 / 4 : 100))
    {
        // We don't think what we see is a blob
        if (tracking_counter > 10)
        {
            // We have seen the blob for long enough, we may have hit it
            if (++hit_blob > 5)
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
        
        //modify state variables
        hit_blob = 0;
        lost_blob = 0;
        
        // Update heading
        // We do this only for a few frames to get a good heading
        if (tracking_counter < 15) {
            heading = blobs[0].mid;
            result->yaw = heading.x;
            result->depth = heading.y;
            cvCircle(result->frame, cvPoint(result->yaw, result->depth), 5, cvScalar(0,0,0,255),1,8,0);
            //adjust to put the origin in the center of the frame
            result->yaw = result->yaw - frame_width / 2;
            result->depth = result->depth - frame_height / 2;
            //subjectively scale output !!!!!!! 
            result->yaw = result->yaw / 3;
        }

        printf ("tracking_counter = %d\n", tracking_counter);
        
        //if the blob gets big enough for us to be close, start a countdown
        if(blobs[0].area > frame_width*frame_height / 4 && saw_big_blob == 0){
            saw_big_blob++;
        }

        if (tracking_counter > 20 || saw_big_blob > 10)
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
            bump_complete = 1;
        }
        printf("saw_big_blob = %d \n", saw_big_blob);
    }

    //RELEASE THINGS 
    blob_free (blobs, blobs_found);
    cvReleaseImage (&ipl_out);

    return 0;
}
