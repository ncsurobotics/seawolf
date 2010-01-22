//THIS FILE:  tracks the movement of blobs to determine motion of the craft

#include "seawolf.h"
#include <stdio.h>
#include <time.h>
#include <math.h>
#include "vision.h"

static BLOB* old_blobs;
static int old_blob_number; //old blob number
static int old_cent_x;
static int old_cent_y;
static float trans_vel; //last translational speed
static float trans_angle; //direction of that speed
static float rot_vel; //speed of rotation
static Timer* timer; //holds time data 

//initialize track blobs
void blob_motion_init(){
   timer = Timer_new();
}

void blob_motion(IplImage* frame){

    double delta_t = Timer_getDelta(timer);            

    //so, we run through every new blob, match it to the closest old blobs, acount for trans & rot velocity, select best fit
    // this should give us many vectors throughout the screen.  subtract / add to them uniformaly until the origin is zero (this is translational)
    // now compute rotational velocity

    //Prepare for a blob detection on the frame
    BLOB* new_blobs;       
    Image* rgb_tmp;
    Image* indexed_tmp;
    IplImage* ipl_out;
    RGBPixel color = {0xff,0xff,0xff};

    //Initialize images 
    ipl_out = cvCreateImage(cvSize(frame->width,frame->height), 8, 3);
    rgb_tmp = Image_new(RGB, frame->width, frame->height);
    indexed_tmp = Image_new(INDEXED, frame->width, frame->height);

    IplImageToImage(frame, rgb_tmp);
    FindTargetColor(rgb_tmp, indexed_tmp, &color, 80,300);
    Image_indexedToRGB(indexed_tmp, rgb_tmp); 
    ImageToIplImage(rgb_tmp, ipl_out);

    //find blobs
    int new_blob_number = blob(ipl_out, &new_blobs, 0, 100);

    //declare calculated change in position
    int y_change = 0;

/*    //compute new centroid
    int i,j,k;
    double new_cent_x=0;
    double new_cent_y=0;
    for(i=0;i<new_blob_number;i++){
	new_cent_x += new_blobs[i].cent_x;
	new_cent_y += new_blobs[i].cent_y;
    }
    new_cent_x /= new_blob_number;
    new_cent_y /= new_blob_number;

    //compute estimated change in position
    int est_delta = old_cent_y - new_cent_y;
    old_cent_y = new_cent_y;


    //match each blob
    for(i=0;i<new_blob_number && i < old_blob_number; i++){
	//initialize newX and newY
	int newX = (int)new_blobs[i].cent_x;
	int newY = (int)new_blobs[i].cent_y;

	//DEBUG
        cvCircle(frame,cvPoint(newX,newY),5,cvScalar(0,255,0,0),1,8,0);

        int predictedX = newX;
	int predictedY = newY + est_delta;


    //cycle through the 5 most prominent blobs, and match them to the 5 last most prominent blobs
    int i,j,k;
    int y_change = 0;
    for(i = 0; i < new_blob_number && i < old_blob_number; i++){
        //compute rotational and translational drift to guess where our target blob should be

	//initialize newX and newY
	int newX = (int)new_blobs[i].cent_x;
	int newY = (int)new_blobs[i].cent_y;

	//DEBUG
        cvCircle(frame,cvPoint(newX,newY),5,cvScalar(0,255,0,0),1,8,0);

        //translational adjustment:
        newY -= trans_vel*sin(trans_angle);
        newX -= trans_vel*cos(trans_angle);

        //rotational adjustment:
        //temporarily center the blob around the origin
        newY -= frame->height/2;
        newX -= frame->width/2;

        //compute current angle
        float current_angle = 0.0f;
        if(newX == 0){
            if(newY >= 0){
                current_angle = M_PI/2;
            }else{
                current_angle = M_PI*3/4;
            }
        }else if(newX > 0){
            current_angle = atan((double)newY/newX);
        }else{
            current_angle = M_PI - atan((double)newY/(-1*newX)); 
        }
        if(current_angle < 0){
            current_angle += 2*M_PI;
        }

        //compute change in angle (between frames)
        float d_theta = rot_vel * delta_t;
        
        //now subtract the change to determine previous angle 
        float previous_angle = current_angle - d_theta;
        
        //and compute the distance from the origin (center of the screen)
        float radius = sqrt(newX*newX + newY*newY);

        //now use radius and previous angle to determine our final guestimate for the old X and Y
        int predictedX, predictedY;
        predictedX = radius * cos(previous_angle) + frame->width/2;
        predictedY = radius * sin(previous_angle) + frame->height/2;
*/ 
    //calculate the total error of the image, testing each pixel 

    int i,j;
    int total_error = 0;
    int best_error = -1; 
    int best_i = 0;
    for(i=-frame->height/4;i<frame->height/4;i+=5){
	for(j=0;j<new_blob_number;j++){
	    //DEBUGGING: 
            cvCircle(frame,cvPoint(new_blobs[j].cent_x,new_blobs[j].cent_y),5,cvScalar(0,0,255,0),1,8,0);
	    

	    //compute between each blob and the closest blob to this position 
	    int newX = new_blobs[j].cent_x;
	    int newY = new_blobs[j].cent_y + i;
	    if(newY > 0 && newY < frame->height){
		//find the nearest old blob, and add the distance to total error
	        int smallest_error = 100000;
		for(j = 0; j < old_blob_number; j++){
		    //compute error for this blob
		    int deltaX = old_blobs[j].cent_x - newX;
		    int deltaY = old_blobs[j].cent_y - newY;
		    int dist = deltaX*deltaX + deltaY*deltaY;

		    if(dist < smallest_error){
			smallest_error = dist;
		    }
		}
		total_error += smallest_error;
	    }
	}
 
	if(total_error < best_error || best_error < 0){
	    best_error = total_error;
	    best_i = i;
 	}
    }

    for(i = 0; i < new_blob_number && i < old_blob_number; i++){

	//initialize newX and newY
	int oldX = (int)new_blobs[i].cent_x;
	int oldY = (int)new_blobs[i].cent_y + i;

        if(oldY > 0 && oldY < frame->height){
            cvCircle(frame,cvPoint(oldX,oldY),5,cvScalar(0,255,0,0),1,8,0);
	}
    }

	//DEBUG
/*
	//now skip matching if assumed position is off the screen
	if(predictedX < 0 || predictedX > frame->width || predictedY < 0 || predictedY > frame->height) continue;

	//now cycle through the predicted blobs, looking for the closest, and totaling the error
	int closest_blob = 0;
        for(j = 0; j < old_blob_number; j++){
	    //compute error for this blob
	    int deltaX = old_blobs[j].cent_x - predictedX;
	    int deltaY = old_blobs[j].cent_y - predictedY;
	    int dist = deltaX*deltaX + deltaY*deltaY;

	    //compute error for current best blob
	    deltaX = (int)old_blobs[closest_blob].cent_x - predictedX;
	    deltaY = (int)old_blobs[closest_blob].cent_y - predictedY;
	    int best_dist = deltaX*deltaX + deltaY*deltaY;

	    //decide if this blob is closer than our current closest blob
	    if(dist < best_dist){
		closest_blob = j;
	    }
        }

	//compute the change in Y and add it to the average 
	y_change += new_blobs[i].cent_y - old_blobs[closest_blob].cent_y;
    }
    //average y_change

    if(i !=0 ){
        y_change /= i;
        printf("y_change = %d \n",y_change);

        trans_vel = y_change / delta_t;
        trans_angle = M_PI/2;
    }else{
	printf("no blobs found\n");
    }
*/
    //free resources        
    Image_destroy(rgb_tmp);
    Image_destroy(indexed_tmp);
    cvReleaseImage(&ipl_out);
    //preserve blobs
    blob_free(old_blobs, old_blob_number);
    old_blobs = new_blobs;
    old_blob_number = new_blob_number;
}

void blob_motion_free();















