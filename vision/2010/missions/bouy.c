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

//TODO: 
//      -set depth
//      -mission switching
//      -add debug

// State variables for BOUY (static limits scope to file)
static int lost_blob = 0;
static int tracking_counter = 0;
static int saw_big_blob = 0;
static int hit_blob = 0;        //increments for every frame we think we've hit the blob
static int bouy_state;

// Bouy colors
#define YELLOW 1
#define RED 2
#define GREEN 3

RGBPixel yellow = { 0xff, 0xff, 0x00 };
RGBPixel red = { 0xff, 0x00, 0x00 };
RGBPixel green = { 0x00, 0xff, 0x00 };

// The order that the 3 bouys are in, left to right

// The order to hit the bouys in
#define BOUY_1 (red)
#define BOUY_2 (yellow)

// States for the bouy state machine
#define BOUY_STATE_BOUY_1 1
#define BOUY_STATE_BOUY_2 2
#define BOUY_STATE_BACKING 3

void mission_bouy_init (IplImage * frame)
{
    tracking_counter = 0;
    saw_big_blob = 0;
    lost_blob = 0;
    hit_blob = 0;
    bouy_state = BOUY_STATE_BOUY_1;
}

struct mission_output mission_bouy_step (struct mission_output result)
{
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    result.frame = frame;
    int frame_width = frame->width;
    int frame_height = frame->height;
    RGBPixel color = { 0xff, 0x00, 0x00 };
    result.depth_control = DEPTH_RELATIVE;
    result.yaw_control = ROT_MODE_RELATIVE;

    switch (bouy_state) {

        case BOUY_STATE_BOUY_1:

            // Set some headings
            result.rho = 20;
            
            // Scan image for color
            IplImage* ipl_out;
            ipl_out = cvCreateImage(cvGetSize (frame), 8, 3);
            int num_pixels = FindTargetColor(frame, ipl_out, &color, 1, 350, 1);

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
                        printf
                            ("We've missed the blob for a while; assuming we hit it.\n");
                        bouy_state = BOUY_STATE_BACKING;
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
                    result.yaw = heading.x;
                    result.depth = heading.y;
                    cvCircle(result.frame, cvPoint(result.yaw, result.depth), 5, cvScalar(0,0,0,255),1,8,0);
                    //adjust to put the origin in the center of the frame
                    result.yaw = result.yaw - frame_width / 2;
                    result.depth = result.depth - frame_height / 2;
                    //subjectively scale output !!!!!!! 
                    result.yaw = result.yaw / 3;
                }

                printf ("tracking_counter = %d\n", tracking_counter);
                
                //if the blob gets big enough for us to be close, start a countdown
                if(blobs[0].area > frame_width*frame_height / 4 && saw_big_blob == 0){
                    saw_big_blob++;
                }

                if (tracking_counter > 20 || saw_big_blob > 10)
                {
                    result.yaw = 0;
                    result.depth = 0;
                    result.rho = 0;
                    bouy_state = BOUY_STATE_BACKING;
                    printf ("WE ARE AT THE BLOB ^_^ !!!!\n");
                }

            }
            
            //check big blob countdown 
            if(saw_big_blob > 0){
                if(++saw_big_blob > 10){
                    bouy_state = BOUY_STATE_BACKING;
                }
                printf("saw_big_blob = %d \n", saw_big_blob);
            }

            //RELEASE THINGS 
            blob_free (blobs, blobs_found);
            cvReleaseImage (&ipl_out);

            break;
        /** End Bouy Tracking **/

        case BOUY_STATE_BACKING:
            result.rho = -20;
            break;
        /** End Bouy Backing **/

        default:
            break;
    }
    
    //Convert Pixels to Degrees
    result.yaw = PixToDeg(result.yaw);

    return result;
}
