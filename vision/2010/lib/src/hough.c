/* hough.c
 * This is a modification of opencv's hough implementation, ported to c.  
 *
 * Debugs specific to this file:
 *   debug_hough_lines
 *   debug_hough_graph
 *   debug_hough_threshold
 */

#include "vision_lib.h"

#include <cv.h>
#include <stdio.h>
#include <highgui.h>
#include <math.h>

CvMemStorage* storage;
CvSeq* lines;

//static CV_IMPLEMENT_QSORT_EX( icvHoughSortDescent32s, int, hough_cmp_gt, const int* );

typedef struct CvLinePolar
{
    float rho;
    float angle;
}
CvLinePolar;

int extra_line_x = 0;
int extra_line_y = 0;
int button_down = 0;
void houghMouseDraw(int event, int x, int y, int flags, void* param)
{
    if (event == CV_EVENT_LBUTTONDOWN)
    {
        button_down = 1;
    } else if (event == CV_EVENT_LBUTTONUP) {
        button_down = 0;
    }
    if (button_down = 1)
    {
        extra_line_x = x;
        extra_line_y = y;
    } else {
        extra_line_x = 0;
        extra_line_y = 0;
    }
}

#ifdef debug_hough_threshold
    int threshold_slider = 18;
#endif

void hough_init()
{
    storage = cvCreateMemStorage(0);
    #ifdef debug_hough_lines
        cvNamedWindow("Hough Lines", CV_WINDOW_AUTOSIZE);
    #endif
    #ifdef debug_hough_graph
        cvNamedWindow("Hough Graph", CV_WINDOW_AUTOSIZE);
        cvSetMouseCallback("Hough Graph", houghMouseDraw, 0);
    #endif
    #ifdef debug_hough_threshold
        cvCreateTrackbar("Hough Threshold", "Controls", &threshold_slider, 255, NULL);
    #endif
}

//ARGUMENTS: targetAngle: desired angle ranging from 0-180 degrees
//           angleThreshold: allowable error in degrees
CvSeq* hough(IplImage* img, IplImage* original, int threshold, int linesMax,int targetAngle, int angleThreshold, int clusterSize, int clusterWidth, int clusterHeight)
{
    #ifdef debug_hough_threshold
        threshold = threshold_slider;
    #endif

    // What used to be arguments:
    float rho = 0.5f; // Rho Resolution
    float theta = CV_PI/360; // Angle Resolution
    lines = cvCreateSeq( CV_32SC4, sizeof(CvSeq), sizeof(int)*4, (CvMemStorage*)storage );
    //int linesMax = 2; //max number of line clusters
    //float angleThreshold = 8.0; //2 or less allows all lines, the higher the number, the more verticle the lines must be to register
    //int clusterSize = 10; //number of lines in a cluster
    //int clusterWidth = 60; //the max rho distance between elements of a cluster
    //int clusterHeight = 60; //the max angular distance between elements of a cluster

    int *accum = 0;
    int **line_clusters = 0; //holds the clusters of lines to be averaged together
    int *temp_cluster = 0;
    int *sort_buf=0;
    float *tabSin = 0;
    float *tabCos = 0;

    const char* image;
    int step, width, height;
    int numangle, numrho;
    float ang;
    int r, n;
    int i, j ,k, t,x,y;
    float irho = 1 / rho;
    double scale;
    int newcluster;
    int averageRho;
    int clusterCount;
    int low_T; //low angle threshold
    int high_T; //high T

    image = img->imageData;
    step = img->widthStep;
    width = img->width;
    height = img->height;

    numangle = cvRound(CV_PI / theta);
    numrho = cvRound(((width + height) * 2 + 1) / rho);
    //printf("numangle = %d, numrho = %d \n",numangle,numrho);
    //fflush(NULL);

    //scale thresholds to image
    targetAngle = (targetAngle+90)%180; //adjust targetAngle to fit the hough graph
    low_T = (targetAngle*numangle/180 - angleThreshold*numangle/180 + numangle)%numangle;
    high_T = (targetAngle*numangle/180 + angleThreshold*numangle/180)%numangle;
//    printf("low_T = %d,high_T = %d\n",low_T,high_T);
//    fflush(NULL);

    accum = (int*)cvAlloc( sizeof(accum[0]) * (numangle+2) * (numrho+2));
    sort_buf = (int*)cvAlloc( sizeof(accum[0]) * linesMax  );
    tabSin = (float*)cvAlloc( sizeof(tabSin[0]) * numangle );
    tabCos = (float*)cvAlloc( sizeof(tabCos[0]) * numangle );
    memset( accum, 0, sizeof(accum[0]) * (numangle+2) * (numrho+2));
    temp_cluster = (int*)cvAlloc(sizeof(accum[0])*clusterSize);
    //allocate memory for the cluster log 
    line_clusters = (int**)cvAlloc(sizeof(accum[0])*linesMax);
    for(i=0;i<linesMax;i++)
    line_clusters[i] = (int*)cvAlloc(sizeof(accum[0])*clusterSize);
    
    //initialize cluster log with -1
    for(i=0;i<linesMax;i++)
      for(j=0;j<clusterSize;j++)
        line_clusters[i][j] = -1;

    //initialize sort_buf with -1
    for(i=0;i<linesMax;i++)
    sort_buf[i] = -1;

    for( ang = 0, n = 0; n < numangle; ang += theta, n++ )
    {
        tabSin[n] = (float)(sin(ang) * irho);
        tabCos[n] = (float)(cos(ang) * irho);
    }

    // stage 1. fill accumulator
    for( i = 0; i < height; i++ )
    {
        for( j = 0; j < width; j++ )
        {
            if( image[i * step + j] != 0 )
                for( n = 0; n < numangle; n++ )
                {
                    r = cvRound( j * tabCos[n] + i * tabSin[n] );
                    r += (numrho - 1) / 2;
                    accum[(n+1) * (numrho+2) + r+1]++;
                }
        }
    }

    // stage 2. find local maximums

    for( r = 0; r < numrho; r++ )
        for( n = 0; n < numangle; n++ )
        {
            int base = (n+1) * (numrho+2) + r+1;
            if( accum[base] > threshold &&
                accum[base] > accum[base - 1] && accum[base] >= accum[base + 1] &&
                accum[base] > accum[base - numrho - 2] && accum[base] >= accum[base + numrho + 2] ) {

        //check to make sure this line is in the angle threshold
        if(low_T < high_T){
            if(base/numrho < low_T || base/numrho > high_T) continue;
        }else{
            if(base/numrho < low_T && base/numrho > high_T) continue;
        }
        //printf("base/numrho = %d\n",base/numrho);
        //fflush(NULL);

        newcluster = 1;
        for(i=linesMax-1;i>=0;i--){
           //check to see if this max should be placed into this cluster
           if(sort_buf[i] != -1 && 
              ( //it's within a box
    (abs(base%(numrho+2) - sort_buf[i]%(numrho+2)) < clusterWidth && abs(base/(numrho+2)-sort_buf[i]/(numrho+2)) < clusterHeight)
              || //or it's witthin a box when including rollover
    (abs(abs(base%(numrho+2)-numrho/2) - abs(sort_buf[i]%(numrho+2)-numrho/2)) < clusterWidth && numangle-abs(base/(numrho+2) - sort_buf[i]/(numrho+2)) < clusterHeight)
                  )
                     )   
           {
              //if so, sort it into that cluster
              for(j=0;j<clusterSize;j++){
            if(line_clusters[i][j] == -1){
              line_clusters[i][j] = base;
              break;
            }
                    else if(accum[base] > accum[line_clusters[i][j]]){
              for(k=clusterSize-1;k>j;k--) 
                line_clusters[i][k] = line_clusters[i][k-1];
                          line_clusters[i][j] = base;
              break;
            }
              }
              newcluster = 0;
              break;      //don't let this line get placed in two clusters
           }
        }
        //if this is a new cluster, sort it in by accumulator value
        if(newcluster){

           k = -1;
           for(t=0;t<linesMax;t++){ 
              if(sort_buf[t] == -1) k=t; //this slot in the sort buff is empty so we can't check accum
              else if (accum[base]>accum[line_clusters[t][0]]) k=t;
                   }
               if (k>-1) {
               for(j=0;j<k;j++){
                  sort_buf[j] = sort_buf[j+1];
                  for(i=0; i<clusterSize;i++)
                 line_clusters[j][i] = line_clusters[j+1][i];
               }
               sort_buf[k] = base;
               line_clusters[k][0] = base; 
               for(i=1;i<clusterSize;i++) line_clusters[k][i] = -1;
           }
        }else{// we just added something to a cluster, so we might have to move one cluster up in priority       
           for(i=0;i<linesMax-1;i++){
              if(line_clusters[i][0] !=-1 && accum[line_clusters[i][0]] > accum[line_clusters[i+1][0]]){
                 k=i; //this is the out-of-place cluster 
                 for(t=0;t<clusterSize;t++) 
                           temp_cluster[t] = line_clusters[k][t];
             for(j=k;  j<linesMax-1 && accum[temp_cluster[0]] > accum[line_clusters[j+1][0]] ; j++){
               for(t=0;t<clusterSize;t++)
                 line_clusters[j][t] = line_clusters[j+1][t];
             }
             for(t=0;t<clusterSize;t++)
                    line_clusters[j][t] = temp_cluster[t];
             break;
              }
           }
           for(i=0;i<linesMax;i++) //update sort_buf with the newley sorted list of clusters  
             sort_buf[i] = line_clusters[i][0]; //used to be average
        }
            }
        
        }

    #ifdef debug_hough_graph
        IplImage* hough_graph = cvCreateImage(cvSize(numrho, numangle),8,3);
        for (r=0; r < numrho; r++)
        {
            for(n=0; n<numangle; n++)
            {
                int value = accum[(n+1) * (numrho+2) + r+1];
                CvScalar pixel;
                if (value>220)
                {
                    //printf("Value: %d\n",value);
                    //fflush(NULL);
                }
                if (value > threshold)
                {
                    pixel.val[0] = 0;
                    pixel.val[1] = MIN(value,255);
                    pixel.val[2] = 0;
                } else {
                    pixel.val[0] = 0;
                    pixel.val[1] = 0;
                    pixel.val[2] = MIN(value,255); 
                }
                //printf("%d/%d %d/%d\n",n,numangle,r,numrho);
                //fflush(NULL);
                cvSet2D(hough_graph,n,r,pixel);
                // Yes, cvSet2D is really inefficient, but its just a debug
            }
        }
    #endif

    // stage 4. store the lines to the output buffer
    linesMax = linesMax;
    scale = 1./(numrho+2);
    for( i = 0; i < linesMax; i++ )
    {
        CvLinePolar line;
//        int idx = sort_buf[i];
        int idx = line_clusters[i][0];
//printf("base %i = %d  accum = %d x=%d y=%d \n",i, idx, accum[line_clusters[i][0]],idx%(numrho+2),idx/(numrho+2));
//fflush(NULL);
        int n = cvFloor(idx*scale) - 1;
        int r = idx - (n+1)*(numrho+2) - 1;
        line.rho = (r - (numrho - 1)*0.5f) * rho;
        line.angle = n * theta;
        if(idx == -1){
       line.rho = -999;
    }
        cvSeqPush( lines, &line );
        #ifdef debug_hough_graph
            //printf("%f %f\n", line.rho, line.angle);
            //fflush(NULL);
            cvCircle(hough_graph, cvPoint(r,n), 5, cvScalar(255,0,0,0),1,8,0);
        #endif
    }
//printf("\n");
//fflush(NULL);
    #ifdef debug_hough_graph
        cvShowImage("Hough Graph", hough_graph);
        cvReleaseImage(&hough_graph);
    #endif

    cvFree( &sort_buf );
    cvFree( &tabSin );
    cvFree( &tabCos );
    cvFree( &accum );
    for(i=0;i<linesMax;i++)
    cvFree(&line_clusters[i]);
    cvFree( &line_clusters);

    #ifdef debug_hough_lines

        IplImage* houghImage = cvCreateImage(cvGetSize(img),8,3);
        cvCopy(original, houghImage, 0);
        if (extra_line_x != 0)
        {
            CvLinePolar line;
            line.rho = (extra_line_x - (numrho - 1)*0.5f) * rho;
            line.angle = extra_line_y*theta;
            //printf("Rho:%f  Theta:%f\n",line.rho,line.angle);
            //fflush(NULL);

            CvPoint pt1, pt2;
            double a = cos(line.angle), b = sin(line.angle);
            double x0 = a*line.rho, y0 = b*line.rho;
            pt1.x = cvRound(x0 + 1000*(-b));
            pt1.y = cvRound(y0 + 1000*(a));
            pt2.x = cvRound(x0 - 1000*(-b));
            pt2.y = cvRound(y0 - 1000*(a));
            cvLine( houghImage, pt1, pt2, CV_RGB(0,255,0), 1, CV_AA, 0 ); 

        }
        for(i = 0; i < linesMax; i++ )
        {
            float* line = (float*)cvGetSeqElem(lines,i);
            float rho = line[0];
            float theta = line[1];
            CvPoint pt1, pt2;
            double a = cos(theta), b = sin(theta);
            double x0 = a*rho, y0 = b*rho;
            pt1.x = cvRound(x0 + 1000*(-b));
            pt1.y = cvRound(y0 + 1000*(a));
            pt2.x = cvRound(x0 - 1000*(-b));
            pt2.y = cvRound(y0 - 1000*(a));
            //printf("Rho:%f  Theta:%f\n",rho,theta);
            cvLine( houghImage, pt1, pt2, CV_RGB(255,0,0), 1, CV_AA, 0 );
        }
        if (lines->total == 0 && extra_line_x == 0)
        {
            cvShowImage("Hough Lines", original);
        } else {
            cvShowImage("Hough Lines", houghImage);
        }
        cvReleaseImage(&houghImage);

    #endif

    return lines;
}

void hough_free()
{
}
