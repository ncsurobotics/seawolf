//target_color header

#ifndef __SEAWOLF_VISION_LIB_FIND_TARGET_COLOR_INCLUDE_H
#define __SEAWOLF_VISION_LIB_FIND_TARGET_COLOR_INCLUDE_H

struct RGBPixel_s {
    unsigned char r; /**< A char containing the red channel of a pixel */
    unsigned char g; /**< A char containing the green channel of a pixel */
    unsigned char b; /**< A char containing the blue channel of a pixel */
};

typedef struct RGBPixel_s RGBPixel;

//Functions: 
int FindTargetColor(IplImage* in, IplImage* out, RGBPixel* color, int min_blobsize, int dev_threshold, double precision_threshold);

float Pixel_stddev(RGBPixel* px_1, RGBPixel* px_2);

#endif 
