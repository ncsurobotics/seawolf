#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include <math.h>

//#define VISUAL_DEBUG 1 
//#define VISUAL_DEBUG_X 1
//#define VISUAL_DEBUG_O 1

#define HOLE_SIZE .5 //smaller the number, smaller the hole
#define R_RATIO .05 //number small radii allowed (per pixel)
#define X_CONFIDENCE_THRESHOLD 80 //required confidence to accept an X
#define O_CONFIDENCE_THRESHOLD 80 //required confidence to accept an O

// Prototypes
int match_letters(IplImage* binary, int index, int cent_x, int cent_y, int roix0, int roiy0, int roix, int roiy);
int match_X(IplImage* binary, CvPoint* points, int pixel_count, CvPoint* r_point, int cent_x, int cent_y, IplImage* debug );
int match_O(IplImage* binary, CvPoint* points, int pixel_count, CvPoint* r_point, int cent_x, int cent_y, int mid_x, int mid_y, IplImage* debug );
int arctan(int x, int y);

int match_letters(IplImage* binary, int index, int cent_x, int cent_y, int roix0, int roiy0, int roix, int roiy){

    int i,x,y; //useful variable names
    CvPoint* points; //an array of pixel coordinates
    int pixel_count = 0; //total number of pixels we find
    CvPoint r_point; //a reference point which has the maximum radius

    //allocate memory for points
    points = (CvPoint*)calloc(binary->width * binary->height, sizeof(CvPoint)); 

    //handle the debug image
    IplImage* debug = NULL;
    #ifdef VISUAL_DEBUG
        debug = cvCreateImage(cvGetSize(binary),8,3);

        //black out the entire debug image
        for(i=binary->width*binary->height - 1; i>=0; i--){
            debug->imageData[3*i + 0] = 0x00;
            debug->imageData[3*i + 1] = 0x00;
            debug->imageData[3*i + 2] = 0x00;
        }
    #endif 

    //populate a list of pixel coordinates, and find the furthest pixel
    int maxr = 0;
    for(x = roix0; x <= roix0 + roix; x++){
        for( y = roiy0; y <= roiy0 + roiy; y++){
            if(binary->imageData[y*binary->width + x] == index){
                //record this pixel
                points[pixel_count].x = x;
                points[pixel_count].y = y;
                
                //increment pixel count
                pixel_count++;
               
                //look for furthest pixel from centroid
                int tempx = x - cent_x;
                int tempy = y - cent_y; 
                int r = (int)sqrt((double)(tempx*tempx + tempy*tempy));

                if( r > maxr){
                    maxr = r;
                    r_point.x = x;
                    r_point.y = y;
                }
            }

            #ifdef VISUAL_DEBUG
                //copy the binary image onto the debug image
                i = y*binary->width + x;
                if(binary->imageData[i] == index){
                    debug->imageData[3*i + 0] = 0xff;
                    debug->imageData[3*i + 1] = 0xff;
                    debug->imageData[3*i + 2] = 0xff;
                }else{
                    debug->imageData[3*i + 0] = 0x00;
                    debug->imageData[3*i + 1] = 0x00;
                    debug->imageData[3*i + 2] = 0x00;
                }
            #endif
        }
    }

    //compute midpoint of roi
    int mid_x = roix0 + roix/2;
    int mid_y = roiy0 + roiy/2;

    //check for an X
    int x_confidence = match_X(binary, points, pixel_count, &r_point, cent_x, cent_y, debug);
    int o_confidence = match_O(binary, points, pixel_count, &r_point, cent_x, cent_y,mid_x, mid_y, debug);

    //determine if this blob is an X or an O
    int result  = 0;
    if( x_confidence >= X_CONFIDENCE_THRESHOLD && o_confidence >= O_CONFIDENCE_THRESHOLD ){
        //something is very wrong.  
        result = 0;
    }else if( x_confidence >= X_CONFIDENCE_THRESHOLD ){
        //we likely see an X
        result = 1;
    }else if( o_confidence >= O_CONFIDENCE_THRESHOLD ){
        //we likely see an O
        result = 2;
    }else{
        //we do not see anything
        result = 0;
    }

    #ifdef VISUAL_DEBUG
        cvNamedWindow("Debug", CV_WINDOW_AUTOSIZE);
        cvShowImage("Debug", debug);
    #endif

    //free memory
    free(points);
    #ifdef VISUAL_DEBUG
        cvReleaseImage(&debug);
    #endif


    return result;    
}

int match_X(IplImage* binary, CvPoint* points, int pixel_count, CvPoint* r_point, int cent_x, int cent_y, IplImage* debug){

    int i,x,y; //useful variable names
    CvPoint* corners; //the corners of the image
    
    corners = (CvPoint*)calloc(4, sizeof(CvPoint)); 
    corners[0].x = r_point->x;
    corners[0].y = r_point->y;

    //find the angle of the first corner
    x = corners[0].x - cent_x;
    y = corners[0].y - cent_y;
    int theta = arctan(y,x);

    //find the other 3 corners
    int maxr1 = 0;
    int maxr2 = 0;
    int maxr3 = 0;
    //keep track of the pixel sums on either side of angle0 
    int pxsum1 = 0; //this is bigger --> corner 0 goes in upper left
    int pxsum2 = 0; // this is bigger --> corner 0 goes in upper right
    for(i = pixel_count -1; i>=0; i--){
        x = points[i].x - cent_x;
        y = points[i].y - cent_y;
        int tempang = arctan(y,x);

        //normalize angles
        if (tempang < theta) tempang += 360;
        
        //find tempr
        int tempr = (int)sqrt((double)(x*x + y*y));

        if( tempang - theta > 315 ){
            //we are in the same quadrant as the origional angle
            pxsum1++;
        } else if( tempang - theta > 225){
            //call this quadrant 3
            if( tempr > maxr3){
                maxr3 = tempr;
                corners[3].x = points[i].x;
                corners[3].y = points[i].y;
            }
       } else if( tempang - theta > 135) {
            //call this quadrant 2
            if( tempr > maxr2) {
                maxr2 = tempr;
                corners[2].x = points[i].x;
                corners[2].y = points[i].y;
            }
       } else if( tempang - theta > 45) {
            //call this quadrant 1
            if( tempr > maxr1) {
                maxr1 = tempr;
                corners[1].x = points[i].x;
                corners[1].y = points[i].y;
            }
       } else {
            //we are again in the same quadrant as the origional angle
            pxsum2++;
       }

       #ifdef VISUAL_DEBUG_X
            //color every quadrant a different color
            if( tempang - theta > 315 ){
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+2]=0;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+1]=254;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+0]=254;
            } else if( tempang - theta > 225){
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+2]=254;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+1]=0;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+0]=0;
           } else if( tempang - theta > 135) {
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+2]=0;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+1]=0;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+0]=254;
           } else if( tempang - theta > 45) {
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+2]=254;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+1]=0;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+0]=254;
           } else {
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+2]=0;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+1]=254;
                debug->imageData[3*points[i].y*debug->width+3*points[i].x+0]=0;
           }
        #endif
    }

    #ifdef VISUAL_DEBUG_X
        //draw a line between consecutive corners
        CvScalar boxcolor = {0, 254, 0};
        cvLine(debug, corners[0], corners[1], boxcolor, 1, 8, 0);
        cvLine(debug, corners[1], corners[2], boxcolor, 1, 8, 0);
        cvLine(debug, corners[2], corners[3], boxcolor, 1, 8, 0);
        cvLine(debug, corners[3], corners[0], boxcolor, 1, 8, 0);
        
        //draw a circle at the center of the image
        CvPoint center = {cent_x, cent_y};
        CvScalar centercolor = {0, 0, 254};
        cvCircle(debug, center, 5, centercolor, 2, 8, 0);

        //mark corner 0
        CvPoint corner0 = {corners[0].x, corners[0].y};
        CvScalar cornercolor = {254, 0, 254};
        cvCircle(debug, corner0, 5, cornercolor, 1, 8, 0);

    #endif

    //load template
    IplImage* xtemplate = cvLoadImage("xtemplate.png",CV_LOAD_IMAGE_GRAYSCALE);
    //get transformation matrix that would place corner values
        //in the correct location to compare to template

    //transform image
        //create an array for the 4 src points and dest points
        CvPoint2D32f* src;
        CvPoint2D32f* dst;
        src = (CvPoint2D32f*)calloc(4, sizeof(CvPoint2D32f));
        dst = (CvPoint2D32f*)calloc(4, sizeof(CvPoint2D32f));

        //populate the src array 
        if( pxsum1 >= pxsum2 ){
            for ( i=0; i<4; i++){
                src[i].x = corners[i].x;
                src[i].y = corners[i].y;
            }
        }else{
            for ( i=0; i<4; i++){
                int j = i-1;
                if ( j<0 ) j = 3;
                src[i].x = corners[j].x;
                src[i].y = corners[j].y;
            }
        }
        //populate the dst array
        dst[0].x = 0;
        dst[0].y = 0;
        dst[1].x = 0;
        dst[1].y = 100;
        dst[2].x = 100;
        dst[2].y = 100;
        dst[3].x = 100;
        dst[3].y = 0;

        //get the transformation matrix
        CvMat* tmatrix = cvCreateMat(3,3,CV_32FC1);
        tmatrix = cvGetPerspectiveTransform( src, dst, tmatrix);

        //transform the image
        CvSize warpedsize = {100,100};
        IplImage* warped = cvCreateImage(warpedsize, 8, 1);
        CvScalar fillcolor = {0};
        cvWarpPerspective(binary, warped, tmatrix,CV_INTER_LINEAR+CV_WARP_FILL_OUTLIERS , fillcolor);

    #ifdef VISUAL_DEBUG_X
        IplImage* compared = cvCreateImage(cvGetSize(xtemplate),8,3);
    #endif

    //XOR the template image with our warped image 
    int xor_sum = 0;
    for ( i=xtemplate->width*xtemplate->height -1; i>=0; i--){
        int p1 = xtemplate->imageData[i];
        int p2 = warped->imageData[i];
        if(( p1 != 0 &&  p2 != 0 ) || ( p1 == 0 && p2 == 0 )){
            xor_sum++;
        }
       
        #ifdef VISUAL_DEBUG_X
        if(p1 != 0 && p2 != 0){
            compared->imageData[i*3+0] = 0x00;
            compared->imageData[i*3+1] = 0xff;
            compared->imageData[i*3+2] = 0x00;
        }else if(p1 == 0 && p2 == 0){
            compared->imageData[i*3+0] = 0x00;
            compared->imageData[i*3+1] = 0xff;
            compared->imageData[i*3+2] = 0x00;
        }else if(p1 != 0){
            compared->imageData[i*3+0] = 0xff;
            compared->imageData[i*3+1] = 0x00;
            compared->imageData[i*3+2] = 0x00;
        }else if(p2 != 0){
            compared->imageData[i*3+0] = 0xff;
            compared->imageData[i*3+1] = 0x00;
            compared->imageData[i*3+2] = 0x00;
        }
        #endif
    }

    //compute confidence
    int confidence = xor_sum * 100 / (xtemplate->width*xtemplate->height);

    #ifdef VISUAL_DEBUG_X
        cvNamedWindow("Compared",CV_WINDOW_AUTOSIZE);
        cvShowImage("Compared", compared);

        cvNamedWindow("Warped", CV_WINDOW_AUTOSIZE);
        cvShowImage("Warped", warped);

        cvNamedWindow("Xtemplate", CV_WINDOW_AUTOSIZE);
        cvShowImage("Xtemplate",xtemplate);
    #endif

    //free memory
    cvReleaseImage(&xtemplate);
    cvReleaseImage(&warped);
    free(corners);
    free(src);
    free(dst);
    cvReleaseMat(&tmatrix);
    #ifdef VISUAL_DEBUG_X
        cvReleaseImage(&compared);
    #endif

    return confidence;
}
int match_O(IplImage* binary, CvPoint* points, int pixel_count, CvPoint* r_point, int cent_x, int cent_y, int mid_x, int mid_y, IplImage* debug){

    int i,x,y; //useful variables
    int o_confidence = 0; //set to 100 if the blob is identified as a circle

    //compute max r
    x = r_point->x - mid_x;
    y = r_point->y - mid_y; 
    int maxr = (int)sqrt(x*x + y*y);

    //count the number of pixels where the hole should be 
    int small_r_sum = 0;
    for( i=0; i<pixel_count; i++){
        x = points[i].x - mid_x;
        y = points[i].y - mid_y;
        int r = (int)sqrt(x*x + y*y);

        if( r < maxr * HOLE_SIZE){
            small_r_sum++;

            #ifdef VISUAL_DEBUG_O
                int temp_idx = 3*points[i].y*binary->width + 3*points[i].x;
                debug->imageData[temp_idx + 2] = 0xff;
                debug->imageData[temp_idx + 1] = 0x00;
                debug->imageData[temp_idx + 0] = 0x00;
            #endif
        }
    }
   
    #ifdef VISUAL_DEBUG_O
        //mark the centroid being used
        CvPoint centroid = {cent_x, cent_y};
        CvScalar centroid_color = {0,255,0}; 
        cvCircle(debug, centroid, 5, centroid_color, 1, 8, 0);  

        CvPoint midpoint = {mid_x, mid_y};
        CvScalar mid_color = {255,0,0};
        cvCircle( debug, midpoint, 5, mid_color, 1, 8, 0);
    #endif

    int small_r_threshold = R_RATIO * pixel_count;
    if( small_r_sum < small_r_threshold){
        o_confidence = 100;    
    }

    return o_confidence;
}

//returns arctan of x and y, from -180 to 180 degrees
int arctan(int x, int y){
    int theta = (int)( atan2((double)y, (double)x) * 180 / M_PI );
    return theta;
}
