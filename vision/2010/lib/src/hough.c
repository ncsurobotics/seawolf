/* hough.c
 * This is a modification of opencv's hough implementation, ported to c.  
 */

#include "vision_lib.h"

#include <cv.h>
#include <stdio.h>
#include <highgui.h>
#include <math.h>

typedef struct CvLinePolar
{
    float rho;
    float angle;
} CvLinePolar;

//ARGUMENTS: targetAngle: desired angle ranging from 0-180 degrees
//           angleThreshold: allowable error in degrees
CvSeq* hough(IplImage* img, IplImage* original, int threshold, int linesMax,int targetAngle, int angleThreshold, int clusterSize, int clusterWidth, int clusterHeight)
{
    CvMemStorage* storage = cvCreateMemStorage(0);

    float rho = 0.5f; // Rho Resolution
    float theta = CV_PI/360; // Angle Resolution
    CvSeq* lines = cvCreateSeq( CV_32SC4, sizeof(CvSeq), sizeof(int)*4, (CvMemStorage*)storage );

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
    int low_T; // How angle threshold
    int high_T; // High T

    image = img->imageData;
    step = img->widthStep;
    width = img->width;
    height = img->height;

    numangle = cvRound(CV_PI / theta);
    numrho = cvRound(((width + height) * 2 + 1) / rho);

    // Scale thresholds to image
    targetAngle = (targetAngle+90)%180; //adjust targetAngle to fit the hough graph
    low_T = (targetAngle*numangle/180 - angleThreshold*numangle/180 + numangle)%numangle;
    high_T = (targetAngle*numangle/180 + angleThreshold*numangle/180)%numangle;

    accum = (int*)cvAlloc( sizeof(accum[0]) * (numangle+2) * (numrho+2));
    sort_buf = (int*)cvAlloc( sizeof(accum[0]) * linesMax  );
    tabSin = (float*)cvAlloc( sizeof(tabSin[0]) * numangle );
    tabCos = (float*)cvAlloc( sizeof(tabCos[0]) * numangle );
    memset( accum, 0, sizeof(accum[0]) * (numangle+2) * (numrho+2));
    temp_cluster = (int*)cvAlloc(sizeof(accum[0])*clusterSize);
    // Allocate memory for the cluster log 
    line_clusters = (int**)cvAlloc(sizeof(accum[0])*linesMax);
    for(i=0;i<linesMax;i++)
    line_clusters[i] = (int*)cvAlloc(sizeof(accum[0])*clusterSize);
    
    // Initialize cluster log with -1
    for(i=0;i<linesMax;i++)
      for(j=0;j<clusterSize;j++)
        line_clusters[i][j] = -1;

    // Initialize sort_buf with -1
    for(i=0;i<linesMax;i++)
    sort_buf[i] = -1;

    for (ang = 0, n = 0; n < numangle; ang += theta, n++)
    {
        tabSin[n] = (float)(sin(ang) * irho);
        tabCos[n] = (float)(cos(ang) * irho);
    }

    // Stage 1. fill accumulator
    for (i = 0; i < height; i++) {
        for (j = 0; j < width; j++) {
            if (image[i * step + j] != 0) {
                for (n = 0; n < numangle; n++) {
                    r = cvRound( j * tabCos[n] + i * tabSin[n] );
                    r += (numrho - 1) / 2;
                    accum[(n+1) * (numrho+2) + r+1]++;
                }
            }
        }
    }

    // Stage 2. find local maximums

    for (r = 0; r < numrho; r++)
    {
        for (n = 0; n < numangle; n++)
        {
            int base = (n+1) * (numrho+2) + r+1;
            if (accum[base] > threshold &&
                accum[base] > accum[base - 1] &&
                accum[base] >= accum[base + 1] &&
                accum[base] > accum[base - numrho - 2] &&
                accum[base] >= accum[base + numrho + 2]
               ) {

                // Check to make sure this line is in the angle threshold
                if (low_T < high_T) {
                    if (base/numrho < low_T || base/numrho > high_T) continue;
                } else {
                    if (base/numrho < low_T && base/numrho > high_T) continue;
                }

                newcluster = 1;
                for (i=linesMax-1; i>=0; i--) {
                    // Check to see if this max should be placed into this cluster
                    if (sort_buf[i] != -1 && 
                       ( // It's within a box
                        (abs(base%(numrho+2) - sort_buf[i]%(numrho+2)) < clusterWidth && abs(base/(numrho+2)-sort_buf[i]/(numrho+2)) < clusterHeight)
                         || // ...or it's witthin a box when including rollover
                         (abs(abs(base%(numrho+2)-numrho/2) - abs(sort_buf[i]%(numrho+2)-numrho/2)) < clusterWidth && numangle-abs(base/(numrho+2) - sort_buf[i]/(numrho+2)) < clusterHeight)
                        )
                       )
                    {
                        // If so, sort it into that cluster
                        for (j=0;j<clusterSize;j++) {
                            if (line_clusters[i][j] == -1) {
                                line_clusters[i][j] = base;
                                break;
                            } else if (accum[base] > accum[line_clusters[i][j]]) {
                                for (k=clusterSize-1;k>j;k--) {
                                    line_clusters[i][k] = line_clusters[i][k-1];
                                }
                                line_clusters[i][j] = base;
                                break;
                            }
                        }
                        newcluster = 0;
                        break;      // Don't let this line get placed in two clusters
                    }
                }
                // If this is a new cluster, sort it in by accumulator value
                if (newcluster) {
                    k = -1;
                    for (t=0;t<linesMax;t++) { 
                        if (sort_buf[t] == -1) {
                        // This slot in the sort buff is empty, we can't check accum
                            k=t;
                        } else if (accum[base]>accum[line_clusters[t][0]]) {
                            k=t;
                        }
                    }
                    if (k>-1) {
                        for (j=0;j<k;j++) {
                            sort_buf[j] = sort_buf[j+1];
                            for(i=0; i<clusterSize;i++)
                            line_clusters[j][i] = line_clusters[j+1][i];
                        }
                        sort_buf[k] = base;
                        line_clusters[k][0] = base; 
                        for(i=1;i<clusterSize;i++) {
                            line_clusters[k][i] = -1;
                        }
                    }
                } else {
                    // We just added something to a cluster, so we might have to move
                    // one cluster up in priority       
                    for (i=0; i<linesMax-1; i++) {
                        if (line_clusters[i][0] !=-1 && accum[line_clusters[i][0]] > accum[line_clusters[i+1][0]]) {
                            k=i; //this is the out-of-place cluster 
                            for(t=0;t<clusterSize;t++) 
                                temp_cluster[t] = line_clusters[k][t];
                            for (j=k;  j<linesMax-1 && accum[temp_cluster[0]] > accum[line_clusters[j+1][0]] ; j++) {
                                for(t=0;t<clusterSize;t++)
                                    line_clusters[j][t] = line_clusters[j+1][t];
                            }
                            for(t=0;t<clusterSize;t++)
                                line_clusters[j][t] = temp_cluster[t];
                            break;
                        }
                    }
                    for (i=0; i<linesMax; i++) { //update sort_buf with the newley sorted list of clusters  
                        sort_buf[i] = line_clusters[i][0]; //used to be average
                    }
                }
            }
        }
    }


    // Stage 4. store the lines to the output buffer
    linesMax = linesMax;
    scale = 1./(numrho+2);
    for(i=0; i < linesMax; i++)
    {
        CvLinePolar line;
        int idx = line_clusters[i][0];
        int n = cvFloor(idx*scale) - 1;
        int r = idx - (n+1)*(numrho+2) - 1;
        line.rho = (r - (numrho - 1)*0.5f) * rho;
        line.angle = n * theta;
        if (idx == -1) {
            line.rho = -999;
        }
        cvSeqPush(lines, &line);
    }

    // Free Resources
    cvFree( &sort_buf );
    cvFree( &tabSin );
    cvFree( &tabCos );
    cvFree( &accum );
    for(i=0;i<linesMax;i++)
    {
        cvFree(&line_clusters[i]);
    }
    cvFree( &line_clusters);

    return lines;
}
