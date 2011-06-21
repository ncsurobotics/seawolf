#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include <math.h>

#define VISUAL_DEBUG 1 

#define HOLE_SIZE .75 //small the number, smaller the hole

// Prototypes

int match_X(IplImage* binary, int index, int centroid_x, int centroid_y, int roix0, int roiy0, int roix, int roiy);
int match_O(IplImage* binary);

int arctan(int x, int y);

int match_X(IplImage* binary, int index, int cent_x, int cent_y, int roix0, int roiy0, int roix, int roiy){

    int i,x,y; //useful variable names
    CvPoint* points; //an array of pixel coordinates
    CvPoint* corners; //the corners of the image
    int pixel_count = 0; //total number of pixels we find
    
    //allocate memory for points
    points = (CvPoint*)calloc(binary->width * binary->height, sizeof(CvPoint)); 
    corners = (CvPoint*)calloc(4, sizeof(CvPoint)); 
  
    #ifdef VISUAL_DEBUG
        //create a debug image
        IplImage* debug = cvCreateImage(cvGetSize(binary),8,3);
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
                    corners[0].x = x;
                    corners[0].y = y;
                }
            }

            #ifdef VISUAL_DEBUG
                //copy the binary image onto the debug image
                int i = y*binary->width + x;
                debug->imageData[3*i + 0] = binary->imageData[i];
                debug->imageData[3*i + 1] = binary->imageData[i];
                debug->imageData[3*i + 2] = binary->imageData[i];
            #endif
        }
    }

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

       #ifdef VISUAL_DEBUG
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

    #ifdef VISUAL_DEBUG
        //printf("theta = %d, pxsum1 = %d, pxsum2 = %d \n", theta,pxsum1,pxsum2);

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

        cvNamedWindow("Debug", CV_WINDOW_AUTOSIZE);
        cvShowImage("Debug", debug);
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

    #ifdef VISUAL_DEBUG
        IplImage* compared = cvCreateImage(cvGetSize(xtemplate),8,3);
    #endif

    //XOR the template image with our warped image 
    int xor_sum = 0;
    for ( i=xtemplate->width*xtemplate->height -1; i>=0; i--){
        int p1 = xtemplate->imageData[i];
        int p2 = warped->imageData[i];
        if(( p1 != 0 &&  p1 != 0 ) || ( p2 == 0 && p2 == 0 )){
            xor_sum++;
        }
       
        #ifdef VISUAL_DEBUG
        if(p1 != 0 && p2 != 0){
            compared->imageData[i*3+0] = 0x00;
            compared->imageData[i*3+1] = 0xff;
            compared->imageData[i*3+2] = 0x00;
        }else if(p1 == 0 && p2 == 0){
            compared->imageData[i*3+0] = 0x00;
            compared->imageData[i*3+1] = 0x00;
            compared->imageData[i*3+2] = 0x00;
        }else if(p1 != 0){
            compared->imageData[i*3+0] = 0xff;
            compared->imageData[i*3+1] = 0x00;
            compared->imageData[i*3+2] = 0x00;
        }else if(p2 != 0){
            compared->imageData[i*3+0] = 0x00;
            compared->imageData[i*3+1] = 0x00;
            compared->imageData[i*3+2] = 0xff;
        }
        #endif
    }

    //compute confidence
    int confidence = xor_sum * 100 / (xtemplate->width*xtemplate->height);

    //scale confidence
    confidence = (confidence - 50 ) * 2;

    #ifdef VISUAL_DEBUG
        printf("X confidence = %d \n",confidence);

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
    free(points);
    free(corners);
    free(src);
    free(dst);
    cvReleaseMat(&tmatrix);

    #ifdef VISUAL_DEBUG
        cvReleaseImage(&debug);
        cvReleaseImage(&compared);
    #endif

    return 0;
}
int match_O(IplImage* binary){

    return 0;
}

//returns arctan of x and y, from -180 to 180 degrees
int arctan(int x, int y){
    int theta = (int)( atan2((double)y, (double)x) * 180 / M_PI );
    return theta;
}
