
#include <stdio.h>
#include <cv.h>
#include <highgui.h>  
#include "vision.h"

#include <math.h>
#include <stdlib.h>
#include <string.h>

#ifdef debug_tuna
    int wait = 0,
        blur = 1,
        colorCount = 8,
        colorThreshold = 16,
        colorFilterCount = 1;
#endif

void tuna_init(){
    #ifdef debug_tuna
//    cvNamedWindow("src", 0);
//    cvNamedWindow("out1", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("out2", CV_WINDOW_AUTOSIZE);
//    cvNamedWindow("out3", CV_WINDOW_AUTOSIZE);
//    cvNamedWindow("out4", CV_WINDOW_AUTOSIZE);

//    cvMoveWindow("out1", 200, 50);
    cvMoveWindow("out2", 400, 50);
//    cvMoveWindow("out3", 600, 50);
//    cvMoveWindow("out4", 800, 50);
        
//    cvCreateTrackbar("Wait", "src", &wait, 100, NULL);
//    cvCreateTrackbar("Blur Rounds", "src", &blur, 16, NULL);
//   cvCreateTrackbar("Color Count", "src", &colorCount, 256, NULL);
//   cvCreateTrackbar("Color Blend", "src", &colorThreshold, 256, NULL); 
//   cvCreateTrackbar("Color Filter Threshold", "src", &colorFilterCount, 256, NULL);
    #endif
}

int* Int_new(int n) {
    int* a = malloc(sizeof(int));
    *a = n;
    return a;
}

float* Float_new(float n) {
    float* a = malloc(sizeof(float));
    *a = n;
    return a;
}

float Pixel_stddev(RGBPixel* px_1, RGBPixel* px_2) {
    return sqrt(pow((short)px_1->r - px_2->r, 2) +
                pow((short)px_1->g - px_2->g, 2) +
                pow((short)px_1->b - px_2->b, 2));
}

bool Pixel_equal(RGBPixel* px_1, RGBPixel* px_2) {
    return memcmp(px_1, px_2, sizeof(RGBPixel)) == 0;
}

float Pixel_brightness(RGBPixel* px) {//changing brightness to be the greates of the three colors
    int brightness = px->r > px->g ? px->r : px->g;
    return (brightness > px->b ? brightness : px->b);
//    return (px->r + px->g + px->b) / 3.0; ORIGIONAL LINE
}

RGBPixel Pixel_normalize(RGBPixel* px, int brightness) {
    RGBPixel out;
    float factor = 255 / Pixel_brightness(px);
    out.r = (int) (px->r * factor);
    out.g = (int) (px->g * factor);
    out.b = (int) (px->b * factor);
    return out;
}
