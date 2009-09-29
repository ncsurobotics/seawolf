
#include "img.h"

#include <opencv/cv.h>
#include <opencv/highgui.h>

void IplImageToImage(IplImage* src, Image* dest) {
    for(int i = src->height * src->width - 1; i >= 0; i--) {
        dest->data.rgb[i].r = src->imageData[(3 * i) + 2];
        dest->data.rgb[i].g = src->imageData[(3 * i) + 1];
        dest->data.rgb[i].b = src->imageData[(3 * i) + 0];
    }
}

void ImageToIplImage(Image* src, IplImage* dest) {
    for(int i = src->height * src->width - 1; i >= 0; i--) {
        dest->imageData[(3 * i) + 2] = src->data.rgb[i].r;
        dest->imageData[(3 * i) + 1] = src->data.rgb[i].g;
        dest->imageData[(3 * i) + 0] = src->data.rgb[i].b;
    }
}

