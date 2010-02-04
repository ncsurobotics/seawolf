#ifndef __SEAWOLF_VISION_LIB_COLOR_FILTER_INCLUDE_H
#define __SEAWOLF_VISION_LIB_COLOR_FILTER_INCLUDE_H

void colorfilter_init(void);
IplImage* colorfilter(IplImage* img, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax);
void colorfilter_free(void);

#endif
