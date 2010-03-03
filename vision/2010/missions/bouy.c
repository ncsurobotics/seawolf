#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#include "mission.h"

//TODO: 
//      -set depth
//      -mission switching
//      -add debug

// State variables for BOUY (static limits scope to file)
static CvPoint old_heading;
static int lost_blob = 0;
static int tracking_counter = 0;
static int hit_blob = 0;        //increments for every frame we think we've hit the blob

void mission_bouy_init (IplImage * frame)
{
    tracking_counter = 0;
    lost_blob = 0;
    hit_blob = 0;
    old_heading;
}

struct mission_output mission_bouy_step (struct mission_output result)
{
    IplImage* frame = multicam_get_frame (FORWARD_CAM);
    result.frame = frame;
    int frame_width = frame->width;
    int frame_height = frame->height;
    RGBPixel color = { 0xff, 0x00, 0x00 };

    // Set craft speed
    result.rho = 10;

    // Sscan image for color
    IplImage* ipl_out;
    ipl_out = cvCreateImage(cvGetSize (frame), 8, 3);
    int num_pixels = FindTargetColor(frame, ipl_out, &color, 80, 256);

    // Find blobs
    BLOB *blobs;
    int blobs_found = blob(ipl_out, &blobs, 4, 100);

    // Determine course
    CvPoint heading;
    if (blobs_found == 0 || blobs_found > 3 ||
         blobs[0].area < (num_pixels * 3 / 4 > 100 ? num_pixels * 3 / 4 : 100))
    {
        // We don't think what we see is a blob
        // We havn't gotten to it yet, so try to follow the blob off the screen for a short time
        if (tracking_counter > 100)
        {
            // We have seen the blob for long enough, we may have hit it
            if (++hit_blob > 8)
            {
                //we have probably hit the blob, so let's look for a marker
                printf
                    ("We've missed the blob for a while; assuming we hit it.\n");
                result.mission_done = true;
            }
        }
        else if (tracking_counter > 5)
        {
            heading.x =
                (old_heading.x - frame_width / 2) * 7 / 8 + frame_width / 2;
            heading.y =
                (old_heading.y - frame_height / 2) * 7 / 8 + frame_height / 2;
            result.theta = heading.x;
            result.phi = heading.y;
            cvCircle(result.frame, cvPoint(result.theta, result.phi), 5, cvScalar(0,0,0,255),1,8,0);
            //adjust to put the origin in the center of the frame
            result.theta = result.theta - frame_width / 2;
            result.phi = result.phi - frame_height / 2;
            //scale the output, diminishing theta and phi as likelyhood that we are lost increases
            result.phi = -1 * result.phi * MAX_PHI / (frame_height / 2) / 3;
            result.theta = result.theta * MAX_THETA / (frame_width / 2) / 5;

            if (lost_blob > 100)
            {
                //alright, this isn't working, just give up. THIS BIT NEEDS TO BE CHANGED LATTER. CAN'T GIVE UP IN SAN DIEGO
                printf ("WE LOST THE BLOB!!");
                result.theta = 0;
                result.phi = 0;
                result.rho = 0;
            }
            old_heading = heading;
        }
        else
        {
            //we arn't even sure we've seen it, so just stay our current course
            result.phi = 0;
            result.theta = 0;
            tracking_counter = 0;
        }

    }
    else if (++tracking_counter > 2)
    {
        //we do see a blob
        //SEND NOTIFY TO GRANT TRACKING CODE DEPTH CONTROL
        //SeaSQL_setTrackerDoDepth(1.0);
        hit_blob = 0;
        heading = blobs[0].mid;
        result.theta = heading.x;
        result.phi = heading.y;
        cvCircle(result.frame, cvPoint(result.theta, result.phi), 5, cvScalar(0,0,0,255),1,8,0);
        //adjust to put the origin in the center of the frame
        result.theta = result.theta - frame_width / 2;
        result.phi = result.phi - frame_height / 2;
        //scale the output
        result.phi = -1 * result.phi * MAX_PHI / (frame_height / 2) / 3;
        result.theta = result.theta * MAX_THETA / (frame_width / 2) / 5;
        old_heading = heading;
        lost_blob = 0;

        printf ("tracking_counter = %d\n", tracking_counter);
        if (tracking_counter > 500)
        {
            result.theta = 0;
            result.phi = 0;
            result.rho = 0;
            printf ("WE ARE AT THE BLOB ^_^ !!!!\n");
        }
    }

    //RELEASE THINGS 
    blob_free (blobs, blobs_found);
    cvReleaseImage (&ipl_out);

    return result;
}
