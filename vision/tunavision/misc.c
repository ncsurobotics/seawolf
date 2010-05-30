
#include "seawolf.h"
#include "img.h"

#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

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

/* Computed the norm of the difference of the pixels as vectors in 3-space */
float Pixel_diff(RGBPixel* px_1, RGBPixel* px_2) {
    return sqrt(pow(((short)px_1->r) - px_2->r, 2) +
                pow(((short)px_1->g) - px_2->g, 2) +
                pow(((short)px_1->b) - px_2->b, 2)) * 0.569;
}

bool Pixel_equal(RGBPixel* px_1, RGBPixel* px_2) {
    return memcmp(px_1, px_2, sizeof(RGBPixel)) == 0;
}

float Pixel_brightness(RGBPixel* px) {
    return (px->r + px->g + px->b) / 3.0;
}

RGBPixel Pixel_normalize(RGBPixel* px, int brightness) {
    RGBPixel out;

    float act = Pixel_brightness(px);
    if(act) {
        float factor = brightness / act;

        out.r = Util_min(255, (int) (px->r * factor));
        out.g = Util_min(255, (int) (px->g * factor));
        out.b = Util_min(255, (int) (px->b * factor));
        
    } else {
        out.r = out.g = out.b = brightness;
    }

    return out;
}
