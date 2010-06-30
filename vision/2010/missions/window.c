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
    [RED_WINDOW]    = 1,
    [BLUE_WINDOW]   = 2,
    [GREEN_WINDOW]  = 3,
    [YELLOW_WINDOW] = 4
}; 

//DEPTH OF THE WINDOW ROWS
#define TOP_ROW_DEPTH 2
#define BOTTOM_ROW_DEPTH 3


//what height to start the robot at
#define INITIAL_DEPTH 2

//how fast to turn when alligning with a window
#define TURN_RATE 5

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
static int window_found = 0; //tracks which window we've seen

//state variable for orientation
static double starting_angle;

void mission_window_init(IplImage* frame, struct mission_output* result)
{

    window_state = WINDOW_STATE_FIRST_APPROACH;
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
            result.rho = 20;

            //scan the image for any of the three bouys
            //window_found = window_first_approach(&result);

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
/*
            //initialize targeting function
            if(window_initialized == 0){
                bouy_bump_init();
            }

            //run bump routine until complete
            if( bouy_bump(&result, &bouy_colors[BOUY_1]) == 1){
                bouy_state++;
                bump_initialized = 0;
                printf("we finished bouy bump 1 \n");
            }else{
                //grab angle data to check how far we have turned
                double current_angle = Var_get("SEA.Yaw");
                if(!(fabs(current_angle-starting_angle) < TURNING_THRESHOLD ||
                    fabs(current_angle-starting_angle) > 360-TURNING_THRESHOLD)){
                        //We have turned too far
                        //result.yaw *= -1;
                        starting_angle = current_angle;
                }
            }*/
            break;

        case FIRE_ZE_MISSILES: 
            //do it. do it now. 
            break;
        
        case WINDOW_STATE_COMPLETE:
            //I guess we are done
            break;

        default:
            printf("window_state SET TO UNDEFINED VALUE\n");
            break;
              
    }
    return result;
}
