
#define __IMAGE__
#include "img.h"

#include <stdlib.h>
#include <string.h>

RGBPixel WHITE = {255, 255, 255};
RGBPixel BLACK = {0, 0, 0};
RGBPixel RED = {255, 0, 0};
RGBPixel GREEN = {0, 255, 0};
RGBPixel BLUE = {0, 0, 255};
RGBPixel YELLOW = {255, 255, 0};
RGBPixel ORANGE = {0xff, 0x80, 0};

Image* Image_new(enum ColorMode mode, unsigned int width, unsigned int height) {
    Image* img = malloc(sizeof(Image));
    if(img == NULL) {
        return NULL;
    }

    img->width = width;
    img->height = height;
    img->mode = mode;
    if(img->mode == INDEXED) {
        img->data.indexed = calloc(sizeof(IndexedPixel), width * height);
        if(img->data.indexed == NULL) {
            free(img);
            return NULL;
        }
        img->palette = malloc(sizeof(RGBPixel) * 256);
        if(img->palette == NULL) {
            free(img->data.indexed);
            free(img);
            return NULL;
        }

        /* Build default, grayscale palette */
        img->palette_size = 256;
        for(int i = 0; i < 256; i++) {
            img->palette[i].r = i;
            img->palette[i].g = i;
            img->palette[i].b = i;
        }
    } else if(img->mode == RGB) {
        img->data.rgb = calloc(sizeof(RGBPixel), width * height);
        if(img->data.rgb == NULL) {
            free(img);
            return NULL;
        }
    } else {
        free(img);
        return NULL;
    }
    
    return img;
}

Image* Image_newFrom(Image* img) {
    return Image_new(img->mode, img->width, img->height);
}

void Image_copy(Image* src, Image* dest) {
    if(src->mode == RGB) {
        memcpy(dest->data.rgb, src->data.rgb, sizeof(RGBPixel) * src->width * src->height);
    } else {
        memcpy(dest->data.indexed, src->data.indexed, sizeof(IndexedPixel) * src->width * src->height);
        memcpy(dest->palette, src->palette, sizeof(RGBPixel) * 256);
        dest->palette_size = src->palette_size;
    }
}

Image* Image_duplicate(Image* img) {
    Image* new = Image_new(img->mode, img->width, img->height);
    if(img == NULL) {
        return NULL;
    }
    
    Image_copy(img, new);

    return new;
}

void Image_destroy(Image* img) {
    free(img->data.indexed);
    free(img);
}

