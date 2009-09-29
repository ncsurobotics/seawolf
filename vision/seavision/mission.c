/* mission.c
 * The mission code.
 */
#include <seawolf.h>
#include <cv.h>
#include <stdio.h>
#include <highgui.h>
#include <math.h>
#include "vision.h"
//tuna includes
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define DELAY 10

#define MAX_THETA 100
#define MAX_PHI   20
#define MAX_RHO   50

#define PATH_DEPTH 2.0

int mission = 0;

int main(int argc, char** argv)
{

    Seawolf_loadConfig("../../conf/seawolf.conf");
    Seawolf_init("Vision Mission Control");

    // Set filter for seasql notify messages
    Notify_filter(FILTER_ACTION, "GO");

    float theta = 0;
    float phi = 0;
    float rho = 0;

    if (argc == 4) {
        multicam_set_camera(DOWN_CAM,argv[1]);
        multicam_set_camera(FORWARD_CAM,argv[2]);
        multicam_set_camera(UP_CAM,argv[3]);
    } else if (argc == 3) {
        multicam_set_camera(DOWN_CAM,argv[1]);
        multicam_set_camera(FORWARD_CAM,argv[2]);
        multicam_set_camera(UP_CAM,argv[1]);
    } else if (argc == 2) {
        multicam_set_camera(DOWN_CAM,argv[1]);
        multicam_set_camera(FORWARD_CAM,argv[1]);
        multicam_set_camera(UP_CAM,argv[1]);
    } else {
        multicam_set_camera(DOWN_CAM,"0");
        multicam_set_camera(FORWARD_CAM,"0");
        multicam_set_camera(UP_CAM,"0");
    }
    IplImage* frame;

    IplImage* grey;
    IplImage* colorfiltered;
    IplImage* edge;
    IplImage* merged;
    CvSeq* lines;
    BLOB* blobs;
    GRID grid;
    CvPoint heading;
    // TUNA VARIABLES 
    IplImage* ipl_out = NULL;
    Image* rgb_tmp = NULL;
    Image* indexed_tmp = NULL;
    RGBPixel color = {0xff, 0x00, 0x00};


    /* Initialize temporary images */
    frame = multicam_get_frame(FORWARD_CAM);
    multicam_reset_camera();
    int frame_width = frame->width;
    int frame_height = frame->height;
    ipl_out = cvCreateImage(cvSize(frame_width,frame_height), 8, 3);
    rgb_tmp = Image_new(RGB, frame_width, frame_height);
    indexed_tmp = Image_new(INDEXED, frame_width, frame_height);

    // Init Transforms
    hough_opencv_init();
    colorfilter_init();
    blob_init();
    edge_opencv_init();
    remove_edges_init();
    tuna_init();
    blob_motion_init();
    grid_init();

   #ifdef debug_heading
       cvNamedWindow("Heading",CV_WINDOW_AUTOSIZE);
   #endif
   //need this for debugging, but this bit needs to be re-done
   #ifdef debug_controls
       cvNamedWindow("Controls", CV_WINDOW_AUTOSIZE);
   #endif

    //**************************************//
    //  S T A T E    V A R I A B L E S      //
    //**************************************//
 
    //universal state variables
    int i;
    int find_path = 0; //turns to 1 when each mission has been completed enough for the next marker may be sought
    int seen_path = 0; //increments for every frame we think we see a path 
    int blobs_found =0;

    //state variables for GATE
    int WHITE_GATE_FLAG =1; //set to zero to look for black gate
    int close_to_gate =0; //number of consecutive frames we've seen something we think is a gate
    int gate_width =0; //the width of the last gate we saw 
    int frames_since_seen_gate = 0; // Frames since we've seen the gate
    int seen_gate = 0;
    int left_pole = 0;
    int right_pole = frame_width;
    int seen_both_poles = 0; //increments every time we see both poles

    //state variables for BOUEY
    CvPoint old_heading;
    int lost_blob=0;
    int tracking_counter = 0;
    int hit_blob = 0; //increments for every frame we think we've hit the blob

    //state varaibles for BARBED_WIRE
    int left_wire = 0;
    int right_wire = frame_width;
    int seen_wire = 0;
    int wire_counter = 0;
    int under_wire = 0;

   //state variables for BARBED_WIRE_ALLIGN
    float wire1 = -999.0f;
    float wire2 = -999.0f;
    int passed_wire2 = 0;


    //state variableis for TORPEDO
    int close_to_goal = 0;
    CvSeq* white_lines;
    CvSeq* green_vertical_lines;
    CvSeq* green_horizontal_lines;
    float rho_white_pole[2] = {0};
    float rho_vertical_green_pole[2] = {0};
    float rho_horizontal_green_pole[2] = {0};
    float theta_white_pole[2] = {0};
    float theta_vertical_green_pole[2] = {0};
    float theta_horizontal_green_pole[2] = {0};

    //state variables for BOMBING_RUN
    int targets[4] = {0,0,0,0}; //1 signifies target. order: Battleship, Airplane, Factory,Tank
    int on_bin = 0;
    int num_type_found=0;//number of types of bins found
    int balls_left = 2;
    int no_new_bins = 0; //increments for every frame we only see old bins
    double current_angle = -999; //how far away we are from pointing down the bombing-run in the direction we approach it
    int find_new_bin = 1; //turns to 1 when we should ignore what we are on top of and go find a new bin
    int aligning = 0;
    int failed_to_allign = 0;
    int facing_right_way = 0;
    int new_bin_y = 0;


    //state variables for BRIEFCASE
  
    //CAUTION: BRIEFCASE RE-USES ALLIGN_PATH STATE VARIABLES B/C THAT WAS THE FASTEST WAY OF WRITING IT

    //state variables for OCTOGON

    //state variables for ALLIGN_PATH
    int on_path=0,xdist,ydist,direction=0;
    double max_measured_rho;
    int path_alligned = 0; 
    CvPoint last_heading = {-999,-999};
    int seen_blob = 0;
    int lost_path = 0;
    float last_theta = -999; //used to keep track of the correct end of the marker

    //state variables for TUNA_BLOB
    int confidence = 0; //distance between best sigma and average sigma
    int num_pixels = 0; //number of total pixels the color filter detects 

    mission = GATE;

    // Wait for mission go first:
    wait_for_go();

    while (1)
    {

        switch (mission)
        {

            case WAIT:

		frame = multicam_get_frame(FORWARD_CAM);

                //TODO
                break;

            case GATE:
                frame = multicam_get_frame(FORWARD_CAM);
                // Set the depth
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(4.0);
                if(WHITE_GATE_FLAG){ //LOOK FOR WHITE LINES
                    grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);
                    cvCvtColor(frame, grey, CV_BGR2GRAY);
                    edge = edge_opencv(grey, 60,100, 3); //this should be much more lenient than normal
                    edge = remove_edges(frame, edge, 0,0,0,0,0,0); //for now this isn't neccessary, leavin in for debugging
                    lines = hough_opencv(edge, frame, 27, 2, 90,20, 10, 150, 150);
                }else{//LOOK FOR BLACK LINES
                    color.r=0x00;
                    color.g=0x00;
                    color.b=0x00;
                    grey = cvCreateImage(cvGetSize(frame), 8, 1);
                    IplImageToImage(frame, rgb_tmp);
                    num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80, 256);
                    Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                    ImageToIplImage(rgb_tmp, ipl_out);
                    #ifdef debug_tuna
                        cvShowImage("out2", ipl_out);
                    #endif
                    cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
                    edge = edge_opencv(grey, 40, 60, 3);
                    lines = hough_opencv(edge, frame, 24, 2, 90,20, 10, 150, 150);
                }

                //now analyze lines
                int pt_gate[2];
                float rho_gate[2];
                float theta_gate[2];
                for(i=0;i<2;i++){
                    float* line = (float*)cvGetSeqElem(lines,i);
                    rho_gate[i] = line[0];
                    theta_gate[i] = line[1];
                    pt_gate[i] = cos(theta_gate[i])*rho_gate[i];
                }

                //figure out where the gate is
                if(rho_gate[0] != -999){ //we see two lines
                    seen_gate++;
                    seen_both_poles++;
                    frames_since_seen_gate = 0;
                    gate_width = abs(pt_gate[0]-pt_gate[1]);
                    if(abs(frame_width - gate_width) < frame_width / 4)
                        close_to_gate++;   //we are close to the gate
                    else if(abs(frame_width-gate_width) > frame_width/5)
                        close_to_gate = 0; //we arn't close to the gate 

                    //assign values to the left and right poles
                    left_pole = pt_gate[0]<pt_gate[1]?pt_gate[0]:pt_gate[1];
                    right_pole = pt_gate[0]>pt_gate[1]?pt_gate[0]:pt_gate[1];

                    theta = ((pt_gate[0]+pt_gate[1])/2-frame_width/2)/2+frame_width/2; //head towards the middle of the gate
                }else if(rho_gate[1] != -999){//we only see one line
                    seen_gate++;
                    frames_since_seen_gate = 0;

                    //if the line we see is closest to the left pole, turn right, else turn left
                    if(abs((int)pt_gate[1]-left_pole) < abs((int)pt_gate[1]-right_pole)){
                        //we see the left pole
                        printf("I see the left pole!");
                        int difference =  pt_gate[1] - left_pole;
                        right_pole = right_pole + difference;
                        left_pole = pt_gate[1];
                        theta = frame_width/2 + 15;
                    }else{
                        //we see the right pole
                        printf("I see the right pole!");
                        int difference =  pt_gate[1] - right_pole;
                        left_pole = left_pole + difference;
                        right_pole = pt_gate[1];
                        theta = frame_width/2 - 15;
                    }
              
                }else{ //we don't see anything
                    if(++frames_since_seen_gate > 20 && seen_gate > 10){
                        mission = ALLIGN_PATH;
                    }

		    theta = frame_width/2;
                }

                //determine rho
                if(close_to_gate > 3)
                    rho= 15; //low rho
                else
                    rho = 15; //high rho
                
                //scale output 
                theta -= frame_width/2;
                theta = (theta*MAX_THETA / (frame_width/2))/6;
                phi = 0;

                //free resources
                cvReleaseImage(&grey);
                cvReleaseImage(&edge);
                cvRelease((void**) &lines);

                if(WHITE_GATE_FLAG){//free white gate resources
                    colorfilter_free();
                    edge_opencv_free();
                    hough_opencv_free();
                    remove_edges_free();
                }else{//free black gate resources
                    cvReleaseImage(&grey);
                    cvReleaseImage(&edge);
                    cvRelease((void**) &lines);
                    colorfilter_free();
                    edge_opencv_free();
                    hough_opencv_free();
                }

                break;

            case GATE_PATH: 
                frame = multicam_get_frame(DOWN_CAM);
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(4.0);
                //select path color
                color.r = 0xff;
                color.g = 0x88;
                color.b = 0x00;

                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 400, 250);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                #ifdef debug_tuna
                    cvShowImage("out2", ipl_out);
                #endif 
    
                blobs_found = blob(ipl_out,&blobs, 1, (num_pixels/2));
                heading = blobs[0].mid;
                if(heading.y < frame_width/2 && (num_pixels/2) > 600){ //we see what we think is a marker, so let's flag this 
                    if(++seen_path >= 3){
                        mission = ALLIGN_PATH; //alright, this is probably a path, let's line up with it
                        last_heading = heading; //let ALLIGN_PATH know where we think the marker is
                    }
                }else{
                    seen_path = 0; //if we really are over a marker, it's not going to randomly drop out for a frame
                }
                //set our forward speed 
                theta = 0;
                rho = 15;

                blob_free(blobs,blobs_found);
                break;

            case BOUEY:
                frame = multicam_get_frame(FORWARD_CAM);
                //select BOUEY color
                color.r = 0xff;
                color.g = 0x00;
                color.b = 0x00;

                //set craft speed
                rho = 10;

                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80,220);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                #ifdef debug_tuna
                    cvShowImage("out2", ipl_out);
                #endif 
                //find blobs
                blobs_found = blob(ipl_out, &blobs, 4, 100);
    
                if(blobs_found == 0 || blobs_found > 3 || blobs[0].area < (num_pixels*3/4>100?num_pixels*3/4:100)){//we don't think what we see is a blob
                    //we havn't gotten to it yet, so try to follow the blob off the screen for a short time
                    if(tracking_counter > 100){
                        //we have seen the blob for long enough, we may have hit it
                        if(++hit_blob > 8){
                            //we have probably hit the blob, so let's look for a marker
                            printf("We've missed the blob for a while, assuming we hit it.\n");
                            mission = ALLIGN_PATH;
                        }
                    }else if(tracking_counter > 5){
                        heading.x = (old_heading.x-frame_width/2)*7/8+frame_width/2;
                        heading.y = (old_heading.y-frame_height/2)*7/8+frame_height/2;
                        theta=heading.x;
                        phi=heading.y;
                        //adjust to put the origin in the center of the frame
                        theta = theta - frame_width/2;
                        phi = phi - frame_height/2;
                        //scale the output, diminishing theta and phi as likelyhood that we are lost increases
                        phi = -1*phi*MAX_PHI/(frame_height/2)/3;
                        theta = theta*MAX_THETA/(frame_width/2)/5;
        
                        if(lost_blob > 100){//alright, this isn't working, just give up. THIS BIT NEEDS TO BE CHANGED LATTER. CAN'T GIVE UP IN SAN DIEGO
                            printf("WE LOST THE BLOB!!");
                            theta=0;
                            phi=0;
                            rho=0;
                        }
                        old_heading = heading;
                    }else{//we arn't even sure we've seen it, so just stay our current course
                        phi = 0;
                        theta = 0;
                        tracking_counter=0;
                    }

                }else if(++tracking_counter>2){//we do see a blob
                    //SEND NOTIFY TO GRANT TRACKING CODE DEPTH CONTROL
                    SeaSQL_setTrackerDoDepth(1.0);
                    hit_blob = 0;
                    heading = blobs[0].mid;
                    theta = heading.x;
                    phi = heading.y;
                    //adjust to put the origin in the center of the frame
                    theta = theta - frame_width/2;
                    phi = phi - frame_height/2;
                    //scale the output
                    phi = -1*phi*MAX_PHI/(frame_height/2)/3;
                    theta = theta*MAX_THETA/(frame_width/2)/5;
                    old_heading = heading;
                    lost_blob = 0;

                    printf("tracking_counter = %d\n", tracking_counter);
                    if(tracking_counter > 500){
                        theta=0;
                        phi = 0;
                        rho = 0;
                        printf("WE ARE AT THE BLOB ^_^ !!!!");
                        fflush(NULL);
                        mission = ALLIGN_PATH;
                    }
                }
                blob_free(blobs,blobs_found);

                if(find_path == 0) break;

            case BOUEY_PATH:
                //looking for the path after the bouey
                //after jarring ourselves on the bouey, we currently don't have any idea which way to orient once we find the path marker

                //RELEASE DEPTH CONTROL FROM TRACKING CODE, AND SET DEPTH TO PATH-SEARCHING ALTITUDE 
                theta = 0;
                theta = 0;
                rho = 10;
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(PATH_DEPTH);
                //if (fabs(SeaSQL_getDepth()-PATH_DEPTH) < 0.5 )
                    mission = ALLIGN_PATH; //so we will just let allign_path drive us in circles until we see one
                break;
        
            case BARBED_WIRE:
                frame = multicam_get_frame(FORWARD_CAM);
                // Set the depth
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(10.0);

                 frame = multicam_get_frame(FORWARD_CAM);
                //select WIRE color
                color.r = 0x00;
                color.g = 0xff;
                color.b = 0x00;

                //set craft speed
                rho = 15;

                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80,220);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                #ifdef debug_tuna
                    cvShowImage("out2", ipl_out);
                #endif 
                //find blobs
                blobs_found = blob(ipl_out, &blobs, 4, 100);
    
                if(blobs_found == 0 || blobs_found > 3 || blobs[0].area < (num_pixels*3/4>400?num_pixels*1/2:400)){//we don't think what we see is a blob
                    //we havn't gotten to it yet, so try to follow the blob off the screen for a short time
                    if(wire_counter > 50){
                        //we have seen the blob for long enough, we may have hit it
                        if(++under_wire > 8){
                            //we have probably hit the blob, so let's look for a marker
                            printf("We've missed the blob for a while, assuming we hit it.\n");
                            mission = BARBED_WIRE_ALLIGN;
                        }
                    }else if(wire_counter > 5){
                        heading.x = (old_heading.x-frame_width/2)*7/8+frame_width/2;
                        heading.y = (old_heading.y-frame_height/2)*7/8+frame_height/2;
                        theta=heading.x;
                        //adjust to put the origin in the center of the frame
                        theta = theta - frame_width/2;
                        //scale the output, diminishing theta and phi as likelyhood that we are lost increases
                        theta = theta*MAX_THETA/(frame_width/2)/3;
     
                        old_heading = heading;
                    }else{//we arn't even sure we've seen it, so just stay our current course
                        theta = 0;
                        wire_counter=0;
                    }

                }else if(++tracking_counter>2){//we do see a blob
                    //SEND NOTIFY TO GRANT TRACKING CODE DEPTH CONTROL
                    under_wire = 0;
                    heading = blobs[0].mid;
                    theta = heading.x;
                    //adjust to put the origin in the center of the frame
                    theta = theta - frame_width/2;
                    //scale the output
                    theta = theta*MAX_THETA/(frame_width/2)/3;
                    old_heading = heading;
                    lost_blob = 0;

                    printf("wire_counter = %d\n", wire_counter);
                    if(wire_counter > 500){
                        theta=0;
                        phi = 0;
                        rho = 0;
                        printf("WE WENT BY THE WIRE >.<!!!!");
                        fflush(NULL);
                        mission = BARBED_WIRE_ALLIGN;
                    }
                }else{
 		    old_heading = heading;
		}
                blob_free(blobs,blobs_found);

                break;

            case BARBED_WIRE_ALLIGN:
                frame = multicam_get_frame(UP_CAM);

                // Get lines
                grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);
                cvCvtColor(frame, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 100, 150, 3);
                CvSeq* lines = hough_opencv(edge, frame, 25, 1, 0,80, 10, 60, 60);

                float* wire= (float*)cvGetSeqElem(lines,0);
                float numrho = cvRound(((frame_width + frame_height) * 2 + 1)*2);
                // if we see a line, track it
                if(wire[0] != -999){
                    //we see a line
                   if(wire1 == -999){
                        //this is the first time we see a line, so call it wire1
                        wire1 = wire[0];
                    }else if( wire1-wire[0] < numrho/4  && wire2 == -999){
                        //this is probably the same wireas line1
                        wire1 = wire[0];

                    }else{
                       //this is a different wirethan line1
                       wire2 = wire[0];
                       
                       //while we pass the second gate, allign us to the right
                       theta = (cos(wire[1])+M_PI/4)*50;
		       theta = theta * MAX_THETA / 78;
		       theta /= 4;
                    }
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(PATH_DEPTH);
                if (fabs(SeaSQL_getDepth()-PATH_DEPTH) < 0.5 ){
                    mission = ALLIGN_PATH; //align us with the marker we found
		    last_theta = -999.0f;
		}
                    
                }else if(wire2 != -999 && ++passed_wire2 > 3){
                    mission = BARBED_WIRE_PATH;
                }else{
                    //we don't see anything, let's try going straight
		    theta = 0;
                }
                
		//release images 
		cvReleaseImage(&edge);
		cvReleaseImage(&grey);
		hough_opencv_free();
		edge_opencv_free();
                break;


            case BARBED_WIRE_PATH:
                //correct path after barbed wire
                frame = multicam_get_frame(DOWN_CAM);

                //RELEASE DEPTH CONTROL FROM TRACKING CODE, AND SET DEPTH TO PATH-SEARCHING ALTITUDE 
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(PATH_DEPTH);

		//NOW, IF WE SEE AN ORANGE BLOB WITH AN APPROPRIATE HOUGH-LINE, PASS IT ON TO ALLIGN_PATH
                color.r = 0xff;
                color.g = 0x66;
                color.b = 0x00;

		//run color filter looking for orange
                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80, 200);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);

		//find blobs
                blobs_found = blob(ipl_out, &blobs, 3, 100);
		
		//if we see a prominent blob, check hough lines
		if(blobs_found > 0 && blobs_found < 3 && blobs[0].area > 400 && blobs[0].area > num_pixels*2/3){
                    // Get horizontal lines
                    grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);
                    cvCvtColor(frame, grey, CV_BGR2GRAY);
                    edge = edge_opencv(grey, 100, 150, 3);
                    CvSeq* lines = hough_opencv(edge, frame, 25, 1, 0,80, 10, 60, 60);

                    float* line= (float*)cvGetSeqElem(lines,0);

		    //if this line is not close to horizontal, allow allign path to take it away
		    if(sin(line[1]) < M_PI/4){
			//we see a blob who's most prominent line is not pointing a hard left
			mission = ALLIGN_PATH;
		    }
		}


		cvReleaseImage(&grey);
		cvReleaseImage(&edge);
		hough_opencv_free();
                blob_free(blobs,blobs_found);
		edge_opencv_free();
                break;

            case TORPEDO:       
                frame = multicam_get_frame(FORWARD_CAM);
                //select color of torpedo goal NOTE: WE CAN ASSUME WE WILL SEE IT VERY VERY WELL IF IT'S THERE
                color.r = 0x00;
                color.g = 0xff;
                color.b = 0x00;

                grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);

                // Get Green lines
                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80, 200);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 50, 150, 3);
                green_vertical_lines = hough_opencv(edge, frame, 12, 2, 90,15, 10, 60, 60);
                green_horizontal_lines = hough_opencv(edge, frame, 12, 2, 0,15, 10, 60, 60);

                // Get White Line
                edge = edge_opencv(grey, 20, 30, 3);
                white_lines = hough_opencv(edge, frame, 15, 1, 90,15, 10, 60, 60);

                //Analyze green lines
                int x_points[2];//holds x values corresponding to vertical lines
                int y_points[2];//holds y values corresponding to horizontal lines
                int num_vertical=0; //number of vertical lines
                int num_horizontal=0; //number of horizontal lines
                for(i=0;i<2;i++){
                    float* line = (float*)cvGetSeqElem(green_vertical_lines,i);
                    float rho = line[0];
                    float theta = line[1];
                    if(rho != -999){
                        num_vertical++;
                        x_points[i] = cos(theta)*rho;
                    }
                    line = (float*)cvGetSeqElem(green_horizontal_lines,i);
                    rho = line[0];
                    theta = line[1];
                    if(rho != -999){
                        num_horizontal++;            
                        y_points[i] = sin(theta)*rho;
                    }
                }

                //Analyze white line
                int white_x = 0; //holds the x value of the white line
                int num_white = 0;
                for(i=0;i<1;i++){
                    float* line = (float*)cvGetSeqElem(white_lines,i);
                    float rho = line[0];
                    float theta = line[1];
                    if(rho != -999){
                        num_white++;
                        white_x = cos(theta)*rho;
                    }
                }

                //direct the craft
                int rho_fast = 10;
                int rho_slow = 5;

                //if two vertical green lines found
                //set x heading, check to see if we are close
                if(num_vertical == 2){
                    if(abs(x_points[0]-x_points[1]) > frame_width*3/4){//then we are close to the target
                        close_to_goal++;
                    }
                }


                if(close_to_goal>1){
                    //we are close
                    //if we see no vertical lines && no horizontal lines: fire torpedo and look for path (stop swimming)
                    //if we see one vertical line: swim away from it and forward SLOWLY
                    //if we see one horizontal line: swim away from it and forward SLOWLY
                    //swim forward SLOWLY
                    if(num_vertical ==0 && num_horizontal == 0){
                        //FIRE ZE MISSILES!!
                        phi=0;
                        theta=0;
                        rho = 0;
                        find_path = 1;
                    }else{
                        theta = 0;
                        phi = 0;
                        if(num_vertical = 1){
                        //turn away from the line 
                        if(x_points[0] < frame_width/2)
                            theta = -10;
                        else
                            theta = 10;
                        }
                        if(num_horizontal = 1){
                        //turn away from the line 
                        if(y_points[0] < frame_height/2)
                            phi = -10;
                        else
                            phi = 10;
                        }
                        rho = rho_slow;
                    }

                }else{
                    //we arn't close
                    //if we see two horizontal lines: set y value
                    if(num_horizontal == 2){
                        phi = (y_points[0]+y_points[1])/2-frame_height/2;
                    }
                    //if we see two vertical lines: set x value
                    if(num_vertical == 2){
                        theta = (x_points[0]+x_points[1])/2 -frame_width/2;
                    }else if((num_horizontal + num_vertical) == 2){
                        //we see at least two green lines (prob. looking at torpedo) and have high confidence, use blob to set x value
 
                        blobs_found = blob(ipl_out,&blobs, 1, (num_pixels/2));
                        heading = blobs[0].mid;
                        if(heading.x > 0){//we see a blob
                            theta = heading.x;
                            phi = heading.y;
                            theta = theta - frame_width;
                            //adjust to put the origin in the center of the frame
                            phi = phi - frame_height;
                            theta = theta/(frame_width/2);
                        }
                        blob_free(blobs,blobs_found);
                    }else if(num_white == 1){
                        //we see the white line: set x value //when we get close to the goal, we will have a hard time seeing this line
                        theta = white_x - frame_width/2;

                    }
                    //scale theta and phi
                    theta = theta*MAX_THETA/frame_width/2;
                    phi = phi*MAX_PHI/frame_height/2;
                    rho = rho_fast;
                }


                if(find_path == 0) break;

            case TORPEDO_PATH:

		//TURN LEFT UNTIL WE CAN'T SEE THE TARGET ANYMORE: 
		last_theta = M_PI * 3/4;

                mission = ALLIGN_PATH; //align us with the marker we found
                break;


/*        case BOMBING_RUN: 

        //S T E P  1:  P O P U L A T E   T H E   G R I D
            frame = multicam_get_frame(DOWN_CAM);
            grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);

            cvCvtColor(frame, grey, CV_BGR2GRAY);
            edge = edge_opencv(grey, 100, 120, 3); //we want this to be fairly strict, to only get the black-white borders if possible
            for(int i = edge->height * edge->width - 1; i >= edge->height*(edge->width - 10); i--) {
        edge->imageData[i] = 0; //turn bottom of the screen black, b/c sobel was messing up
        }
            lines = hough_opencv(edge, frame, 25,20, 90, 90, 10, 60, 130); //now find all the lines in the image, again being fairly strict
            find_regions(lines,&grid, frame); //TODO:filter incoming lines for largest grid 
            find_bins(&grid, frame); //determine which regions are bins
        combine_bins(&grid, frame); //simply combines adjacent bins, 1 horizontal sweep and 1 vertical sweep
            determine_type(&grid, frame); //determine which type of target each bin is

            //release temporary resources
            cvReleaseImage(&grey);
            cvReleaseImage(&edge);
            cvRelease((void**) &lines);
 
        //done populating grid. all bins and their type have been flagged

        //S T E P 2:  S O R T   T H R O U G H   T H E   B I N S

        int bins_found = 0;
        int types_found[4] = {0};
        int closest_distance = frame_width*frame_width/4+frame_height*frame_height/4;
        CvPoint target = {-1,-1};
        int j,k;
        for(i = 0; i < grid.rows;i++){
        for(j = 0; j < grid.columns;j++){
            if(grid.region[i][j].type != 0){//this region is a bin
            //now increase the number of bins found
            bins_found++;

            //find the middle of this bin
            for(k=0;k<4;k++){
                
                grid.region[i][j].mid.x += grid.region[i][j].pt[k].x;
                grid.region[i][j].mid.y += grid.region[i][j].pt[k].y;
            }
                grid.region[i][j].mid.x /= 4;
            grid.region[i][j].mid.y /= 4;

            int x_dist = grid.region[i][j].mid.x - frame_width/2;
            int y_dist = grid.region[i][j].mid.y - frame_height/2;
            int distance = (x_dist*x_dist)+(y_dist*y_dist);
            //if this is the closest bin, and we haven't already checked it, make this our target bin
            if(types_found[grid.region[i][j].type] == 0 && distance < closest_distance){
                target.x = j;
                target.y = i;
                closest_distance = distance;
            }  
            }
        }
        }
        //done sorting bins. we now know how many bins we see, and which is the closest we havnt' examined yet

        //S T E P 3 :   M O V E   T H E   R O B O T  A P R O P R I A T E L Y

        //if we see no bins, keep going straight
        if(bins_found == 0){
        theta = 0;
        phi = 0;
        rho = 10;
        //if we've already found a bin, start incrementing our we-are-lost counter
        if(num_type_found > 0){
            no_new_bins++;
        }

        //else if we see a new bin, drive on top of it
        }else if(target.x != -1 && target.y != -1){
        //flag that we've found a new bin
        no_new_bins = 0; 
        printf("we are centering on a bin of type %d \n",grid.region[target.y][target.x].type);

        //drive on top of the bin, use allign_path code
                    xdist =  grid.region[target.y][target.x].mid.x - frame->width/2;
                    ydist =  frame->height/2 - grid.region[target.y][target.x].mid.x ;
                    theta =  xdist; 
                    max_measured_rho = sqrt((frame_width/2)*(frame_width/2)+(frame_height/2)*(frame_height/2));
                    rho = sqrt(xdist*xdist + ydist*ydist); //compute estimated distance to target
                    if(ydist < 0){ //if we need to go backwards, change the sign of rho and theta 
                        theta = -1*theta;
                        rho = -1*rho;
                    }
                    //scale the rho and theta value
                    rho = (rho*MAX_RHO/max_measured_rho); 
                    theta = (theta*MAX_THETA/(frame_width/2))/3; 

                    //decide if this counts as on top of the marker
                    if(abs(rho) < MAX_RHO/6) 
                        on_bin++; 
                    else 
                        on_bin = 0; 
                    //don't go charging off until we are pointed at the target
                    if(abs(theta) > MAX_THETA/10) rho = 0; 
        
            //try to aproximate actual distance we need to cover (so scale rho AGAIN)
            rho /=5; //scaled down additionaly, b/c we will never be more than a few feet off
                    phi = 0;
        }   

            //if we are on top of our bin, check to see if it's a target, then mark it as completed
        if(on_bin > 2){
        on_bin = 0;
        num_type_found++;//let the code know that we've found another bin (so it knows when it's on its fourth)

        printf("we are on a bin of type %d \n",grid.region[target.y][target.x].type);

        //mark this bin type as completed
        types_found[grid.region[target.y][target.x].type] = 1; 

        //if we are over a target, drop it and mark the target completed
        if(targets[grid.region[target.y][target.x].type] == 1){
            balls_left--;
            targets[grid.region[target.y][target.x].type] = 0;
            //DROP THE MARKER!!!!!!!!!!!!!! CODE GOES HERE!!!!!!!!!!!!!
            //printf("this is a target bin, so we are dropping a marker\n");
        }
        //else if we are on our third marker, drop something
        else if((num_type_found == 3 && balls_left == 2) || num_type_found == 4){
           //printf("we are running our of possible markers, so we are dropping the ball anywas)");
           balls_left--;
           //DROP THE MARKER!!! CODE GOES HERE
        }
        } 

        //if we have filled both targets, or are out of balls, consider ourselves done
        if(!(targets[0] || targets[1] || targets[2] || targets[3]) || balls_left == 0){ 
        //hand the robot over to acoustics, set the mission as done
        }

            //if we don't see any new bins, only old bins, let's think about giving up
        if(bins_found > 0 && target.x == -1 && target.y == -1 ){
        ++no_new_bins;
        }
        if(no_new_bins > 1){ //we might just be having some fluke, let's just hope we see something
            theta=0;
            phi = 0;
                rho = 0; 
        }
        if(no_new_bins > 6){ //okay, still lost, let's try turning
            theta = 10;
            phi = 0;
            rho = 0;
        }
        if(no_new_bins > 20){ //alright, we really have no clue, try to give up
            //hand the robot over to acoustics, set the mission to done
        }

        //done moving the robot to where it needs to go
        
        //S T E P 4 :  R E L E A S E   R E S O U R C E S 
        
            if(grid.rows*grid.columns != 0){
                for(i=0;i<grid.rows;i++)
                    cvFree(&(grid.region[i]));
                cvFree(&(grid.region));
            }

            if(find_path == 0) break;
        
        case BOMBING_RUN_PATH:
            mission = ALLIGN_PATH; //align us with the marker we found
            break;
*/

            case BOMBING_RUN_2: 

                //S T E P  1:  P O P U L A T E   T H E   G R I D
                frame = multicam_get_frame(DOWN_CAM);
                grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);

                cvCvtColor(frame, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 100, 120, 3); //we want this to be fairly strict, to only get the black-white borders if possible
                lines = hough_opencv(edge, frame, 25,20, 90, 90, 10, 60, 130); //now find all the lines in the image, again being fairly strict
                find_regions(lines,&grid, frame); //TODO:filter incoming lines for largest grid 
                find_bins(&grid, frame); //determine which regions are bins
                combine_bins(&grid, frame); //simply combines adjacent bins, 1 horizontal sweep and 1 vertical sweep

                //release temporary resources
                cvReleaseImage(&grey);
                cvReleaseImage(&edge);
                cvRelease((void**) &lines);
     
                //done populating grid. all bins and their type have been flagged

                //S T E P 2:  S O R T   T H R O U G H   T H E   B I N S

                int bins_found = 0;
                int closest_distance = frame_width*frame_width/4+frame_height*frame_height/4;
                CvPoint target = {-1,-1};
                int j,k;
                for(i = 0; i < grid.rows;i++){
                    for(j = 0; j < grid.columns;j++){
                        if(grid.region[i][j].type != 0){//this region is a bin
                            //now increase the number of bins found
                            bins_found++;

                            //find the middle of this bin
                            for(k=0;k<4;k++){
                                
                                grid.region[i][j].mid.x += grid.region[i][j].pt[k].x;
                                grid.region[i][j].mid.y += grid.region[i][j].pt[k].y;
                            }
                            grid.region[i][j].mid.x /= 4;
                            grid.region[i][j].mid.y /= 4;

                            int x_dist = grid.region[i][j].mid.x - frame_width/2;
                            int y_dist = grid.region[i][j].mid.y - frame_height/2;
                            int distance = (x_dist*x_dist)+(y_dist*y_dist);
                            printf("find_new_bin = %d y_dist = %d       mid.y = %d, new_bin_y = %d \n",find_new_bin,y_dist,grid.region[i][j].mid.y,new_bin_y);
                            //if this is the closest bin, and it's in front of us, make this our target bin
                            if(distance < closest_distance && (y_dist < -30 || find_new_bin == 0) && 
                              (grid.region[i][j].mid.y < new_bin_y + 60 || find_new_bin ==1)){
                                target.x = j;
                                target.y = i;
                                closest_distance = distance;
                            }  
                        }
                    }
                }
                //done sorting bins. we now know how many bins we see, and which is the closest we havnt' examined yet

                //S T E P 3 :   M O V E   T H E   R O B O T  A P R O P R I A T E L Y


                //if we see no bins, keep going straight
                if(bins_found == 0){
                    theta = 0;
                    phi = 0;
                    rho = 10;
                    //if we've already found a bin, start incrementing our we-are-lost counter
                    if(num_type_found > 0){
                        no_new_bins++;
                    }

                //else if we see a new bin, drive on top of it
                }else if(target.x != -1 && target.y != -1){
                    //flag that we've found a new bin
                    no_new_bins = 0; 
                    find_new_bin = 0;
                    printf("we are centering on a bin \n");
                    new_bin_y = grid.region[target.y][target.x].mid.y;

                    //--ENTER ANGLE TRACKING CODE HERE--
                    //determine a long leg of the box 
                    int a=0,b;
                    int dist[2] = {0};
                    for(i=1;i<=2;i++){
                        int x_temp = grid.region[target.y][target.x].pt[0].x - grid.region[target.y][target.x].pt[i].x;
                        int y_temp = grid.region[target.y][target.x].pt[0].y - grid.region[target.y][target.x].pt[i].y;
                        dist[i-1] = sqrt(x_temp*x_temp + y_temp*y_temp);
                    }
                    b = dist[0]>dist[1]?1:2; 
            
                    //now find a vertical leg of the relavant triangle
                    int y_leg = grid.region[target.y][target.x].pt[a].y - grid.region[target.y][target.x].pt[b].y;
                    y_leg = grid.region[target.y][target.x].pt[a].x < grid.region[target.y][target.x].pt[b].x ? y_leg:-1*y_leg;  
                    
                    //flag our starting angle, assuming the target angle is the closest vertical orientation
                    if( current_angle == -999){
                        int y_leg = grid.region[target.y][target.x].pt[a].y - grid.region[target.y][target.x].pt[b].y;
                        current_angle = asin((float)y_leg/(float)dist[b-1]);
                    }else{
                        //now decide if theta or theta+pi is the closest to current angle.  assign this to our current angle
                        double theta = asin((float)y_leg/(float)dist[b-1]);
                        if(theta<0){
                            current_angle = fabs(current_angle-theta)<fabs(current_angle-(theta+M_PI))?theta:theta+M_PI;
                        }else{
                            current_angle = fabs(current_angle-theta)<fabs(current_angle-(theta-M_PI))?theta:theta-M_PI;
                        }
                    }
                    printf("current_angle = %f\n",current_angle);
                    //--DONE WITH ANGLE TRACKNG CODE--

                    //drive on top of the bin, use allign_path code
                    xdist =  grid.region[target.y][target.x].mid.x - frame->width/2;
                    ydist =  frame->height/2 - grid.region[target.y][target.x].mid.y;
                    theta =  xdist; 
                    max_measured_rho = sqrt((frame_width/2)*(frame_width/2)+(frame_height/2)*(frame_height/2));
                    rho = sqrt(xdist*xdist + ydist*ydist); //compute estimated distance to target
                    if(ydist < 0){ //if we need to go backwards, change the sign of rho and theta 
                        theta = -1*theta;
                        rho = -1*rho;
                    }
                    //scale the rho and theta value
                    rho = (rho*MAX_RHO/max_measured_rho);
                    theta = (theta*MAX_THETA/(frame_width/2))/3;

                    //decide if this counts as on top of the marker
                    if(abs(rho) < MAX_RHO/6)
                        on_bin++;
                    else 
                        on_bin = 0;
                    //don't go charging off until we are pointed at the target
                    if(abs(theta) > MAX_THETA/10) rho = 0;
                
                    //try to aproximate actual distance we need to cover (so scale rho AGAIN)
                    rho = rho/3; //scaled down additionaly, b/c we will never be more than a few feet off
                    phi = 0;
                }

                //if we are on top of our bin, check to see if it's a target, then mark it as completed
                if(on_bin > 2 && aligning == 0){
                    on_bin = 0;
                    num_type_found++;//let the code know that we've found another bin (so it knows when we are on our fourth/third)
                    aligning = 1;    

                    //determine_type(&grid, frame); //determine which type of target each bin is
                    printf("we are on a bin of type %d \n",grid.region[target.y][target.x].type);

                    //if we are over a target, drop it and mark the target completed
                    if(targets[grid.region[target.y][target.x].type] == 1){
                        balls_left--;
                        targets[grid.region[target.y][target.x].type] = 0;
                        //DROP THE MARKER!!!!!!!!!!!!!! CODE GOES HERE!!!!!!!!!!!!!
                        //printf("this is a target bin, so we are dropping a marker\n");
                    } else if((num_type_found == 3 && balls_left == 2) || num_type_found == 4){
                        //else if we are on our third marker, drop something
                        //printf("we are running our of possible markers, so we are dropping the ball anywas)");
                        balls_left--;
                        //DROP THE MARKER!!! CODE GOES HERE
                    }
                }
                if(aligning == 1 && target.x != -1 && target.y != -1){
                    phi = 0;
                    rho = (frame_height/2 - grid.region[target.y][target.x].mid.y);
                    //scale rho
                    rho = rho*MAX_RHO/(frame_height/2);
                    //assign theta
                    theta = -1*current_angle*MAX_THETA/M_PI;
                    //reduce rho and theta FINE TUNE VALUES HERE I SUPPOSE
                    rho = rho/5;
                    theta = theta/4;

                    if(fabs(current_angle) < .1 && facing_right_way++ > 5 ){
                        facing_right_way = 0;
                        printf("we are moving on to a new bin\n");
                        find_new_bin = 1; //we are ready to look for a new bin
                        aligning = 0;
                    }
                    failed_to_allign = 0;
                }else if(aligning == 1 && failed_to_allign++>5){
                    //alright, we lost something, let's just try driving forward and looking for a new bin
                    failed_to_allign = 0;
                    find_new_bin = 1;
                }

                //if we have filled both targets, or are out of balls, consider ourselves done
                if(!(targets[0] || targets[1] || targets[2] || targets[3]) || balls_left == 0){ 
                    //hand the robot over to acoustics, set the mission as done
                }

                //if we don't see any new bins, only old bins, let's think about giving up
                if(bins_found > 0 && target.x == -1 && target.y == -1 ){
                    ++no_new_bins;
                }
                if(no_new_bins > 1){ //we might just be having some fluke, let's just hope we see something
                    theta=0;
                    phi = 0;
                    rho = 10; 
                }
                if(no_new_bins > 10){ //okay, still lost, let's try turning
                    theta = 10;
                    phi = 0;
                    rho = 0;
                }
                if(no_new_bins > 40){ //alright, we really have no clue, try to give up
                    //hand the robot over to acoustics, set the mission to done
                }

                //done moving the robot to where it needs to go
                
                //S T E P 4 :  R E L E A S E   R E S O U R C E S 
                
                    if(grid.rows*grid.columns != 0){
                        for(i=0;i<grid.rows;i++)
                            cvFree(&(grid.region[i]));
                        cvFree(&(grid.region));
                    }

                    if(find_path == 0) break;
        
            case BOMBING_RUN_2_PATH:
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(PATH_DEPTH);
                if (fabs(SeaSQL_getDepth()-PATH_DEPTH) < 0.5 )
                    mission = ALLIGN_PATH; //align us with the marker we found
                break;


            case BRIEFCASE:
                frame = multicam_get_frame(DOWN_CAM);
                find_path = 0; //reset state variable
                color.r = 0xff; //select path color
                color.b = 0x00;
                color.g = 0x33;

                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(6);
            
                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 400, 350);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                #ifdef debug_tuna
                    cvShowImage("out2", ipl_out);
                #endif 

                //run hough transform to look for line             
                grey = cvCreateImage(cvGetSize(frame), 8, 1);
                cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 50, 200, 3);
                lines = hough_opencv(edge, frame, 25, 1, 90, 90, 10, 60, 60);
                float* line = (float*)cvGetSeqElem(lines,0);

                //if we've seen a blob, keep track of the angle
                if(last_theta != -999 && line[0] != -999){
                        theta = cos(line[1])*50; //determine how much to turn
                    //don't allow theta to jump 180 degrees when the line passes pi/2 (which for some reason is 1)
                        if(theta < 0){
                   theta = fabs(theta-last_theta) < fabs((theta + 50*2) - last_theta) ? theta : theta + 50*2;
                    }else{
                   theta = fabs(theta-last_theta) < fabs((theta - 50*2) - last_theta) ? theta : theta - 50*2;
                    }
                //store this theta value
                    last_theta = theta; 
                }

                //look for multiple blobs (6) if we see more than two, assume we arn't getting a solid color filter reading
                blobs_found = blob(ipl_out, &blobs, 6, 100);
                heading = blobs[0].mid;
                if(on_path < 6){

                    if(blobs_found == 0 || blobs_found>5 || blobs[0].area < (num_pixels/6>500?num_pixels/6:500) || line[0] == -999){//we don't see a blob
                        seen_blob = 0;
                        if(last_heading.x == -999 && last_heading.y == -999){ //we have no clue where the marker is
                              rho = 10;
                            theta = 10;
                            phi = 0;
                        }else if(last_heading.y < frame_height/2){
                            rho = 10;
                            theta = 0;
                            phi = 0;
                        }else{
                            rho = -10;
                            theta = 0;
                            phi = 0;
                        }
                    }else if( ++seen_blob>3){
                        fflush(NULL);
                        //we see a blob, lets try and track it
                        phi = 0;
                        xdist =  heading.x - frame->width/2;
                        ydist =  frame->height/2 - heading.y ;
                        theta =  xdist; 
                        max_measured_rho = sqrt((frame_width/2)*(frame_width/2)+(frame_height/2)*(frame_height/2));
                        rho = sqrt(xdist*xdist + ydist*ydist); //compute estimated distance to target
                        if(ydist < 0){ //if we need to go backwards, change the sign of rho and theta 
                            theta = -1*theta;
                            rho = -1*rho;
                        }
                        //scale the rho and theta value
                        rho = (rho*MAX_RHO/max_measured_rho); 
                        theta = (theta*MAX_THETA/(frame_width/2))/3; 

                        //decide if this counts as on top of the marker
                        if(abs(rho) < MAX_RHO/6) 
                            on_path++; 
                        else 
                            on_path = 0; 
                        //don't go charging off until we are pointed at the target
                        if(abs(theta) > MAX_THETA/20) rho = 0; 
        
                        //try to aproximate actual distance we need to cover (so scale rho AGAIN)
                        rho /=4; //scaled down additionaly, b/c we will never be more than a few feet off

                    }else{ 
                        //we see what might become a blob, so let's initialize last_theta here
                        //only initialize this value once. 
                        if(last_theta == -999){
                            last_theta = (sin(line[1])*50); //determine how much to turn
                            last_theta = cos(line[1])>0 ? last_theta : -1*last_theta; //determine which direction to turn
                        }
                    }

                }else{ //we are now supposing ourselves to be on the marker, and need to orient correctly

                    if(blobs_found == 0 || blobs_found>3){//if we don't see the marker
                        //just wait for it to come back I suppose
                        theta = 0;
                        lost_path++;

                    }else if(line[0] != -999){
                        lost_path=0;

                        //limit theta in case it for some reason overflows (it really shouldn't)
                        theta = theta>MAX_THETA ? MAX_THETA:theta;
                        theta = theta/2;
                        if(abs(theta)<2) path_alligned++;
                        else path_alligned=0; //only consecutive counts
                        if(path_alligned>10) {
                            //we have just completed a task and can start the next one, beginning with bringing craft to correct altitude
                            //SET NEW MISSION DEPTH, THEN MOVE FORWARD OFF PATH MARKER
                            theta = 0;
                            printf("we are above the briefcase\n");
                            fflush(NULL);
                            // Reset our state variables so they don't conflict when we run allign path again
                            int on_path=0,xdist,ydist,direction=0;
                            double max_measured_rho;
                            int path_alligned = 0; 
                            CvPoint last_heading = {-999,-999};
                            int seen_blob = 0;
                            int lost_path = 0;
                            float last_theta = -999; //used to keep track of the correct end of the marker
                            mission = BRIEFCASE_GRAB;
                        }
                        //now set the rho (we do still want to try to stay centered, and y is the easy direction
                        rho = ((frame_height/2-heading.y)*MAX_RHO/(frame_height/2))/4; 
                        //make sure the path isn't horribly off the screen in the x direction. if it is, fall back to centering ourselves   
                        if(abs(heading.x-frame_width/2)>(frame_width/2)*3/4){
                            printf("GOD DAMNIT I'M LOOSING THE BLOODY MARKER, NOW I HAVE TO GO GET  BACK ON TOP OF IT");
                            fflush(NULL);
                            on_path=0;
                        }
                    } else { //we see a blob but not a line, so it's prob. not our blob
                        theta = 0;
                        lost_path++;
                    }
                    if(lost_path>4){//we deffinetly lost the path so let's go find it again
                        lost_path=0;
                        on_path=0;
                    }
                    phi = 0; //we don't want to go up or down

                    cvReleaseImage(&edge);
                    cvReleaseImage(&grey);
                    cvRelease((void**) &lines);
                }
                if(frame_width*frame_height / 5 >num_pixels && ++seen_blob>4){ 
                    last_heading = heading;
                }
                blob_free(blobs,blobs_found);
                //printf("Rho = %f, theta = %f\n",rho,theta);
                //fflush(NULL);
                //cvReleaseImage(&ipl_out);
                break;

	    case BRIEFCASE_GRAB:

		//descend for some time, then decide we are done
                SeaSQL_setTrackerDoDepth(0.0);
                SeaSQL_setDepthHeading(13);
                if (SeaSQL_getDepth() < 9 ){
		    SeaSQL_setDepthHeading(8);
                    mission = mission_done(); //align us with the marker we found
		    last_theta = -999.0f;
		}
		
		break;


            case ALLIGN_PATH:
                frame = multicam_get_frame(DOWN_CAM);
                find_path = 0; //reset state variable
                color.r = 0xff; //select path color
                color.b = 0xff;
                color.g = 0xff;

            
                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 400, 250);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                #ifdef debug_tuna
                    cvShowImage("out2", ipl_out);
                #endif 

                //run hough transform to look for line             
                grey = cvCreateImage(cvGetSize(frame), 8, 1);
                cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 50, 200, 3);
                lines = hough_opencv(edge, frame, 25, 1, 90, 90, 10, 60, 60);
                line = (float*)cvGetSeqElem(lines,0);

                //if we've seen a blob, keep track of the angle
                if(last_theta != -999 && line[0] != -999){
                        theta = (sin(line[1])*50); //determine how much to turn
                        theta = cos(line[1])>0 ? theta : -1*theta; //determine which direction to turn
                    //don't allow theta to jump 180 degrees when the line passes pi/2 (which for some reason is 1)
                        if(theta < 0){
                   theta = fabs(theta-last_theta) < fabs((theta + 50*2) - last_theta) ? theta : theta + 50*2;
                    }else{
                   theta = fabs(theta-last_theta) < fabs((theta - 50*2) - last_theta) ? theta : theta - 50*2;
                    }
                //store this theta value
                    last_theta = theta;
                }

                //look for multiple blobs (3) if we see more than two, assume we arn't getting a solid color filter reading
                blobs_found = blob(ipl_out, &blobs, 4, 100);
                heading = blobs[0].mid;
                if(on_path < 6){
                    printf("we are centering ourselves\n");
                    if(blobs_found == 0 || blobs_found>3 || blobs[0].area < (num_pixels*4/5>1000?num_pixels*4/5:1000) || line[0] == -999){//we don't see a blob
                        seen_blob = 0;
                        if(last_heading.x == -999 && last_heading.y == -999){ //we have no clue where the marker is
                              rho = 10;
                            theta = 0;
                            phi = 0;
                        }else if(last_heading.y < frame_height/2){
                            rho = 10;
                            theta = 0;
                            phi = 0;
                        }else{
                            rho = -10;
                            theta = 0;
                            phi = 0;
                        }
                    }else if( ++seen_blob>3){
                        fflush(NULL);
                        //we see a blob, lets try and track it
                        phi = 0;
                        xdist =  heading.x - frame->width/2;
                        ydist =  frame->height/2 - heading.y ;
                        theta =  xdist; 
                        max_measured_rho = sqrt((frame_width/2)*(frame_width/2)+(frame_height/2)*(frame_height/2));
                        rho = sqrt(xdist*xdist + ydist*ydist); //compute estimated distance to target
                        if(ydist < 0){ //if we need to go backwards, change the sign of rho and theta 
                            theta = -1*theta;
                            rho = -1*rho;
                        }
                        //scale the rho and theta value
                        rho = (rho*MAX_RHO/max_measured_rho); 
                        theta = (theta*MAX_THETA/(frame_width/2))/6; 

                        //decide if this counts as on top of the marker
                        if(abs(rho) < MAX_RHO/6) 
                            on_path++; 
                        else 
                            on_path = 0; 
                        //don't go charging off until we are pointed at the target
                        if(abs(theta) > MAX_THETA/20) rho = 0; 
        
                        //try to aproximate actual distance we need to cover (so scale rho AGAIN)
                        rho /=4; //scaled down additionaly, b/c we will never be more than a few feet off

                    }else{ 
                        //we see what might become a blob, so let's initialize last_theta here
                        //only initialize this value once. 
                        if(last_theta == -999){
                            last_theta = (sin(line[1])*50); //determine how much to turn
                            last_theta = cos(line[1])>0 ? last_theta : -1*last_theta; //determine which direction to turn
                        }
                    }

                }else{ //we are now supposing ourselves to be on the marker, and need to orient correctly

                    if(blobs_found == 0 || blobs_found>3){//if we don't see the marker
                        //just wait for it to come back I suppose
                        theta = 0;
                        lost_path++;

                    }else if(line[0] != -999){
                        lost_path=0;

                        //limit theta in case it for some reason overflows (it really shouldn't)
                        theta = theta>MAX_THETA ? MAX_THETA:theta;
                        theta = theta/6;
                        if(fabs(theta)<1.5) path_alligned++;
                        else path_alligned=0; //only consecutive counts
                        if(path_alligned>10) {
                            //we have just completed a task and can start the next one, beginning with bringing craft to correct altitude
                            //SET NEW MISSION DEPTH, THEN MOVE FORWARD OFF PATH MARKER
                            theta = 0;
                            printf("we are alligned\n");
                            fflush(NULL);
                            // Reset our state variables so they don't conflict when we run allign path again
                            int on_path=0,xdist,ydist,direction=0;
                            double max_measured_rho;
                            int path_alligned = 0; 
                            CvPoint last_heading = {-999,-999};
                            int seen_blob = 0;
                            int lost_path = 0;
                            float last_theta = -999; //used to keep track of the correct end of the marker
                            mission = mission_done();
                        }
                        //now set the rho (we do still want to try to stay centered, and y is the easy direction
                        rho = ((frame_height/2-heading.y)*MAX_RHO/(frame_height/2))/4; 
                        //make sure the path isn't horribly off the screen in the x direction. if it is, fall back to centering ourselves   
                        if(abs(heading.x-frame_width/2)>(frame_width/2)*3/4){
                            printf("GOD DAMNIT I'M LOOSING THE BLOODY MARKER, NOW I HAVE TO GO GET  BACK ON TOP OF IT");
                            fflush(NULL);
                            on_path=0;
                        }
                    } else { //we see a blob but not a line, so it's prob. not our blob
                        theta = 0;
                        lost_path++;
                    }
                    if(lost_path>4){//we deffinetly lost the path so let's go find it again
                        lost_path=0;
                        on_path=0;
                    }
                    phi = 0; //we don't want to go up or down

                    cvReleaseImage(&edge);
                    cvReleaseImage(&grey);
                    cvRelease((void**) &lines);
                }
                if(frame_width*frame_height / 5 >num_pixels && ++seen_blob>4){ 
                    last_heading = heading;
                }
                blob_free(blobs,blobs_found);
                //printf("Rho = %f, theta = %f\n",rho,theta);
                //fflush(NULL);
                //cvReleaseImage(&ipl_out);
                break;

            case IDENTIFY_SILHOUET: //INCOMPLETE - this is the testing version of BOMBING_RUN
                frame = multicam_get_frame(DOWN_CAM);
                grey = cvCreateImage(cvSize(frame_width,frame_height), 8, 1);

                //int targets[] = {0,0,0,0}; //1 signifies target. order: Battleship, Airplane, Factory,Tank
                cvCvtColor(frame, grey, CV_BGR2GRAY);
                edge = edge_opencv(grey, 80, 100, 3); //we want this to be fairly strict, to only get the black-white borders
                for(int i = edge->height * edge->width - 1; i >= edge->height*(edge->width - 10); i--) {
                    edge->imageData[i] = 0; //turn everything black (white, so we can see)
                }
                cvShowImage("Heading",edge);
                lines = hough_opencv(edge, frame, 100,20, 90, 90, 10, 50, 100); //now find all the lines in the image, again being fairly strict
                find_regions(lines,&grid, frame); //TODO:filter incoming lines & correct verticle case / look into odd lagg
                find_bins(&grid, frame); //determine which regions are bins
                determine_type(&grid, frame); //determine which type of target each bin is

                //flag all regions that are a target (need to be dropped)
                //if at least 1 target drive towards the target
                //if we are on the target, but target is too small, swim down
                //if we are on target of suitable size, drop ball, remove target
                //if at least 1 bin, drive towards the closest bin (anything behind is further than anything infront)
                //if we are on the only bin, follow the shortest edge in the direction we are facing
                //this should gaurantee to eventually drop both targets, once 2nd target dropped, then idk what
           
                cvReleaseImage(&grey);
                cvReleaseImage(&edge);
                cvRelease((void**) &lines);
                if(grid.rows*grid.columns != 0){
                    for(i=0;i<grid.rows;i++)
                        cvFree(&(grid.region[i]));
                    cvFree(&(grid.region));
                }
                break;

            case TUNA_BLOB: 
                frame = multicam_get_frame(FORWARD_CAM);
                //select pathcolor
                color.r = 0xff;
                color.g = 0x33;
                color.b = 0x00;

                IplImageToImage(frame, rgb_tmp);
                num_pixels = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80,220);
                Image_indexedToRGB(indexed_tmp, rgb_tmp); 
                ImageToIplImage(rgb_tmp, ipl_out);
                #ifdef debug_tuna
                    cvShowImage("out2", ipl_out);
                #endif 
                //find blobs

                blobs_found = blob(ipl_out, &blobs, 10, 60);
                if(blobs_found > 0){//we see a blob
                    heading = blobs[0].mid;
                    theta = heading.x;
                    phi = heading.y;
                    theta = theta - frame_width/2;
                    //adjust to put the origin in the center of the frame
                    phi = phi - frame_height;
                    //theta = theta/(frame_width/2);
                    //scale the output
                    phi = phi*MAX_PHI/(frame_height/2)/3;
                    theta = theta*MAX_THETA/(frame_width/2)/3;
                }
                blob_free(blobs,blobs_found);
                rho = 5;
                break;

	    case MOTION:
		//run our motion-tracking algorithms
                frame = multicam_get_frame(DOWN_CAM);

		blob_motion(frame);

		break;

        }

       //  Code to test Chris's theta zero/non-zero switching
        //if (frame_number%40 < 20)
        //    theta = 1;
        //else
        //    theta = 10;
//printf("frame_number = %d \n",frame_number);
	//rho = 10;

        #ifdef debug_heading
            cvCircle(frame,heading,5,cvScalar(0,255,0,0),1,8,0);
            cvShowImage("Heading",frame);
        #endif

        //TEMPORARILY HACK A GO-STRAIGHT THINGY
        //if (rho > 5)
	//    theta += 1.3;

	theta = 1;
	rho = 10;
        // Give mission control its heading
        printf("Theta, Phi,Rho: %f, %f,%f\n", theta, phi,rho);
        SeaSQL_setSetPointVision_Theta(theta);
        SeaSQL_setSetPointVision_Phi(phi);
        SeaSQL_setSetPointVision_Rho(rho);
        Notify_send("UPDATED", "SetPointVision");

        cvWaitKey(DELAY);

    }

}
