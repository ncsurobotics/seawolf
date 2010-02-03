#ifndef __SEAWOLF_VISION_LIB_HOUGH_INCLUDE_H
#define __SEAWOLF_VISION_LIB_HOUGH_INCLUDE_H

void hough_opencv_init();
CvSeq* hough_opencv(IplImage* img, IplImage* original, int threshold, int linesMax,int targetAngle, int angleThreshold, int clusterSize, int clusterWidth, int clusterHeight);
void hough_opencv_free();

#endif
