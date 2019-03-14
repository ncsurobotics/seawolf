#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include <math.h>

/* FILE CONTAINS:           */
/* match_letters()          */
/* find_bins()              */
/* and related functions    */

//#define VISUAL_DEBUG      1 
//#define VISUAL_DEBUG_X    1
//#define VISUAL_DEBUG_O    1

//#define VISUAL_DEBUG_BINS 1

/* X recognition */
#define X_CONFIDENCE_THRESHOLD 80 //required confidence to accept an X
/* O recognition */
#define HOLE_SIZE .5 //smaller the number, smaller the hole
#define R_RATIO .05 //number small radii allowed (per pixel)
#define O_CONFIDENCE_THRESHOLD 80 //required confidence to accept an O
/* corner finding */
#define CORNER_COUNT 15 //how many corners to look for
#define CORNER_QUALITY .5  //how sharp the corners must be
#define MIN_CORNER_DISTANCE 30 //how close the corners may be 
/* corner linking */
#define EDGE_WIDTH 3 //how far to look for edge pixels when linking corners
#define GAP_SIZE 15  //number of edgless pixels that can connect two corners
/* rectange recognition */
#define ANGLE_TOLERANCE .15 //how close to a right angle the bins must be
#define LIN_TOLERANCE .05 //how perfect the ratios of the rectangle sides must be

#ifndef M_PI
    #define M_PI 3.1415926535897932384626433832795028841971693993751058209749445923
#endif

// Rectangle Deffintion
typedef struct Rect_s {
    
    /* area of the rectangle */
    int32_t area;
    
    /* center of rectangle */
    int32_t c_x;
    int32_t c_y;

    /* direction of rectangle */
    int32_t theta;
} Rect;


/* PROTOTYPES */

//letter identification
int match_letters(IplImage* binary, int index, int cent_x, int cent_y, int roix0, int roiy0, int roix, int roiy);
int match_X(IplImage* binary, CvPoint* points, int pixel_count, CvPoint* r_point, int cent_x, int cent_y, IplImage* debug );
int match_O(IplImage* binary, CvPoint* points, int pixel_count, CvPoint* r_point, int cent_x, int cent_y, int mid_x, int mid_y, IplImage* debug );

//bin detection
Rect** find_bins(IplImage* frame, int* bin_count);
int pair_corners(CvPoint2D32f* pt1, CvPoint2D32f* pt2, IplImage* edges, IplImage* debug);
int mod(int x, int a);
int test_connect(int c1, int c2, int** pairs, int* pair_counts);
Rect* create_rect(CvPoint* ctr_pt, CvPoint* cls_pt, CvPoint* far_pt);

//misc 
int arctan(int x, int y);

/* FUNCTION: find_bins() */

void free_bins(Rect** rects, int num_rects){
    int i;
    for(i = 0; i < num_rects; i++){
        free(rects[i]);
    }
    free(rects);
}

Rect** find_bins(IplImage* frame, int* bin_count){

    //Edge Detection
    IplImage* grayscale = cvCreateImage(cvGetSize(frame),IPL_DEPTH_8U,1);
    cvCvtColor(frame, grayscale, CV_BGR2GRAY);
    IplImage* edge = cvCreateImage(cvGetSize(frame),8,1);

    cvCanny(grayscale,edge,120,120,3);

    #ifdef VISUAL_DEBUG_BINS 
        cvNamedWindow("Bin Edges", CV_WINDOW_AUTOSIZE);
        cvShowImage("Bin Edges", edge);
    #endif

    //Corner Detection
    int i,j,l;

    IplImage* eigimage = cvCreateImage(cvGetSize(frame),IPL_DEPTH_32F,1);
    IplImage* tmpimage = cvCreateImage(cvGetSize(frame),IPL_DEPTH_32F,1);
    CvPoint2D32f* corners;
    int corner_count = CORNER_COUNT;
    double quality_level = CORNER_QUALITY;
    double min_distance = MIN_CORNER_DISTANCE;
    int block_size = 5;

    //allocate memory for corners
    corners = (CvPoint2D32f*)calloc(corner_count,sizeof(CvPoint2D32f));

    //find corners
    cvGoodFeaturesToTrack(grayscale,eigimage,tmpimage,corners,&corner_count,quality_level,min_distance,NULL,block_size,0,0.0);

    IplImage* debug = NULL;
    #ifdef VISUAL_DEBUG_BINS 
        debug = cvCloneImage(frame);

        for(i=0;i<corner_count;i++){
            CvScalar corner_color = {{0,255,255}};
            CvPoint center;
            center.x = corners[i].x;
            center.y = corners[i].y;
            cvCircle(debug,center,5,corner_color,2,8,0);
        }

    #endif

    //create table of adjacent corners
    int** pairs;
    int** groups;
    int* group_sizes; //records sizes of groups of corners
    int* pair_counts; //records number of pairs per corner
    //int group_count = 0; //track number of groups

    //create list of rectangles
    Rect** rects = calloc(corner_count,sizeof(Rect*));
    int rect_count = 0;

    group_sizes = (int*)calloc(corner_count,sizeof(int));
    pair_counts = (int*)calloc(corner_count,sizeof(int));
    groups = (int**)calloc(corner_count,sizeof(int*));
    pairs = (int**)calloc(corner_count,sizeof(int*));
    for(i=0; i<corner_count; i++){
        pair_counts[i] = 0;
        group_sizes[i] = 1;
        groups[i] = (int*)calloc(corner_count,sizeof(int));
        pairs[i] = (int*)calloc(corner_count-1,sizeof(int));
        groups[i][0] = i;
    }
    
    //pair and group corners based on edge detect
    for(i = 0; i<corner_count; i++){
        for(j=i+1; j<corner_count; j++){
            int paired = pair_corners(&corners[i], &corners[j], edge, debug);
            if(!paired) continue;

            int g_old, g_new; 
            //find the old group that i belongs to
            for(g_old = i; group_sizes[g_old]<0; g_old = groups[g_old][0]);
            for(g_new = j; group_sizes[g_new]<0; g_new = groups[g_new][0]);
            

            if(g_old != g_new){
                //update old group to new group
                for(l=0;l<group_sizes[g_old];l++){
                    //check to see if groups[i][l] is already a member of groups[j]
                    int k;
                    int member_found = 0;
                    for(k=0;k<group_sizes[g_new];k++){
                        if (groups[g_new][k] == groups[g_old][l]){
                            member_found = 1;
                            break;
                        }
                    }
                    if(!member_found){
                        groups[g_new][group_sizes[g_new]++] = groups[g_old][l];
                    }
                }
                //flag this group as moved elsewhere
                group_sizes[g_old] = -1;
                groups[g_old][0] = j;
            }

            //record this match
            pairs[i][pair_counts[i]++] = j;
            pairs[j][pair_counts[j]++] = i;

            #ifdef VISUAL_DEBUG_BINS
                CvScalar connect_color = {{0,0,255}};
                CvPoint pt1, pt2;
                pt1.x = corners[i].x;
                pt2.x = corners[j].x;
                pt1.y = corners[i].y;
                pt2.y = corners[j].y;
                cvLine(debug,pt1,pt2,connect_color,1,8,0);
            #endif
        }
    }

    //Identify Bins
    CvPoint pt[3];
    int dis[3];
    int hyp[3];
    int connections[3];
    int cor[3]; 
    int group_finished;
    for(i=0; i<corner_count; i++){
        #ifdef VISUAL_DEBUG_BINS
            if(group_sizes[i] > 2){
                for(j=0; j<group_sizes[i]; j++){
                    for(l=0; l < pair_counts[groups[i][j]]; l++){
                        CvScalar group_color = {{255,0,255}};
                        CvPoint pt1, pt2;
                        pt1.x = corners[groups[i][j]].x;
                        pt2.x = corners[pairs[groups[i][j]][l]].x;
                        pt1.y = corners[groups[i][j]].y;
                        pt2.y = corners[pairs[groups[i][j]][l]].y;
                        cvLine(debug,pt1,pt2,group_color,1,8,0);
                    }
                }
            }
        #endif
        group_finished = 0;
        if(group_sizes[i] < 3) continue;
        //there are at least 3 corners in this group
        //test all combinations of 3 corners to see if we find a right triangle
        for(cor[0]=0; cor[0]<group_sizes[i]; cor[0]++){
            for(cor[1]=cor[0]+1;cor[1]<group_sizes[i]; cor[1]++){
                for(cor[2]=cor[1]+1; cor[2]<group_sizes[i]; cor[2]++){
                    for(j=0; j<3; j++){
                        //rename the coner coordinates
                        pt[j].x = corners[groups[i][cor[j]]].x;
                        pt[j].y = corners[groups[i][cor[j]]].y;
                    }

                    for(j=0; j<3; j++){
                        //make note of any disconections                        
                        int prv = mod(j-1,3);
                        int nxt = mod(j+1,3);
                        connections[j] = test_connect(groups[i][cor[prv]],groups[i][cor[j]],pairs,pair_counts);
                        connections[j] *= test_connect(groups[i][cor[nxt]],groups[i][cor[j]],pairs,pair_counts);

                        //gather distances between points 
                        dis[j] = (int)sqrt(pow(pt[prv].x-pt[nxt].x,2)+pow(pt[prv].y-pt[nxt].y,2)); 
                    }

                    for(j=0; j<3; j++){
                        if(!connections[j]) continue;

                        int prv = mod(j-1,3);
                        int nxt = mod(j+1,3);

                        //gather hypotnues calculations 
                        hyp[j] = (int)sqrt((double)pow(dis[prv],2)+pow((double)dis[nxt],2)); 
                    
                        //check hpyotneuses vs actual distances to find right angles
                        int ang_dif = abs(dis[j]-hyp[j]);
                        if(ang_dif > dis[j] * ANGLE_TOLERANCE) continue;

                        //check proportions of the rectangle
                        int small_dis, large_dis, cls_pt, far_pt;
                        if(dis[prv] < dis[nxt]){
                            cls_pt = nxt;
                            far_pt = prv;
                        }else{
                            cls_pt = prv;
                            far_pt = nxt;
                        }
                        small_dis = dis[far_pt];
                        large_dis = dis[cls_pt];
                        int lin_dif = abs(small_dis*2 - large_dis);
                        if(lin_dif > dis[j] * LIN_TOLERANCE) continue;

                        //we are now sure that these three points are part of a rectangle
                        //record this rectangle
                        rects[rect_count++] = create_rect(&pt[j],&pt[cls_pt],&pt[far_pt]);
                        group_finished = 1;
                        #ifdef VISUAL_DEBUG_BINS
                            int k;
                            for(k=0;k<3;k++){
                                CvScalar good_color = {{0,255,0}};
                                CvPoint center;
                                center.x = pt[k].x;
                                center.y = pt[k].y;
                                cvCircle(debug,center,7,good_color,2,8,0);
                            }
                        #endif
                        break;
                    }
                if(group_finished) break;    
                }
            if(group_finished) break;    
            }
        if(group_finished) break;    
        }
    }

    #ifdef VISUAL_DEBUG_BINS
        cvNamedWindow("Bin Debug",CV_WINDOW_AUTOSIZE);
        cvShowImage("Bin Debug",debug);
    #endif
    //free memory
    for(i=0; i<corner_count; i++){
        free(pairs[i]);
        free(groups[i]);
    }
    free(groups);
    free(group_sizes);
    free(pairs);
    free(pair_counts);
    free(corners);
    cvReleaseImage(&edge);
    cvReleaseImage(&grayscale);
    cvReleaseImage(&tmpimage);
    cvReleaseImage(&eigimage);

    #ifdef VISUAL_DEBUG_BINS
        cvReleaseImage(&debug);
    #endif
   
    //return data
    (*bin_count) = rect_count;
    return rects;
}

//create a new rectangle structure
Rect* create_rect(CvPoint* ctr_pt, CvPoint* cls_pt, CvPoint* far_pt){
    //compute center
    int32_t cnt_x = (cls_pt->x + far_pt->x )/2;
    int32_t cnt_y = (cls_pt->y + far_pt->y )/2;
    
    //compute area
    int smalld = sqrt(pow(cls_pt->x-ctr_pt->x,2)+pow(cls_pt->y-ctr_pt->y,2));
    int larged = sqrt(pow(far_pt->x-ctr_pt->x,2)+pow(far_pt->y-ctr_pt->y,2));
    int32_t area = smalld * larged;

    //compute angle
    int refx = (cls_pt->x + ctr_pt->x ) / 2;
    int refy = (cls_pt->y + ctr_pt->y ) / 2;
    refx -= cnt_x;
    refy -= cnt_y;
    int32_t theta = arctan(refx,refy);

    //create rectangle
    Rect* rect = (Rect*)calloc(1,sizeof(Rect));
    rect->area = area;
    rect->c_x = cnt_x;
    rect->c_y = cnt_y;
    rect->theta = theta;

    return rect;
}

int test_connect(int c1, int c2, int** pairs, int* pair_counts){
    int connected = 0;
    int i;
    for(i=0; i<pair_counts[c1]; i++){
        if(pairs[c1][i] == c2){
            connected = 1;
        }
    }
    for(i=0; i<pair_counts[c2]; i++){
        if(pairs[c2][i] == c1){
            connected = 1;
        }
    }
    return connected;
}
int pair_corners(CvPoint2D32f* pt1, CvPoint2D32f* pt2, IplImage* edges, IplImage* debug){
    int x,y;
    int total_gap = 0;
    int distance = 0;
    
    if(abs(pt1->x - pt2->x) > abs(pt1->y - pt2->y)){
        //sort the two corners by x value
        CvPoint lowx;
        CvPoint highx; 
        if(pt1->x < pt2->x){
            lowx.x = pt1->x;
            lowx.y = pt1->y;
            highx.x = pt2->x;
            highx.y = pt2->y;
        }else{
            lowx.x = pt2->x;
            lowx.y = pt2->y;
            highx.x = pt1->x;
            highx.y = pt1->y;
        }
        distance = highx.x - lowx.x;

        //compute the slope between these two points
        double slope = (double)(highx.y-lowx.y)/(highx.x-lowx.x);
        
        //check the number of edge pixels between these two corners 
        for(x=lowx.x; x<=highx.x; x++){
            int linept = (x-lowx.x) * slope + lowx.y;
            int gap_found = 1;
            for(y= linept-EDGE_WIDTH; y <= linept+EDGE_WIDTH; y++){
                if(x < 0 || y < 0 || x >= edges->width || y >= edges->height) continue;
                if(edges->imageData[x+y*edges->width] != 0){
                    gap_found = 0;
                }
            }
            total_gap += gap_found;

        }
    }else{
        //sort the two corners by y value
        CvPoint lowy;
        CvPoint highy; 
        if(pt1->y < pt2->y){
            lowy.x = pt1->x;
            lowy.y = pt1->y;
            highy.x = pt2->x;
            highy.y = pt2->y;
        }else{
            lowy.x = pt2->x;
            lowy.y = pt2->y;
            highy.x = pt1->x;
            highy.y = pt1->y;
        }
        distance = highy.y - lowy.y;
        
        //compute the slope between these two points
        double slope = (double)(highy.x-lowy.x)/(highy.y-lowy.y);
        
        //check the number of edge pixels between these two corners 
        for(y=lowy.y; y<=highy.y; y++){
            int linept = (y-lowy.y) * slope + lowy.x;
            int gap_found = 1;
            for(x= linept-EDGE_WIDTH; x <= linept+EDGE_WIDTH; x++){
                if(x < 0 || y < 0 || x >= edges->width || y >= edges->height) continue;
                if(edges->imageData[x+y*edges->width] != 0){
                    gap_found = 0;
                }
            }
            total_gap += gap_found;
        }
    }
    
    //decide if the points are connected
    int points_connected = 0;
    if(total_gap < GAP_SIZE)
        points_connected = 1;

    return points_connected;
}

int mod(int x, int a){
    for(;x>=a;x-=a);
    for(;x<0;x+=a);
    return x;
}

int match_letters(IplImage* binary, int index, int cent_x, int cent_y, int roix0, int roiy0, int roix, int roiy){

    int x,y; //useful variable names
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
        int i;
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
        CvScalar boxcolor = {{0, 254, 0}};
        cvLine(debug, corners[0], corners[1], boxcolor, 1, 8, 0);
        cvLine(debug, corners[1], corners[2], boxcolor, 1, 8, 0);
        cvLine(debug, corners[2], corners[3], boxcolor, 1, 8, 0);
        cvLine(debug, corners[3], corners[0], boxcolor, 1, 8, 0);
        
        //draw a circle at the center of the image
        CvPoint center = {cent_x, cent_y};
        CvScalar centercolor = {{0, 0, 254}};
        cvCircle(debug, center, 5, centercolor, 2, 8, 0);

        //mark corner 0
        CvPoint corner0 = {corners[0].x, corners[0].y};
        CvScalar cornercolor = {{254, 0, 254}};
        cvCircle(debug, corner0, 5, cornercolor, 1, 8, 0);

    #endif

    //load template
    IplImage* xtemplate = cvLoadImage("../vision/xtemplate.png",CV_LOAD_IMAGE_GRAYSCALE);
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
        CvScalar fillcolor = {{0}};
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
        CvScalar centroid_color = {{0,255,0}}; 
        cvCircle(debug, centroid, 5, centroid_color, 1, 8, 0);  

        CvPoint midpoint = {mid_x, mid_y};
        CvScalar mid_color = {{255,0,0}};
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
