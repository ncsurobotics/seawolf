#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#include "mission.h"

//state variables for ALLIGN_PATH
static int on_path=0,xdist,ydist,direction=0;
static double max_measured_rho;
static int path_alligned = 0;
static CvPoint last_heading = {-999,-999};
static int seen_blob = 0;
static int lost_path = 0;
static float last_theta = -999; // Used to keep track of the correct end of the marker


void mission_align_path_init(IplImage* frame)
{
    //state variables for ALLIGN_PATH
    int on_path=0,xdist,ydist,direction=0;
    double max_measured_rho;
    int path_alligned = 0;
    CvPoint last_heading = {-999,-999};
    int seen_blob = 0;
    int lost_path = 0;
    float last_theta = -999; // Used to keep track of the correct end of the marker
}

struct mission_output mission_align_path_step(struct mission_output result)
{
    IplImage* grey;
    IplImage* edge;
    IplImage* ipl_out = NULL;
    RGBPixel color = {0xff, 0x00, 0x00};
    CvSeq* lines;
    IplImage* frame = multicam_get_frame(DOWN_CAM);
    ipl_out = cvCreateImage(cvGetSize(frame),8,3);
    result.frame = frame;

    // Temporary variables for theta,phi,rho
    int theta=result.theta;
    int phi=result.phi;
    int rho=result.rho;

    // Run a color filter on the frame to select the path's color
    int num_pixels = FindTargetColor(frame, ipl_out, &color, 400, 250,3);

    // Run hough transform to look for line
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
        theta = (sin(line[1])*50); //determine how much to turn
        theta = cos(line[1])>0 ? theta : -1*theta; //determine which direction to turn
        // Don't allow theta to jump 180 degrees when the line passes pi/2
        // (which for some reason is 1)
        if(theta < 0){
            theta = fabs(theta-last_theta) < fabs((theta + 50*2) - last_theta) ? theta : theta + 50*2;
        }else{
            theta = fabs(theta-last_theta) < fabs((theta - 50*2) - last_theta) ? theta : theta - 50*2;
        }
        // Store this theta value
        last_theta = theta;
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
            theta = xdist;
            max_measured_rho = sqrt((frame->width/2)*(frame->width/2)+(frame->height/2)*(frame->height/2));
            rho = sqrt(xdist*xdist + ydist*ydist); // Compute estimated distance to target
            if(ydist < 0){
                // If we need to go backwards, change the sign of rho and theta
                theta = -1*theta;
                rho = -1*rho;
            }
            // Scale the rho and theta value
            rho = (rho*MAX_RHO/max_measured_rho);
            theta = (theta*MAX_THETA/(frame->width/2))/6;

            // Decide if this counts as on top of the marker
            if(abs(rho) < MAX_RHO/6) {
                on_path++;
            } else {
                on_path = 0;
            }
            // Don't go charging off until we are pointed at the target
            if(abs(theta) > MAX_THETA/20) rho = 0;

            // Try to aproximate actual distance we need to cover (so scale rho
            // AGAIN)
            rho /=4; // Scaled down additionaly, b/c we will never be more than a few feet off

        }else{
            // We see what might become a blob, so let's initialize last_theta
            // here
            // Only initialize this value once.
            if(last_theta == -999){
                last_theta = (sin(line[1])*50); // Determine how much to turn
                last_theta = cos(line[1])>0 ? last_theta : -1*last_theta; // Determine which direction to turn
            }
        }

    }else{
        // We are now supposing ourselves to be on the marker, and need to
        // orient correctly

        if(blobs_found == 0 || blobs_found>3) { // If we don't see the marker
            // Just wait for it to come back I suppose
            theta = 0;
            lost_path++;

        }else if(line[0] != -999) {
            lost_path=0;

            // Limit theta in case it for some reason overflows (it really
            // shouldn't)
            theta = theta>MAX_THETA ? MAX_THETA:theta;
            theta = theta/6;
            if(fabs(theta)<1.5) {
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
    result.theta = theta;
    result.phi = phi;
    result.rho = rho;

    // Release Resources
    blob_free (blobs, blobs_found);
    cvReleaseImage(&grey);
    cvReleaseImage(&edge);
    cvReleaseImage(&ipl_out);
    cvReleaseMemStorage(&(lines->storage));

    return result;
}
