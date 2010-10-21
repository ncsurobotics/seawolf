#ifndef __SEAWOLF_VISION_LIB_HOUGH_INCLUDE_H
#define __SEAWOLF_VISION_LIB_HOUGH_INCLUDE_H

CvSeq* hough(IplImage* img, IplImage* original, int threshold, int linesMax,int targetAngle, int angleThreshold, int clusterSize, int clusterWidth, int clusterHeight);
void hough_draw_lines(IplImage* image, CvSeq* lines);

#endif
