#ifndef __SEAWOLF_VISION_LIB_EDGE_INCLUDE_H
#define __SEAWOLF_VISION_LIB_EDGE_INCLUDE_H

void edge_opencv_init(void);
IplImage* edge_opencv(IplImage* frame, int low_threshold, int high_threshold, int aperture);
void edge_opencv_free(void);

#endif
