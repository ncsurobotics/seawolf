#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

#define IN_RANGE(a, x, b) (((x) < (a)) ? (a) : (((x) > (b)) ? (b) : (x)))

RGBPixel grey = {127, 127, 127};

IplImage* normalize_image(IplImage* img)
{
    double imgAverage_r = 0;
    double imgAverage_g = 0;
    double imgAverage_b = 0;

    uchar* data = (uchar*) img->imageData;

    // Find average color
    for(int i=img->width*img->height; i>=0; i--) {

        // Update the average color
        imgAverage_r = (imgAverage_r*(i)+data[3*i+2])/(i+1);
        imgAverage_g = (imgAverage_g*(i)+data[3*i+1])/(i+1);
        imgAverage_b = (imgAverage_b*(i)+data[3*i+0])/(i+1);
    }

    // Find distance between the average color and grey
    int r_offset = grey.r - imgAverage_r;
    int g_offset = grey.g - imgAverage_g;
    int b_offset = grey.b - imgAverage_b;

    // Normalize!
    for(int i=img->width*img->height; i>=0; i--) { // Fill the acumulator tables
        data[3*i+2] = IN_RANGE(0, data[3*i+2] + r_offset, 255);
        data[3*i+1] = IN_RANGE(0, data[3*i+1] + g_offset, 255);
        data[3*i+0] = IN_RANGE(0, data[3*i+0] + b_offset, 255);
    }
    return img;
}
